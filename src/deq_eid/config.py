"""
config.py: Configuration values. Secrets to be handled with Secrets Manager
"""

import logging
import socket
import urllib

SKID_NAME = "deq-eid"

#: Try to get project id from GCP metadata server for hostname. If it's empty or errors out, revert to local hostname
try:
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    if not project_id:
        raise ValueError
    HOST_NAME = project_id
    IS_LOCAL_DEV = False
except Exception:
    HOST_NAME = socket.gethostname()
    IS_LOCAL_DEV = True

SENDGRID_SETTINGS = {  #: Settings for SendGridHandler
    "from_address": "noreply@utah.gov",
    "to_addresses": ["ugrc-developers@utah.gov"],
    "prefix": f"{SKID_NAME} on {HOST_NAME}: ",
}
LOG_LEVEL = logging.DEBUG
LOG_FILE_NAME = "log"


class FieldConfig:
    #: field types
    text = "text"
    integer = "integer"
    float = "float"
    date = "date"
    static = "static"
    composite = "composite"

    def __init__(self, agol_field, sf_field, alias, field_type, static_value=None, composite_format=None):
        self.agol_field = agol_field
        self.sf_field = sf_field
        self.alias = alias

        if field_type not in (self.text, self.integer, self.date, self.static, self.composite):
            raise ValueError(f"Invalid field type: {field_type}")
        self.field_type = field_type

        if field_type == self.static and static_value is None:
            raise ValueError("Field type 'static' must have a 'static_value'")
        elif field_type != self.static and static_value is not None:
            raise ValueError("Field type '{field_type}' cannot have a 'static_value'")
        self.static_value = static_value

        if field_type == self.composite and composite_format is None:
            raise ValueError("Field type 'composite' must have a 'composite_format'")
        elif field_type != self.composite and composite_format is not None:
            raise ValueError("Field type '{field_type}' cannot have a 'composite_format'")
        self.composite_format = composite_format


INCIDENTS_SF_API = "Case"
INCIDENTS_TITLE = "Environmental Incidents"
INCIDENTS_TABLE_NAME = "EnvironmentalIncidents"
INCIDENTS_FIELDS = (
    #: AGOL field name, Salesforce field name, AGOL Alias, type
    FieldConfig("Id", "CaseNumber", "Spill ID", "text"),
    FieldConfig('Salesforce_Id', "Id", "Salesforce ID", "text"),
    FieldConfig("SITEDESC", None, "Site Program Description", "static", static_value="Environmental Incidents"),
    FieldConfig("Northing", "Utm_N_Y_7_dgts__c", "Northing", "integer"),
    FieldConfig("Easting", "Utm_E_X_6_dgts__c", "Easting", "integer"),
    FieldConfig("Title_EventName", "Title_Event_Name__c", "Title Event Name", "text"),
    FieldConfig("Address_Location", "Address_Location__c", "Address Location", "text"),
    FieldConfig("Nearest_City", "Nearest_Town_City__c", "Nearest City", "text"),
    FieldConfig("Date_Discovered", None, "Date Discovered", "static", static_value=""),  #: populated later
    FieldConfig("Responsible_Party", "Responsible_Party_Name__c", "Responsible Party", "text"),
    FieldConfig("County", "County__c", "County", "text"),
    FieldConfig("Map_Label", None, "Map Label", "composite", composite_format="{SITEDESC} - {DERRID}"),
    FieldConfig("DERRID", "INR_Number__c", "DERR ID", "text"),
    FieldConfig("Date_Discovered_For_Filter", "Date_Time_Discovered__c", "Date Discovered For Filter", "date"),
    FieldConfig("Incident_summary", "Event_Description_Initial_Actions_Taken__c", "Incident Summary", "text"),
)
