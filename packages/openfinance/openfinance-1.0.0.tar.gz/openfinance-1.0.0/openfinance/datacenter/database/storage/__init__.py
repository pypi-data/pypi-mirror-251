from openfinance.datacenter.database.storage.financial import (
    store_main_business,
    store_stock_holder,
    store_cash_flow,
    store_financial_report_statement,
    store_income_profit,
    store_balance_sheet,
    store_forcast_report,
    store_eps_forecast,
    store_stock_divide,
    store_money_flow
)
from openfinance.datacenter.database.storage.industry import (
    store_north_money_to_sector,
    store_industy_all_valuation
)

from openfinance.datacenter.database.storage.macro import (
    build_marco
)

from openfinance.datacenter.database.storage.market import (
    build_market
)


from openfinance.datacenter.database.storage.fred.store import (
    build_fed
)

from openfinance.datacenter.database.storage.national_data.store import (
    build_debt
)

stock_func = [
    store_main_business,
    store_stock_holder,
    store_cash_flow,
    store_financial_report_statement,
    store_income_profit,
    store_balance_sheet,
    store_forcast_report,
    store_eps_forecast,
    store_stock_divide,
    store_money_flow,
    build_marco,
    build_fed,
    build_debt,
    build_market,
    store_north_money_to_sector,
    store_industy_all_valuation
]