#!/usr/bin/env python
# * coding: utf8 *
"""
Run the deq_eid script as a cloud function.
"""
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

import arcgis
from arcgis.features import GeoAccessor
from arcgis.gis._impl._content_manager import SharingLevel
from palletjack import extract, load
from supervisor.message_handlers import SendGridHandler
from supervisor.models import MessageDetails, Supervisor

#: This makes it work when calling with just `python <file>`/installing via pip and in the gcf framework, where
#: the relative imports fail because of how it's calling the function.
try:
    from . import config, helpers, version
except ImportError:
    import config
    import helpers
    import version


class Skid:
    def __init__(self):
        self.secrets = SimpleNamespace(**self._get_secrets())
        self.tempdir = TemporaryDirectory(ignore_cleanup_errors=True)
        self.tempdir_path = Path(self.tempdir.name)
        # self.log_name = f'{config.LOG_FILE_NAME}_{datetime.now().strftime("%Y%m%d-%H%M%S")}.txt'
        self.log_name = f"{config.LOG_FILE_NAME}.txt"
        self.log_path = self.tempdir_path / self.log_name
        self._initialize_supervisor()
        self.skid_logger = logging.getLogger(config.SKID_NAME)

        self.skid_logger.info("Initializing AGOL connection...")
        self.gis = arcgis.gis.GIS(
            config.AGOL_ORG,
            self.secrets.AGOL_USER,
            self.secrets.AGOL_PASSWORD,
        )

        self.skid_logger.info("Initializing Salesforce connection...")
        salesforce_credentials = extract.SalesforceApiUserCredentials(
            self.secrets.SF_CLIENT_SECRET,
            self.secrets.SF_CLIENT_ID,
        )
        self.salesforce_extractor = extract.SalesforceRestLoader(
            self.secrets.SF_ORG,
            salesforce_credentials,
        )

    def __del__(self):
        self.tempdir.cleanup()

    @staticmethod
    def _get_secrets():
        """A helper method for loading secrets from either a GCF mount point or the local src/deq_eid/secrets/secrets.json file

        Raises:
            FileNotFoundError: If the secrets file can't be found.

        Returns:
            dict: The secrets .json loaded as a dictionary
        """

        secret_folder = Path("/secrets")

        #: Try to get the secrets from the Cloud Function mount point
        if secret_folder.exists():
            return json.loads(Path("/secrets/app/secrets.json").read_text(encoding="utf-8"))

        #: Otherwise, try to load a local copy for local development
        #: This file path might not work if extracted to its own module
        secret_folder = Path(__file__).parent / "secrets"
        if secret_folder.exists():
            return json.loads((secret_folder / "secrets.json").read_text(encoding="utf-8"))

        raise FileNotFoundError("Secrets folder not found; secrets not loaded.")

    def _initialize_supervisor(self):
        """A helper method to set up logging and supervisor

        Returns:
            Supervisor: The supervisor object used for sending messages
        """

        skid_logger = logging.getLogger(config.SKID_NAME)
        skid_logger.setLevel(config.LOG_LEVEL)
        palletjack_logger = logging.getLogger("palletjack")
        palletjack_logger.setLevel(config.LOG_LEVEL)

        cli_handler = logging.StreamHandler(sys.stdout)
        cli_handler.setLevel(config.LOG_LEVEL)
        formatter = logging.Formatter(
            fmt="%(levelname)-7s %(asctime)s %(name)15s:%(lineno)5s %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        cli_handler.setFormatter(formatter)

        log_handler = logging.FileHandler(self.log_path, mode="w")
        log_handler.setLevel(config.LOG_LEVEL)
        log_handler.setFormatter(formatter)

        skid_logger.addHandler(cli_handler)
        skid_logger.addHandler(log_handler)
        palletjack_logger.addHandler(cli_handler)
        palletjack_logger.addHandler(log_handler)

        #: Log any warnings at logging.WARNING
        #: Put after everything else to prevent creating a duplicate, default formatter
        #: (all log messages were duplicated if put at beginning)
        logging.captureWarnings(True)

        skid_logger.debug("Creating Supervisor object")
        self.supervisor = Supervisor(handle_errors=False)
        sendgrid_settings = config.SENDGRID_SETTINGS
        sendgrid_settings["api_key"] = self.secrets.SENDGRID_API_KEY
        self.supervisor.add_message_handler(
            SendGridHandler(
                sendgrid_settings=sendgrid_settings, client_name=config.SKID_NAME, client_version=version.__version__
            )
        )

    def _remove_log_file_handlers(self):
        """A helper function to remove the file handlers so the tempdir will close correctly"""

        loggers = [logging.getLogger(config.SKID_NAME), logging.getLogger("palletjack")]

        for logger in loggers:
            for handler in logger.handlers:
                try:
                    if self.log_name in handler.stream.name:
                        logger.removeHandler(handler)
                        handler.close()
                except Exception:
                    pass

    def _get_environmental_incidents(self) -> GeoAccessor:
        #: Load data from Salesforce and generate analyses using Summarize methods
        self.skid_logger.info("loading records from Salesforce...")
        records = helpers.SalesForceRecords(
            self.salesforce_extractor,
            "Case",
            config.INCIDENTS_FIELDS,
            "Utm_N_Y_7_dgts__c != null and Utm_E_X_6_dgts__c != null",
        )
        records.extract_data_from_salesforce()

        self.skid_logger.info("converting to spatial dataframe...")
        sdf = GeoAccessor.from_xy(records.df, "Easting", "Northing", sr=26912)

        self.skid_logger.info("projecting...")
        sdf.spatial.project(3857, "NAD_1983_To_WGS_1984_5")

        return sdf

    def _publish_layer(self, table_name, title, sdf):
        import arcpy

        #: save to a feature class just so that we can add field aliases
        self.skid_logger.info("saving to feature class...")
        feature_class_path = self.tempdir_path / f"{table_name}.gdb" / table_name
        if arcpy.Exists(feature_class_path):
            self.skid_logger.info("deleting existing feature class...")
            arcpy.management.Delete(feature_class_path)
        elif not arcpy.Exists(feature_class_path.parent):
            self.skid_logger.info("creating gdb...")
            arcpy.management.CreateFileGDB(
                str(feature_class_path.parent.parent),
                feature_class_path.parent.name,
            )
        sdf.spatial.to_featureclass(
            location=feature_class_path,
            sanitize_columns=False,
        )

        aliases = {field.agol_field: field.alias for field in config.INCIDENTS_FIELDS}
        for field in arcpy.Describe(str(feature_class_path)).fields:
            if field.name in aliases:
                arcpy.management.AlterField(
                    str(feature_class_path),
                    field.name,
                    new_field_alias=aliases[field.name],
                )

        zip_path = self.tempdir_path / f"{table_name}.zip"
        helpers.zip_fgdb(feature_class_path.parent, zip_path)
        fgdb_item = self.gis.content.add(
            {
                "type": "File Geodatabase",
            },
            data=str(zip_path),
            folder="Interactive Map",
        )
        layer_item = fgdb_item.publish(
            publish_parameters={
                "name": title,
                "layerInfo": {
                    "capabilities": "Query",
                },
            },
        )
        manager = arcgis.features.FeatureLayerCollection.fromitem(layer_item).manager
        manager.update_definition({"capabilities": "Query,Extract,Sync"}),
        layer_item.update({"title": title})
        layer_item.sharing.sharing_level = SharingLevel.EVERYONE
        # layer_item.protect()

        print(f"feature layer published: {title} | {layer_item.id}")

    def update(self):
        # start = datetime.now()

        # incidents_loader = load.FeatureServiceUpdater(gis, config.STATEWIDE_LAYER_ITEMID, self.tempdir_path)
        # statewide_count = statewide_loader.truncate_and_load_features(statewide_spatial)
        pass

        # end = datetime.now()

        # summary_message = MessageDetails()
        # summary_message.subject = f"{config.SKID_NAME} Update Summary"
        # summary_rows = [
        #     f'{config.SKID_NAME} update {start.strftime("%Y-%m-%d")}',
        #     "=" * 20,
        #     "",
        #     f'Start time: {start.strftime("%H:%M:%S")}',
        #     f'End time: {end.strftime("%H:%M:%S")}',
        #     f"Duration: {str(end-start)}",
        #     "",
        #     f"Incidents rows loaded: {len(records.df)}",
        # ]

        # summary_message.message = "\n".join(summary_rows)
        # summary_message.attachments = self.tempdir_path / self.log_name

        # self.supervisor.notify(summary_message)

        self._remove_log_file_handlers()

    def publish(self):
        """Publish new AGOL hosted feature layers"""

        #: NOTE: this method requires arcpy

        incidents_sdf = self._get_environmental_incidents()

        self._publish_layer(
            "EnvironmentalIncidents",
            "Environmental Incidents",
            incidents_sdf,
        )

        self._remove_log_file_handlers()


def main(event, context):  # pylint: disable=unused-argument
    """Entry point for Google Cloud Function triggered by pub/sub event

    Args:
         event (dict):  The dictionary with data specific to this type of
                        event. The `@type` field maps to
                         `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
                        The `data` field maps to the PubsubMessage data
                        in a base64-encoded string. The `attributes` field maps
                        to the PubsubMessage attributes if any is present.
         context (google.cloud.functions.Context): Metadata of triggering event
                        including `event_id` which maps to the PubsubMessage
                        messageId, `timestamp` which maps to the PubsubMessage
                        publishTime, `event_type` which maps to
                        `google.pubsub.topic.publish`, and `resource` which is
                        a dictionary that describes the service API endpoint
                        pubsub.googleapis.com, the triggering topic's name, and
                        the triggering event type
                        `type.googleapis.com/google.pubsub.v1.PubsubMessage`.
    Returns:
        None. The output is written to Cloud Logging.
    """

    #: Call process() and any other functions you want to be run as part of the skid here.
    skid = Skid()

    #: choose one of the following
    skid.publish()  #: requires arcpy
    # skid.update()


#: Putting this here means you can call the file via `python main.py` and it will run. Useful for pre-GCF testing.
if __name__ == "__main__":
    main(1, 2)  #: Just some junk args to satisfy the signature needed for Cloud Functions
