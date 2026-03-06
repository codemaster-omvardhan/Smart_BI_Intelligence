def detect_business_metrics(columns):
    revenue_keywords = ["revenue", "sales", "income"]
    cost_keywords = ["cost", "expense"]
    profit_keywords = ["profit", "margin"]
    quantity_keywords = ["quantity", "units", "volume"]
    date_keywords = ["date", "time", "orderdate"]

    detected = {}

    for col in columns:
        col_lower = col.lower()

        if any(k in col_lower for k in revenue_keywords):
            detected["revenue"] = col

        elif any(k in col_lower for k in cost_keywords):
            detected["cost"] = col

        elif any(k in col_lower for k in profit_keywords):
            detected["profit"] = col

        elif any(k in col_lower for k in quantity_keywords):
            detected["quantity"] = col

        elif any(k in col_lower for k in date_keywords):
            detected["date"] = col

    return detected