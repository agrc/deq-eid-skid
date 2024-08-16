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
except Exception:
    HOST_NAME = socket.gethostname()

SENDGRID_SETTINGS = {  #: Settings for SendGridHandler
    "from_address": "noreply@utah.gov",
    "to_addresses": ["stdavis@utah.gov"],
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
    FieldConfig("Id", "Id", "Spill ID", "text"),
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

CHEMICAL_SF_API = "Chemicals__c"
CHEMICAL_TITLE = "Chemicals"
CHEMICAL_TABLE_NAME = "DEQMAP_EIChemical"
CHEMICAL_FIELDS = (
    FieldConfig("SpillId", "Case__c", "Spill ID", "text"),
    FieldConfig("Chemical_Number", "Legacy_Id__c", "Chemical Number", "text"),
    FieldConfig("Chemical", "Material_Chem__c", "Chemical Name", "text"),
    FieldConfig("Chemical_Name", "Chemical_Name_Text__c", "Chemical Name Text", "text"),
    FieldConfig("Chemical_Other", "If_Other_Material_Chem_describe__c", "Other Chemical", "text"),
    FieldConfig("Amount", "Amount__c", "Amount", "text"),
    FieldConfig("Amount_Type", "Amount_Type__c", "Amount Type", "text"),
    FieldConfig("Amount_Other", "If_Other_Amount_Type_describe__c", "Amount Other", "text"),
)

MEDIA_SF_API = "Impacted_Media__c"
MEDIA_TITLE = "Impacted Media"
MEDIA_TABLE_NAME = "DEQmap_ImpactedMedia"
MEDIA_FIELDS = (
    FieldConfig("SpillId", "Case__c", "Spill ID", "text"),
    FieldConfig("WaterwayName", "Waterway_Name__c", "Waterway Name", "text"),
    FieldConfig("ImpactedMediaOther", "If_Other_Impacted_Media_describe__c", "Impacted Media Other", "text"),
    FieldConfig("ImpactedMedia", "Impacted_Media_List__c", "Impacted Media", "text"),
    FieldConfig("In_NearWater", "In_Near_Surface_Water__c", "In or Near Water", "text"),
    FieldConfig("LandUse", "Land_Use__c", "Land Use", "text"),
)
