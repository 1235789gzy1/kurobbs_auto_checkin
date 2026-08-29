import os
from dataclasses import dataclass
from typing import List, Optional


class SettingsError(Exception):
    """Raised when required settings are missing or invalid."""


def parse_bool(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


@dataclass
class Settings:
    token: str
    debug: bool = False
    bark_device_key: Optional[str] = None
    bark_server_url: Optional[str] = None
    server3_send_key: Optional[str] = None
    telegram_bot_token: Optional[str] = None
    telegram_chat_id: Optional[str] = None

    @classmethod
    def load(cls) -> "Settings":
        token = os.getenv("TOKEN")
        if not token:
            raise SettingsError("TOKEN is required but missing.")

        return cls(
            token=token,
            debug=parse_bool(os.getenv("DEBUG", "")),
            bark_device_key=os.getenv("BARK_DEVICE_KEY"),
            bark_server_url=os.getenv("BARK_SERVER_URL"),
            server3_send_key=os.getenv("SERVER3_SEND_KEY"),
            telegram_bot_token=os.getenv("TELEGRAM_BOT_TOKEN"),
            telegram_chat_id=os.getenv("TELEGRAM_CHAT_ID"),
        )

    def sensitive_values(self) -> List[str]:
        """Values that should be redacted from logs."""
        return [
            value
            for value in [
                self.token,
                self.bark_device_key,
                self.bark_server_url,
                self.server3_send_key,
                self.telegram_bot_token,
                self.telegram_chat_id,
            ]
            if value
        ]
