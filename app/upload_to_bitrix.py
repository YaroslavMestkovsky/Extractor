import os

from script import BrowserAutomation

import logging
import pandas as pd


if __name__ == "__main__":
    automation = BrowserAutomation()
    logger = logging.getLogger(__name__)

    for file in os.listdir('../Downloads'):
        if 'Bitrix' in file:
            logger.info(f'Start uploading {file}')
            df = pd.read_excel(f'../Downloads/{file}')

            automation.bitrix_manager.upload(df)
