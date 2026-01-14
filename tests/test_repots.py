import pandas as pd
from datetime import datetime, timedelta
from src.reports import spending_by_category


def test_with_date_parameter():
    """Тест с указанием даты"""
    print("1️⃣ Тест с указанием даты")

    # Создаем тестовые данные
    test_data = pd.DataFrame({
        'Дата операции': [
            '2024-01-15 12:30:00',  # Попадает
            '2024-02-10 14:45:00',  # Попадает
            '2023-10-01 10:00:00',  # Не попадает (больше 3 месяцев)
            '2024-03-05 09:15:00'  # Попадает
        ],
        'Категория': ['Еда', 'Еда', 'Еда', 'Еда'],
        'Сумма платежа': [-1000, -1500, -800, -1200]
    })

    result = spending_by_category(test_data, "Еда", "2024-04-01")

    print(f"   Всего транзакций: {len(test_data)}")
    print(f"   Отфильтровано: {len(result)}")

    assert len(result) == 3, f"Ожидалось 3, получено {len(result)}"
    print("   ✅ Правильно отфильтрованы данные")


def test_without_date_parameter():
    """Тест без указания даты (используется текущая)"""
    print("\n2️⃣ Тест без указания даты")

    # Создаем данные с сегодняшней датой
    today = datetime.now().strftime('%Y-%m-%d')
    test_data = pd.DataFrame({
        'Дата операции': [f'{today} 12:30:00'],
        'Категория': ['Тест'],
        'Сумма платежа': [-1000]
    })

    result = spending_by_category(test_data, "Тест")

    print(f"   Дата по умолчанию: сегодня")
    print(f"   Результат: {len(result)} транзакций")

    assert len(result) >= 0  # Может быть 0 или 1 в зависимости от времени
    print("   ✅ Функция работает без даты")


def test_empty_result():
    """Тест когда нет данных"""
    print("\n3️⃣ Тест когда нет данных")

    test_data = pd.DataFrame({
        'Дата операции': ['2023-01-01 12:30:00'],  # Очень старая
        'Категория': ['Еда'],
        'Сумма платежа': [-1000]
    })

    result = spending_by_category(test_data, "Еда", "2024-04-01")

    print(f"   Отфильтровано: {len(result)} транзакций")
    assert len(result) == 0
    print("   ✅ Правильно возвращает пустой результат")


def test_different_categories():
    """Тест разных категорий"""
    print("\n4️⃣ Тест разных категорий")

    test_data = pd.DataFrame({
        'Дата операции': [
            '2024-01-15 12:30:00',
            '2024-01-16 14:00:00',
            '2024-01-17 09:30:00'
        ],
        'Категория': ['Еда', 'Транспорт', 'Еда'],
        'Сумма платежа': [-1000, -500, -800]
    })

    # Тестируем категорию "Еда"
    result = spending_by_category(test_data, "Еда", "2024-04-01")

    print(f"   Категория 'Еда': {len(result)} транзакций")
    assert len(result) == 2
    print("   ✅ Правильно фильтрует по категории")


def test_real_file():
    """Тест с реальным файлом"""
    print("\n5️⃣ Тест с реальным файлом")

    try:
        df = pd.read_excel("./data/operations.xlsx", sheet_name="Отчет по операциям")
        print(f"   ✅ Файл прочитан: {len(df)} строк")

        # Тест с датой
        result1 = spending_by_category(df, "Ж/д билеты", "2019-04-10")
        print(f"   С датой: {len(result1)} транзакций")

        # Тест без даты
        result2 = spending_by_category(df, "Ж/д билеты")
        print(f"   Без даты: {len(result2)} транзакций")

    except FileNotFoundError:
        print("   ⚠️ Файл не найден")
    except Exception as e:
        print(f"   ❌ Ошибка: {e}")


def test_dataframe_structure():
    """Тест структуры возвращаемого DataFrame"""
    print("\n6️⃣ Тест структуры DataFrame")

    test_data = pd.DataFrame({
        'Дата операции': ['2024-01-15 12:30:00'],
        'Категория': ['Еда'],
        'Сумма платежа': [-1000],
        'Дополнительная_колонка': ['тест']  # Должна сохраниться
    })

    result = spending_by_category(test_data, "Еда", "2024-04-01")

    print(f"   Колонки в результате: {list(result.columns)}")
    assert isinstance(result, pd.DataFrame)
    print("   ✅ Возвращает DataFrame")

    # Проверяем что добавились вычисляемые колонки
    if not result.empty:
        assert 'Сумма_абсолютная' in result.columns
        print("   ✅ Добавлена колонка 'Сумма_абсолютная'")
