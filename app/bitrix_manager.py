import configparser
from typing import Any

import pandas as pd
import requests
import json
import datetime

from app.enums import BitrixDealsEnum

db_confing = "app/bitrix.conf"
config = configparser.ConfigParser()
config.read(db_confing)


class BitrixManager:
    WEBHOOK_URL = config.get("base", "webhook_url")
    GET_METHOD = config.get("deals", "get_method")
    ADD_METHOD = config.get("deals", "add_method")
    LIST_METHOD = config.get("deals", "list_method")

    HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
    SELECT: list = []
    FILTER: dict[str: Any] = {}
    ORDER = {"DATE_CREATE": "ASC"}

    DATA = {
        "SELECT": SELECT,
        "FILTER": FILTER,
        "ORDER": ORDER,
        "start": 0,
    }

    def __init__(self, logger):
        self.logger = logger
        self.reg_num_field = BitrixDealsEnum.VAR_TO_FIELD[BitrixDealsEnum.REG_NUM]

    def upload(self, df):
        columns_to_keep = [col for col in [col.strip() for col in df.columns] if col in BitrixDealsEnum.NAME_TO_FIELD]
        df.columns = df.columns.str.strip()
        df = df[columns_to_keep]
        df = df.rename(columns=BitrixDealsEnum.NAME_TO_FIELD)
        df = df.where(pd.notna(df), None)

        records = df.to_dict('records')

        reg_nums = [rec[self.reg_num_field] for rec in records]
        reg_nums = [reg_num for reg_num in reg_nums if reg_num]
        uploaded_by_reg_num = self._get_records_by_reg_nums(reg_nums)

        records_to_upload = [rec for rec in records if rec[self.reg_num_field] not in uploaded_by_reg_num]

        for record in records_to_upload:
            self._upload_to_bitrix(record)

        self.logger.info(f'Загружено: {len(records_to_upload)} записей.')

    def _get_records_by_reg_nums(self, reg_nums):
        """Получаем рег. номера из битрикса что бы понять, что уже загружено."""

        _filter = {f'@{self.reg_num_field}': reg_nums}
        _select = [self.reg_num_field]

        self.DATA.update({
            'FILTER': _filter,
            'SELECT': _select,
        })

        records_by_reg_nums = self._get_response(self.LIST_METHOD)
        reg_nums = set([rec[self.reg_num_field] for rec in records_by_reg_nums['result']])

        self.logger.info(f'Уже загружено рег. номеров: {len(reg_nums)}')

        return reg_nums

    def _get_response(self, method):
        result = None

        try:
            response = requests.post(
                f"{self.WEBHOOK_URL}{method}",
                headers=self.HEADERS,
                data=json.dumps(self.DATA),
            )

            response.raise_for_status()
            result = response.json()

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Произошла ошибка при выполнении запроса: {e}")
        except json.JSONDecodeError:
            self.logger.error("Ошибка декодирования JSON из ответа сервера.")
        except Exception as e:
            self.logger.error(f"Произошла неизвестная ошибка: {e}")
        except Exception as e:
            raise self.logger.error(e)

        return result

    def _upload_to_bitrix(self, record):
        """Выгрузка сделки в битрикс."""

        try:
            response = requests.post(f"{self.WEBHOOK_URL}{self.ADD_METHOD}", json={"fields": record})
            response.raise_for_status()

            if response.status_code == 200:
                result = response.json()

                if "error" in result:
                    self.logger.warning("Ошибка при создании сделки:", result.get("error", "Неизвестная ошибка"))
            else:
                self.logger.error("Ошибка при отправке запроса:", response.status_code, response.text)

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Произошла ошибка при выполнении запроса: {e}")
        except json.JSONDecodeError:
            self.logger.error("Ошибка декодирования JSON из ответа сервера.")
        except Exception as e:
            self.logger.error(f"Произошла неизвестная ошибка: {e}")
        except Exception as e:
            raise self.logger.error(e)
