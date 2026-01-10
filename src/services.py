import pandas as pd
from fastjsonschema.indent import indent
from pandas.core.dtypes.common import ensure_str
from pandas.io.formats.format import return_docstring
import json

def analize_cashback(file_path: str, year: int, month: int) -> dict[str, int]:
    """
        Анализирует выгодные категории кэшбэка и возвращает json
    """
    df = pd.read_excel(file_path)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    filter_data = df[
        (df["Дата операции"].dt.year == year)
        &
        (df["Дата операции"].dt.month == month)
    ]
    filter_data = filter_data[
        df["Кэшбэк"] > 0
    ]

    filter_data = filter_data[
        df["Сумма платежа"] < 0
    ]
    expenses_by_category = filter_data.groupby('Категория')['Сумма платежа'].sum()
    cashback_by_category = abs(expenses_by_category) // 100

    result = cashback_by_category.to_dict()
    return json.dumps(result, ensure_ascii=False, indent=4)