import requests
import json
import datetime


class BitrixManager:
    def __init__(self, logger):
        self.webhook_url = "https://crm.grandmed.ru/rest/27036/pnkrzq23s3h1r71c/"
        self.method = "crm.deal.list"

        self.logger = logger

    def get_response(self, _filter):
        url = f"{self.webhook_url}{self.method}"

        # Тело запроса
        data = {
            "SELECT": [],
            "FILTER": _filter,
        }

        # Отправляем POST запрос
        try:
            response = requests.post(
                url,
                headers={"Content-Type": "application/json", "Accept": "application/json"},
                data=json.dumps(data),
            )
            response.raise_for_status()  # Проверка на HTTP ошибки (например, 404, 500)
            result = response.json()
            return json.dumps(result, indent=4) # Выводим результат в удобочитаемом формате

        except requests.exceptions.RequestException as e:
            self.logger.error(f"Произошла ошибка при выполнении запроса: {e}")
        except json.JSONDecodeError:
            self.logger.error("Ошибка декодирования JSON из ответа сервера.")
        except Exception as e:
            self.logger.error(f"Произошла неизвестная ошибка: {e}")

        raise
