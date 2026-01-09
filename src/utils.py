from datetime import datetime
from pandas import DataFrame

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
