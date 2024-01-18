from nomad_media_pip.exceptions.api_exception_handler import _api_exception_handler
from nomad_media_pip.helpers.slugify import _slugify

import requests, json

def _create_and_update_event(AUTH_TOKEN, URL, CONTENT_ID, CONTENT_DEFINITION_ID, 
                             START_DATETIME, END_DATETIME, PROPERTIES, DEBUG):
    
    HEADERS = {
        "Authorization": "Bearer " + AUTH_TOKEN,
        "Content-Type": "application/json"
    }

    if (CONTENT_ID == ""):
        API_URL = f"{URL}/content/new?contentDefinitionId={CONTENT_DEFINITION_ID}"

        if DEBUG:
            print(f"URL: {API_URL},\nMETHOD: GET")

        try:
            RESPONSE = requests.get(API_URL, headers= HEADERS)

            if not RESPONSE.ok:
                raise Exception()

            INFO = RESPONSE.json()
            CONTENT_ID = INFO["contentId"]
        except:
            _api_exception_handler(RESPONSE, "Create Event Failed")

    API_URL = f"{URL}/content/{CONTENT_ID}"

    if not PROPERTIES: PROPERTIES = {}

    PROPERTIES["startDateTime"] = START_DATETIME
    PROPERTIES["endDateTime"] = END_DATETIME

    BODY = {
        "contentId": CONTENT_ID,
        "contentDefinitionId": CONTENT_DEFINITION_ID,
        "properties": PROPERTIES
    }

    if DEBUG:
        print(f"URL: {API_URL},\nMETHOD: POST,\nBODY: {json.dumps(BODY, indent= 4)})")

    try:
        RESPONSE = requests.post(API_URL, headers= HEADERS, data= json.dumps(BODY))

        if not RESPONSE.ok:
            raise Exception()

        return RESPONSE.json()
    except:
        _api_exception_handler(RESPONSE, "Create Event Failed")