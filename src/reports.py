import pandas as pd
from datetime import datetime, timedelta
from typing import Optional


def spending_by_category(
        transactions: pd.DataFrame,
        category: str,
        date: Optional[str] = None
) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.

    Args:
        transactions: DataFrame с транзакциями
        category: Название категории для анализа
        date: Дата в формате 'YYYY-MM-DD'. Если None - текущая дата.

    Returns:
        DataFrame с отфильтрованными транзакциями за последние 3 месяца.
    """
    try:
        # Если дата не указана, берем текущую
        if date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(date, '%Y-%m-%d')

        # Вычисляем дату 3 месяца назад
        start_date = end_date - timedelta(days=90)

        # Проверяем необходимые колонки
        required_columns = ['Дата операции', 'Категория', 'Сумма платежа']
        missing = [col for col in required_columns if col not in transactions.columns]

        if missing:
            raise ValueError(f"Отсутствуют колонки: {missing}")

        # Преобразуем дату в транзакциях
        transactions['Дата операции'] = pd.to_datetime(
            transactions['Дата операции'],
            errors='coerce'
        )

        # Фильтруем данные
        filtered = transactions[
            (transactions['Дата операции'] >= start_date) &
            (transactions['Дата операции'] <= end_date) &
            (transactions['Категория'] == category) &
            (transactions['Сумма платежа'] < 0)  # Только траты
            ].copy()

        # Добавляем вычисляемые колонки
        if not filtered.empty:
            filtered['Сумма_абсолютная'] = abs(filtered['Сумма платежа'])
            filtered['День_недели'] = filtered['Дата операции'].dt.day_name()
            filtered['Месяц'] = filtered['Дата операции'].dt.month

        # Возвращаем результат
        return filtered.reset_index(drop=True)

    except Exception as e:
        # В случае ошибки возвращаем пустой DataFrame с информацией
        error_df = pd.DataFrame({'Ошибка': [str(e)]})
        return error_df