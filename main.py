import os
from dotenv import load_dotenv

from clients import TelegramBotClient, DomRiaClient


if __name__ == '__main__':
    load_dotenv('.env')

    bot_token = os.getenv('bot_token')
    chat_id = os.getenv('chat_id')
    dom_ria_api_key = os.getenv('dom_ria_api_key')

    client = TelegramBotClient(bot_token, chat_id)
    dom_ria_client = DomRiaClient(dom_ria_api_key)

    ids = dom_ria_client.get_ids()
    for id in ids:
        message = dom_ria_client.generate_message(id)
        client.send_message(message)
