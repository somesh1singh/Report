import pandas as pd
import numpy as np
from stock_report_agent import StockReportAgent


def test_format_number():
    a = StockReportAgent(output_dir="tmp")
    assert a._format_number(123) == "123.0"
    assert a._format_number(1500) == "1.5K"
    assert a._format_number(1_500_000) == "1.5M"
    assert a._format_number(0) == "-"
    assert a._format_number(np.nan) == "-"


def test_safe_get_and_balance_sheet_rows():
    df = pd.DataFrame(
        {
            '2020': [1000, 200, 50],
            '2021': [1100, 210, 60]
        },
        index=['Total Assets', 'Total Debt', 'Stockholders Equity']
    )
    a = StockReportAgent(output_dir="tmp")
    # existing row
    assert a._safe_get(df, 'Total Assets', 0) == 1000
    # missing row returns default
    assert a._safe_get(df, 'Nonexistent', 0, default=999) == 999
    # column index out-of-range returns default
    assert a._safe_get(df, 'Total Assets', 10, default=42) == 42
