import logging
import sys
from fastapi import FastAPI, Request, BackgroundTasks, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from config import BITRIX_USER_FIELD
from currency_service import CurrencyService
from bitrix24_service import BitrixService

logging.basicConfig(stream=sys.stdout, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("main")
app = FastAPI(title="Bitrix24 Webhook Enricher")

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    logger.info("Получен GET-запрос на главную страницу")
    return templates.TemplateResponse(request=request, name="index.html")

def proccess_webhook_background(deal_id: int):
    #Фоновая задача для обработки сделки.
    try:
        logger.info(f"[ФОН] Начало обработки сделки №{deal_id}")
        #Запрашиваем актуальный курс доллара
        usd_rate = CurrencyService.get_usd_rate()
        #Отправляем полученный запрос обратно в Битрик24
        success = BitrixService.update_deal(deal_id, usd_rate)
        if success:
            logger.info(f"[ФОН] Сделка №{deal_id} успешно обогащена курсом {usd_rate}")
        else:
            logger.error(f"[ФОН] Не удалось обновить сделку №{deal_id}")

    except Exception as e:
        logger.error(e)

@app.post("/webhook/deal-add")
async def handle_deal_webhook(
    background_tasks: BackgroundTasks,
    event: str = Form(None),
    # Принимаем ID сделки из параметров формы Битрикс24, используя alias для парсинга структуры data[FIELDS][ID]
    data_id: int = Form(None, alias="data[FIELDS][ID]")
):
    logger.info(f"Получен вебхук от Битрикс24. Событие: {event}, ID сущности: {data_id}")
    #Проверка ID сделки
    if not data_id:
        logger.warning("Вебхук получен, но ID сделки отсутствует в данных.")
        return {"status": "error", "message": "No deal ID provided"}
    #Добавляем ресурсоемкую задачу
    background_tasks.add_task(proccess_webhook_background, data_id)
    #Отправляем успешный ответ Битрикс24, подтверждая получение хука
    return {"status": "success", "message": "Webhook received, processing started"}