import logging
import requests
from fastapi import BackgroundTasks
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type
from config import CURRENCY_API_URL

logger = logging.getLogger("main.currency")
class CurrencyService:
    @staticmethod
    @retry(
        stop=stop_after_attempt(3),  # Делаем максимум 3 попытки
        wait=wait_fixed(2),  # Ждем 2 секунды между попытками
        retry=retry_if_exception_type((requests.RequestException, ValueError)),
        reraise=True  # Если все попытки провалились, прокидываем ошибку дальше
    )



    def get_usd_rate() -> float:
        logger.info(f"Запрос курса валют из API: {CURRENCY_API_URL}")
        #Выполняем GET запрос
        response = requests.get(CURRENCY_API_URL)
        response.raise_for_status()

        data = response.json()

        #Разбор JSON-структуры ответа от ExchangeRate-API
        rates = data.get("rates", {})
        rub_rate = rates.get("RUB")

        if not rub_rate:
            raise ValueError("В ответе API валют отсутствует курс RUB")

        logger.info(f"Актуальный курс USD успешно получен: {rub_rate} RUB")
        return float(rub_rate)