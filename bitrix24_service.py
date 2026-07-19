import logging
import requests
from config import BITRIX24_WEBHOOK_URL, BITRIX_USER_FIELD

logger = logging.getLogger("main.bitrix")

class BitrixService:
    def update_deal(deal_id: int, rate : float) -> bool:
        base_url = BITRIX24_WEBHOOK_URL.rstrip("/")
        url = f"{base_url}/crm.deal.update.json"
        # Тело запроса
        payload = {
            "id": deal_id,
            "fields": {
                BITRIX_USER_FIELD: rate
            }
        }
        logger.info(f"Отправка запроса в Битрикс24 для сделки №{deal_id} (Поле: {BITRIX_USER_FIELD}, Курс: {rate})")
        try:
            # POST запрос
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()

            result_data = response.json()

            #Проверка ответа от Битрикс24
            if result_data.get("result") == True:
                logger.info(f"Сделка №{deal_id} успешно обновлена в Битрикс24.")
                return True
            else:
                logger.error(f"Битрикс24 вернул ошибку при обновлении сделки: {result_data}")
                return False

        except requests.RequestException as ex:
            logger.error(f"Ошибка сети при запросе к Битрикс24: {e}")
            return False