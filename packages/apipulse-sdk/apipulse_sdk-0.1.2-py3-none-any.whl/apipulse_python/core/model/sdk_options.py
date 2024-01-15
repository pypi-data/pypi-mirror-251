from typing import List

from apipulse_python.sdk_logger import logger


class SdkOptions:
    def __init__(
        self,
        url: str,
        application_name: str,
        auth_key: str,
        environment: str,
        logging_enabled: bool,
        log_level: str,
        mask_headers: List[str],
        capture: str,
        partner_id: str,
        team_name: str,
    ):
        self.url: str = url
        self.application_name: str = application_name
        self.auth_key: str = auth_key
        self.environment: str = environment
        self.logging_enabled: bool = logging_enabled
        self.log_level: str = log_level
        self.mask_headers: List[str] = mask_headers
        self.capture: str = capture
        self.partner_id = partner_id
        self.team_name = team_name

    def sanitize(self):
        self.url = self.url if not self.url else self.url.strip()
        self.application_name = self.application_name if not self.application_name else self.application_name.strip()
        self.auth_key = self.auth_key if not self.auth_key else self.auth_key.strip()
        self.environment = self.environment if not self.environment else self.environment.strip()
        self.capture = self.capture.strip() if self.capture and self.capture.strip() == "always" else None
        self.partner_id = self.partner_id if not self.partner_id else self.partner_id.strip()
        self.team_name = self.team_name if not self.team_name else self.team_name.strip()

    def validate(self):
        if not self.environment or self.environment == "":
            logger.error("Missing option: `environment` is required")
            return False
        if self.url == "":
            logger.error("Missing option: `url` is required")
            return False
        if self.application_name == "":
            logger.error("Missing option: `application_name` is required")
            return False
        if not self.partner_id:
            logger.error("Missing option: `partner_id` is required")
            return False
        if not self.team_name:
            logger.error("Missing option: `team_name` is required")
            return False
        return True

    def __str__(self):
        return (
            f"SdkOptions(url={self.url}, "
            f"application_name={self.application_name}, "
            f"auth_key={self.auth_key}, "
            f"environment={self.environment}, "
            f"logging_enabled={self.logging_enabled}, "
            f"log_level={self.log_level}, "
            f"mask_headers={self.mask_headers}, "
            f"capture={self.capture}, "
            f"partner_id={self.partner_id}, "
            f"team_name={self.team_name}),"
        )
