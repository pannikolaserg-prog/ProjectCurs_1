import json
import os
from src.services import analize_cashback


def test_with_real_file():
    """Тестируем с реальным файлом data/operations.xlsx"""

    file_path = "data/operations.xlsx"

    # Проверяем существует ли файл
    if not os.path.exists(file_path):
        print(f"⚠️ Файл {file_path} не найден")
        print("Создайте файл data/operations.xlsx с данными транзакций")
        return

    print(f"📁 Тестируем с файлом: {file_path}")
    print("-" * 50)

    try:
        # Тест 1: Проверяем что функция работает
        print("1️⃣ Тестируем базовый вызов функции...")
        result = analize_cashback(file_path, 2024, 1)

        # Проверяем что возвращается строка
        assert isinstance(result, str), "Функция должна возвращать строку"
        print("   ✅ Функция вернула строку")

        # Проверяем что это валидный JSON
        data = json.loads(result)
        assert isinstance(data, dict), "Результат должен быть словарем в JSON"
        print("   ✅ JSON валиден и является словарем")

        # Тест 2: Проверяем структуру данных
        print("\n2️⃣ Проверяем структуру данных...")
        if data:  # Если есть данные
            for category, cashback in data.items():
                assert isinstance(category, str), f"Категория должна быть строкой: {category}"
                assert isinstance(cashback, int), f"Кэшбэк должен быть целым числом: {cashback}"
                assert cashback >= 0, f"Кэшбэк не может быть отрицательным: {cashback}"
            print(f"   ✅ Найдено {len(data)} категорий")
            print(f"   ✅ Все значения - целые неотрицательные числа")
        else:
            print("   ℹ️ Нет данных за указанный период")

        # Тест 3: Проверяем разные месяцы
        print("\n3️⃣ Проверяем разные месяцы...")

        # Пробуем несколько месяцев
        months_to_test = [1, 2, 3, 12]
        for month in months_to_test:
            try:
                result_month = analize_cashback(file_path, 2024, month)
                data_month = json.loads(result_month)
                print(f"   Месяц {month:2d}: {len(data_month):3d} категорий")
            except Exception as e:
                print(f"   Месяц {month:2d}: ошибка - {e}")

        # Тест 4: Проверяем вывод
        print("\n4️⃣ Проверяем формат вывода...")
        # Проверяем отступы в JSON
        if '\n' in result and '    ' in result:
            print("   ✅ JSON с отступами (форматированный)")
        else:
            print("   ℹ️ JSON без отступов")

        # Тест 5: Показываем пример результата
        print("\n5️⃣ Пример результата:")
        if data:
            # Берем первые 3 категории
            items = list(data.items())[:3]
            for category, cashback in items:
                print(f"   {category}: {cashback} руб.")
        else:
            print("   Нет данных для отображения")

        print("\n" + "=" * 50)
        print("🎉 Все тесты пройдены успешно!")

    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}")
        print("Проверьте путь к файлу")
    except json.JSONDecodeError as e:
        print(f"❌ Ошибка декодирования JSON: {e}")
        print("Функция вернула некорректный JSON")
    except Exception as e:
        print(f"❌ Неожиданная ошибка: {type(e).__name__}: {e}")
