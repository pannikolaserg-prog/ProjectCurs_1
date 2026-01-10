from datetime import datetime
import pandas as pd
import requests
from mypy.util import json_loads
from numpy.f2py.crackfortran import param_eval
from openpyxl.styles.builtins import currency
from pandas import DataFrame
from typing import Dict, Any
import json

URL = "https://api.apilayer.com/currency_data/convert"
API_KEY = "PTIuLo9UJXVpm5I9Sk2K8XfVctdvRGNz"

def get_time_greeting() -> str:
    """
    Возвращает приветствие в зависимости от времени суток.

    Returns:
        Строка с приветствием
    """
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_data_time(date_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> list[str]:
    """
    Преобразует дату и возвращает начало месяца и исходную дату.

    Args:
        date_time: Строка с датой и временем
        date_format: Формат входной даты (по умолчанию "%Y-%m-%d %H:%M:%S")

    Returns:
        Список из двух строк: [начало_месяца, исходная_дата] в формате "%d.%m.%Y %H:%M:%S"
    """
    dt = datetime.strptime(date_time, date_format)

    # Начало месяца
    start_of_month = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    return [
        start_of_month.strftime("%d.%m.%Y %H:%M:%S"),
        dt.strftime("%d.%m.%Y %H:%M:%S")
    ]

def get_path_and_period(path_to_file: str, period_date: list) -> DataFrame:
    """
    Функция принимает путь к Exel файлу и список дат, и возвращает
    таблицу в заданном периоде
    """
    df = pd.read_excel(path_to_file, sheet_name="Отчет по операциям")

    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")

    filtered_df = df[
        (df["Дата операции"] >= start_date)&
        (df["Дата операции"] <= end_date)
    ]
    sorted_df = filtered_df.sort_values(by="Дата операции", ascending=True)
    return sorted_df

def get_card_with_spend(sorted_df: DataFrame) -> list[dict]:
    """
    Функция принимает DataFrame и возвращает список карт с расходами.
    """
    card_spent_transactions = []
    card_sorted = sorted_df[
        [
            "Номер карты",
            "Сумма операции",
            "Кэшбэк",
            "Сумма операции с округлением"
        ]
    ]
    for index, row in card_sorted.iterrows():
        if row["Сумма операции"] < 0:
            last_digits = str(row["Номер карты"]).replace("*", "")
            total_spent = row["Сумма операции с округлением"]
            cashback = total_spent//100
            row ={
                 "last_digits": last_digits,
                 "total_spent": total_spent,
                 "cashback": cashback
            }
            card_spent_transactions.append(row)

    return card_spent_transactions

def get_top_transactions(sorted_df: DataFrame, get_top):
    """
        Функция принимает DataFrame и возвращает get_top топ_транзакции по сумме платежа
    """
    top_pay_transactions = []
    sorted_pay_df = sorted_df.sort_values(by="Сумма операции", ascending=False)
    top_transactions = sorted_pay_df.head(get_top)
    top_transactions_sorted = top_transactions[
        [
            "Дата платежа",
            "Сумма операции",
            "Категория",
            "Описание"
        ]
    ]

    for index, row in top_transactions_sorted.iterrows():
        transaction = {
            "date": f"{row['Дата платежа']}",
            "amount": f"{row['Сумма операции']}",
            "category": f"{row['Категория']}",
            "description": f"{row['Описание']}"
        }
        top_pay_transactions.append(transaction)

    return top_pay_transactions

def get_currency(path_to_json: str) -> list[dict]:
    """
        Функция принимает на вход path_to_json и возвращает курс валют
    """
    currency_rates = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        currencies = data['user_currencies']
        for currency in currencies:
            params = {
                "amount": 1,
                "from": f"{currency}",
                "to": "RUB"
            }
            headers = {
                "apikey": f"{API_KEY}"
            }
            response = requests.request("GET", URL, headers=headers, data=params)

            status_code = response.status_code
            if status_code == 200
                result = response.status_code
                currency_code_responce = result["query"]["from"]
                currency_amount = round(result["result"], 2)
                currency_rates.append({
                    "currency": f"{currency_code_responce}",
                    "rate": f"{currency_amount}"
                })
        return currency_rates

def get_stock_prices(path_to_json: str) -> list[dict]:
    stock_rates = []
    with open(path_to_json, "r", encoding="utf-8") as file:
        data = json.load(file)
        stocks = data['user_stock']
        for stock in stocks:
            pass



