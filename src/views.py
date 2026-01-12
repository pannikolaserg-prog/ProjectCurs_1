import json
from typing import Dict, Any
from src.utils import (
    get_time_greeting,
    get_data_time,
    get_path_and_period,
    get_card_with_spend,
    get_top_transactions,
    get_currency,
    get_stock_prices
)

def main_page(data_time: str) -> dict[str, any]:

    # Делаем срез всего файла Excel на определенный диапазон
    time_period = get_data_time(data_time)
    sorted_df = get_path_and_period("./data/operations.xlsx", time_period)

    # 1. Приветствие
    greeting = get_time_greeting()

    # 2. По каждой карте
    cards = get_card_with_spend(sorted_df)

    # 3. Топ-5 транзакций по сумме платежа.
    top_transactions = get_top_transactions(sorted_df, 5)

    # 4. Курс валют
    currency_rates = get_currency("./data/user_settings.json")

    # 5. Стоимость акций из S&P500.
    stock_prices = get_stock_prices("./data/user_settings.json")


    data = {
            "greeting": greeting,
            "cards": cards,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices
    }
    json_data = json.dumps(data, ensure_ascii=False, indent=4)

    return json_data
