
import requests
from loguru import logger
from serverchan_sdk import sc_send

from settings import Settings


class NotificationService:
    """Aggregate notification channels for GitHub Actions."""

    def __init__(self, settings: Settings):
        self.settings = settings

    def send(self, message: str):
        title = "库街区自动签到任务"
        delivered = [
            self._send_bark(title, message),
            self._send_server3(title, message),
            self._send_telegram(title, message),
        ]
        if not any(delivered):
            logger.debug("No notification channel configured; skipped sending result.")

    def _send_bark(self, title: str, message: str) -> bool:
        if not self.settings.bark_device_key or not self.settings.bark_server_url:
            return False

        url = f"{self.settings.bark_server_url}/{self.settings.bark_device_key}/{title}/{message}"
        try:
            response = requests.get(url, timeout=10)
            logger.debug("Sent Bark notification, status={}", response.status_code)
        except requests.RequestException as exc:
            logger.warning("Failed to push Bark notification: {}", exc)
        return True

    def _send_server3(self, title: str, message: str) -> bool:
        if not self.settings.server3_send_key:
            return False

        try:
            response = sc_send(
                self.settings.server3_send_key,
                title,
                message,
                {"tags": "Github Action|库街区"},
            )
            logger.debug("Sent ServerChan3 notification: {}", response)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to push ServerChan3 notification: {}", exc)
        return True

    def _send_telegram(self, title: str, message: str) -> bool:
        """Send the result through the Telegram Bot API."""
        if not self.settings.telegram_bot_token or not self.settings.telegram_chat_id:
            return False

        url = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}/sendMessage"
        try:
            response = requests.post(
                url,
                json={
                    "chat_id": self.settings.telegram_chat_id,
                    "text": f"{title}\n\n{message}",
                },
                timeout=10,
            )
            response.raise_for_status()
            logger.debug("Sent Telegram notification, status={}", response.status_code)
            return True
        except requests.RequestException as exc:
            logger.warning("Failed to push Telegram notification: {}", exc)
            return False
