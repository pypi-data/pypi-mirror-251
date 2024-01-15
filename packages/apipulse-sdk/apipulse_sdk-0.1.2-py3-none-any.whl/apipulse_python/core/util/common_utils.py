
HEADERS = None

def get_headers():
    global HEADERS
    if HEADERS:
        return HEADERS
    else:
        build_headers()
        return HEADERS


def build_headers():
    from ..apipulse_sdk import options as OPTIONS
    from apipulse_python.sdk_logger import logger
    from apipulse_python.core.model.sdk_options import SdkOptions
    options: SdkOptions = OPTIONS
    global HEADERS
    HEADERS = {
        'X-API-KEY': options.auth_key,
        'X-PARTNER-ID': options.partner_id,
        'X-ENV-NAME': options.environment,
        'X-TEAM-NAME': options.team_name,
        'X-SERVICE-NAME': options.application_name,
        'Content-Type': 'application/json'
    }
