from datetime import datetime

def calculate_total_price(price_per_night: float, quantity: int, start_date, end_date):
    days = (end_date - start_date).days
    return price_per_night * quantity * days
