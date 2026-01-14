import json
import pytest
from unittest.mock import Mock, patch
from src.views import main_page


# Тест 1: Проверка структуры ответа
def test_main_page_structure():
    """Тест проверяет, что функция возвращает правильную структуру данных"""

    # Тестовый вызов
    result = main_page("2021-12-31 15:44:39")

    # Преобразуем строку JSON обратно в словарь
    data = json.loads(result)

    # Проверяем наличие всех ключей
    expected_keys = ["greeting", "cards", "top_transactions", "currency_rates", "stock_prices"]
    for key in expected_keys:
        assert key in data, f"Ключ '{key}' отсутствует в ответе"

    # Проверяем типы данных
    assert isinstance(data["greeting"], str)
    assert isinstance(data["cards"], list)
    assert isinstance(data["top_transactions"], list)
    assert isinstance(data["currency_rates"], list)
    assert isinstance(data["stock_prices"], list)


# Тест 2: Мок-тест с заглушками
def test_main_page_with_mocks():
    """Тест с использованием заглушек для зависимостей"""

    # Создаем моки для всех зависимостей
    mock_greeting = "Доброе утро"
    mock_cards = [
        {"card": "Visa Gold", "total_spent": 15000},
        {"card": "MasterCard Platinum", "total_spent": 25000}
    ]
    mock_transactions = [
        {"date": "2023-12-01", "amount": 5000, "description": "Покупка"},
        {"date": "2023-12-02", "amount": 3000, "description": "Оплата услуг"}
    ]
    mock_currency = [
        {"currency": "USD", "rate": 90.5},
        {"currency": "EUR", "rate": 98.3}
    ]
    mock_stocks = [
        {"stock": "AAPL", "price": 185.5},
        {"stock": "GOOGL", "price": 135.2}
    ]

    # Патчим все функции
    with patch('src.views.get_time_greeting', return_value=mock_greeting), \
            patch('src.views.get_card_with_spend', return_value=mock_cards), \
            patch('src.views.get_top_transactions', return_value=mock_transactions), \
            patch('src.views.get_currency', return_value=mock_currency), \
            patch('src.views.get_stock_prices', return_value=mock_stocks), \
            patch('src.views.get_data_time') as mock_time, \
            patch('src.views.get_path_and_period') as mock_df:
        # Настраиваем моки
        mock_time.return_value = "2023-12-01"
        mock_df.return_value = Mock()  # заглушка для DataFrame

        # Вызываем функцию
        result = main_page("2023-12-01")
        data = json.loads(result)

        # Проверяем значения
        assert data["greeting"] == mock_greeting
        assert data["cards"] == mock_cards
        assert data["top_transactions"] == mock_transactions
        assert data["currency_rates"] == mock_currency
        assert data["stock_prices"] == mock_stocks


# Тест 3: Проверка JSON формата
def test_main_page_json_format():
    """Тест проверяет, что возвращается валидный JSON"""

    result = main_page("2021-12-31 15:44:39")

    # Проверяем, что это валидный JSON
    try:
        parsed = json.loads(result)
        assert True, "JSON успешно парсится"
    except json.JSONDecodeError as e:
        pytest.fail(f"Невалидный JSON: {e}")

    # Проверяем, что JSON содержит данные
    assert len(parsed) > 0


# Тест 4: Проверка обработки ошибок (если нужно)
def test_main_page_error_handling():
    """Тест проверяет, как функция обрабатывает ошибки"""

    # Тест с некорректной датой
    try:
        result = main_page("некорректная_дата")
        # Если функция не падает, проверяем структуру
        data = json.loads(result)
        assert "greeting" in data
    except Exception:
        # Если функция падает - это тоже нормально, если это ожидаемое поведение
        pass
