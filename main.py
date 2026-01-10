from unicodedata import category

from src.services import analize_cashback
from src.reports import spending_by_category
from src.views import main_page
import pandas as pd

if __name__ == "__main__":
    # result_views = main_page("2021-12-31 15:44:39")
    #
    # # print(result_views)
    #
    # result_services = analize_cashback("./data/operations.xlsx", 2018, 3)
    # print(result_services)

    df = pd.read_excel("./data/operations.xlsx", sheet_name="Отчет по операциям")
    result_report = spending_by_category(df,"Ж/д билеты", "2019-04-10")
    print(result_report)