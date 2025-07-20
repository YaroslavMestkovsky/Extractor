import os
from turtledemo.penrose import start

from script import BrowserAutomation

import asyncio
import logging
import pandas as pd


async def main():
    """Основная функция для запуска автоматизации."""
    automation = BrowserAutomation()

    try:
        await automation.execute_actions()
    except Exception as e:
        automation.logger.error(f"Произошла ошибка: {str(e)}")
        await automation.close_browser()


def run():
    """Запуск программы с обработкой ошибок."""
    logger = logging.getLogger(__name__)
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    automation = BrowserAutomation()
    logger = logging.getLogger(__name__)

    for file in os.listdir('../Downloads'):
        analytics = True
        logger.info(f'Start uploading {file}')
        df = pd.read_excel(f'../Downloads/{file}')

        if 'E' in file:
            analytics = False

        automation.postgres_manager.upload(df, analytics)
