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

AGOL_ORG = "https://utahdeq.maps.arcgis.com"
SENDGRID_SETTINGS = {  #: Settings for SendGridHandler
    "from_address": "noreply@utah.gov",
    "to_addresses": ["stdavis@utah.gov"],
    "prefix": f"{SKID_NAME} on {HOST_NAME}: ",
}
LOG_LEVEL = logging.DEBUG
LOG_FILE_NAME = "log"

FEATURE_LAYER_ITEMID = ""
JOIN_COLUMN = ""
ATTACHMENT_LINK_COLUMN = ""
ATTACHMENT_PATH_COLUMN = ""
FIELDS = {}
