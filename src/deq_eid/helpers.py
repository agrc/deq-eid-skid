import logging
from os import sep, walk
from os.path import basename, join, normpath
from zipfile import ZIP_DEFLATED, ZipFile

import palletjack

try:
    from . import config
except ImportError:
    import config

logger = logging.getLogger(config.SKID_NAME)


def convert_to_int(s):
    """Convert a string to an integer. If the string cannot be converted, return -1."""
    if s is None:
        return None

    try:
        return int(s)
    except ValueError:
        return -1


class SalesForceRecords:
    """A helper class that extracts data from Salesforce for a specific table/api."""

    table = "table"
    feature_layer = "feature_layer"

    def __init__(
        self,
        salesforce_extractor: palletjack.extract.SalesforceRestLoader,
        salesforce_api: str,
        field_configs,
        where_clause,
    ):
        self.salesforce_extractor = salesforce_extractor
        self.salesforce_api = salesforce_api
        self.field_configs = field_configs
        self.where_clause = where_clause

    def extract_data_from_salesforce(self):
        """Load data from Salesforce into self.df dataframe

        Builds a string of needed column names for our specific needs and uses that in the REST query.
        """

        fields_string = self._build_columns_string()

        #: Main query with just our desired fields
        self.df = self.salesforce_extractor.get_records(
            "services/data/v60.0/query/",
            f"SELECT {fields_string} from {self.salesforce_api} where {self.where_clause}",
        )

        self.df.drop(columns=["attributes"], inplace=True)

        field_mappings = {c.sf_field: c.agol_field for c in self.field_configs if c.sf_field is not None}
        self.df.rename(mapper=field_mappings, axis=1, inplace=True)

        for field_config in self.field_configs:
            if field_config.field_type == config.FieldConfig.static:
                self.df[field_config.agol_field] = field_config.static_value
            elif field_config.field_type == config.FieldConfig.integer:
                self.df[field_config.agol_field] = self.df[field_config.agol_field].apply(convert_to_int)
            elif field_config.field_type == config.FieldConfig.text:
                self.df[field_config.agol_field] = self.df[field_config.agol_field].apply(str)
            elif field_config.field_type == config.FieldConfig.composite:
                self.df[field_config.agol_field] = self.df.apply(
                    lambda x: field_config.composite_format.format(**dict(x)), axis=1
                )

        #: ints
        self.df = palletjack.transform.DataCleaning.switch_to_nullable_int(
            self.df,
            [c.agol_field for c in self.field_configs if c.field_type == c.integer],
        )

        #: dates
        self.df = palletjack.transform.DataCleaning.switch_to_datetime(
            self.df,
            [c.agol_field for c in self.field_configs if c.field_type == c.date],
        )
        self.df["Date_Discovered"] = self.df["Date_Discovered_For_Filter"].dt.strftime("%m/%d/%Y")

        self.df = self.df.query("Northing > 0 & Easting > 0 & DERRID.notnull()")

    def _build_columns_string(self) -> str:
        """Build a string of needed columns for the SOQL query based on field mapping and some custom fields

        Returns:
            str: A comma-delimited string of needed columns for the SOQL query
        """
        fields = list([c.sf_field for c in self.field_configs if c.sf_field is not None])
        fields_string = ",".join(fields)

        return fields_string


def zip_fgdb(fgdb_path, zip_file_path):
    with ZipFile(zip_file_path, "w", ZIP_DEFLATED) as zip_file:
        fgdb_path = normpath(fgdb_path)
        for dirpath, dirnames, filenames in walk(fgdb_path):
            for file in filenames:
                # Ignore .lock files
                if not file.endswith(".lock"):
                    try:
                        zip_file.write(
                            join(dirpath, file),
                            join(basename(fgdb_path), join(dirpath, file)[len(fgdb_path) + len(sep) :]),
                        )

                    except Exception as e:
                        logger.warn("error zipping file geodatabase: {}".format(e))
        return None
