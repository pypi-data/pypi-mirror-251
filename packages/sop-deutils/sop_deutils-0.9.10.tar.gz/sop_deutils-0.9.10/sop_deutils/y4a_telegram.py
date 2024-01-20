import requests
import logging
import warnings
import pandas as pd
import numpy as np

warnings.filterwarnings("ignore", category=UserWarning)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
)


def send_message(
    text: str,
    bot_token: str = None,
    chat_id: str = None,
):
    """
    Send a message to a group chat of Telegram

    :param text: the message to send
    :param bot_token: the token of the bot which send the message
    :param chat_id: the chat id where the message is sent
    """

    if not bot_token:
        bot_token = '6318613524:AAG3_JGEsTZbSvcupG5aJk-jZPzghuf3yZ4'
    if not chat_id:
        chat_id = '-868321875'

    telegram_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown',
    }
    response = requests.post(telegram_url, json=payload)
    if response.status_code == 200:
        logging.info('Telegram alert sent successfully!')
    else:
        logging.info('Failed to send Telegram alert!')
        logging.error(response.text)


def send_data(
    data: pd.DataFrame,
    bot_token: str = None,
    chat_id: str = None,
):
    """
    Send data to a group chat of Telegram

    :param data: the data to send
    :param bot_token: the token of the bot which send data
    :param chat_id: the chat id where data is sent
    """

    df = data.copy()

    df = df.rename(
        columns=lambda x: x.replace(':', ' ')
        .replace('_', ' ')
        .replace('/', ' ')
        .replace('-', ' ')
        .strip().lower()
    )
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: x.replace('_', ' ')
            if isinstance(x, str)
            else x
        )
    df = df.replace(np.nan, 'None')
    df_txt = df.to_markdown(
        headers='keys',
        tablefmt='psql',
        index=False,
    )

    send_message(
        text=df_txt,
        bot_token=bot_token,
        chat_id=chat_id,
    )
