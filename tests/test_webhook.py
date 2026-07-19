import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_handle_deal_webhook(monkeypatch):
    #Имитация успешного вызова внешних сервисов
    monkeypatch.setattr("main.CurrencyService.get_usd_rate", lambda _: 78.01)
    monkeypatch.setattr("main.CurrencyService.update_deal", lambda deal_id, rate: True)

    #Отправка POST-запрос с данными формы (FastAPI Form)
    payload = {
        "event": "ONCRMDEALADD",
        "data[FIELDS][ID]": 14
    }
    response = client.post("/webhook/deal-add", data=payload)
    # Проверяем, что эндпоинт отработал штатно
    assert response.status_code == 200
    assert response.json() == {"status": "success",
        "message": "Webhook received, processing started"}

if __name__ == '__main__':
    unittest.main()
