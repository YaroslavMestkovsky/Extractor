import configparser
import datetime
import json
import logging
import requests

from datetime import timedelta
from enums import DEALS, CONTRACTS
from models import get_session, Contract


db_confing = "bitrix.conf"
config = configparser.ConfigParser()
config.read(db_confing)


class ContractsUploader:
    """Загружает контракты в БД."""

    logging.basicConfig(
        filename="logs.txt",
        level=logging.INFO,
        encoding="utf-8",
    )

    WEBHOOK_URL = config.get("base", "webhook_url")
    LIST_METHOD = config.get("contracts", "list_method")
    URL = f"{WEBHOOK_URL}{LIST_METHOD}"

    HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}
    SELECT = []
    FILTER = {}
    ORDER = {"DATE_CREATE": "ASC"}

    DATA = {
        "SELECT": SELECT,
        "FILTER": FILTER,
        "ORDER": ORDER,
        "start": 0,
    }

    def __init__(self):
        self.session = get_session()

    def run(self):
        """Загружаем контракты по следующему алгоритму:
        1. Проверяем дату последнего загруженного в БД контракта и берем 1 день до него.
        2. Полученные данные подготавливаем для сохранения в БД.
        3. Создаем новую запись, если полученного bitrix_id уже нет в БД, иначе обновляем.
        """

        created_count = 0
        updated_count = 0

        start_date = self._get_start_date()
        self.msg(f"Начало загрузки контрактов: {start_date}.")
        self.FILTER[">DATE_CREATE"] = start_date.strftime("%Y-%m-%d")
        contracts = [] #todo здесь

        for contract in self._process_contracts():
            instance, created = self.update_or_create(defaults=contract, bitrix_id=contract['bitrix_id'])
            contracts.append(instance)

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.msg(f'Загрузка окончена.\n\tСоздано записей: {created_count}\n\tОбновлено записей: {updated_count}\n\n', need_time=False)

        self.session.add_all(contracts)
        self.session.commit()

    def _process_contracts(self):
        while True:
            response = requests.post(
                url=self.URL,
                headers=self.HEADERS,
                data=json.dumps(self.DATA),
            )

            data = response.json()

            for contract in data.get("result", []):
                yield self._relate_contract_to_model_fields(contract)

            _next = data.get("next")

            if _next:
                self.DATA["start"] = _next
            else:
                break

    def _get_start_date(self):
        last_uploaded_deal = self.session.query(Contract).order_by("date_create").with_entities(Contract.date_create).first()
        start_date = last_uploaded_deal[0] - timedelta(days=1) if last_uploaded_deal else datetime.datetime(2025, 5, 27)

        return start_date

    def update_or_create(self, defaults=None, **kwargs):
        """Аналог Django's update_or_create для SQLAlchemy.

        Аргументы:
            session: Сессия SQLAlchemy.
            defaults: Словарь значений по умолчанию для обновления или создания.
            **kwargs: Критерии поиска записи (например, name="foo", value=42).

        Возвращает:
            Кортеж: (instance, created), где instance - объект модели,
            а created - True, если объект был создан, иначе False.
        """

        instance = self.session.query(Contract).filter_by(**kwargs).first()
        defaults = defaults or {}
        created = False

        if instance:
            for key, value in defaults.items():
                setattr(instance, key, value)
        else:
            created = True
            instance = Contract(**defaults)
            self.session.add(instance)

        return instance, created

    def close_connection(self):
        self.session.close()

    @staticmethod
    def _relate_contract_to_model_fields(deal):
        """Меняем ключи на названия столбцов из таблицы БД для последующего сохранения."""
        return {value: deal.get(key) or None for key, value in CONTRACTS.items()}

    @staticmethod
    def msg(msg, need_time=True):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") if need_time else ''
        logging.info(f"{msg} {now}")

    @staticmethod
    def err(err):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logging.error(f"{err} ({now})")


if __name__ == "__main__":
    uploader = ContractsUploader()
    uploader.run()
    uploader.close_connection()
