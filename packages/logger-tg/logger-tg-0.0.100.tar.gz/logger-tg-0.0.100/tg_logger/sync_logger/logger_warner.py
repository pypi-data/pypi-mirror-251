import asyncio

import aiohttp
import requests

from tg_logger.settings import SyncTgLoggerSettings


class ClientLogger:
    MAX_MSG_LENGTH: int = 4096

    def __init__(self, settings: SyncTgLoggerSettings):
        self.bot_token = settings.bot_token
        self.recipient_id = settings.recipient_id
        self.api_url = (
            f'https://api.telegram.org/bot{self.bot_token}/sendMessage')

    def format_message(self, message: str) -> list[str]:
        message = message.strip()
        if len(message) <= self.MAX_MSG_LENGTH:
            return [message]
        return [message[i:i + self.MAX_MSG_LENGTH] for i in
                range(0, len(message), self.MAX_MSG_LENGTH)]

    def send_error(self, message):
        data = {'chat_id': self.recipient_id}
        for message in self.format_message(message):
            data['text'] = message
            try:
                asyncio.get_running_loop()
            except RuntimeError:
                self.send_error_sync(data)
            else:
                asyncio.create_task(self.send_error_async(data))

    def send_error_sync(self, data: dict):
        try:
            response = requests.post(self.api_url, data=data)
            response.raise_for_status()
        except Exception as e:
            print(f'Error sending message: {e}')

    async def send_error_async(self, data: dict):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.api_url, data=data) as response:
                    response.raise_for_status()
            except Exception as e:
                print(f'Error sending message: {e}')
