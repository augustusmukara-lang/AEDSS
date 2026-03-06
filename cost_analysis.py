# modules/cost_analysis.py

def calculate_revenue(yield_amount, price_per_kg):
    """
    Revenue = yield_amount (kg) * price per kg
    """
    return yield_amount * price_per_kg

def calculate_profit(revenue, variable_cost, fixed_cost):
    """
    Profit = Revenue - Total Cost
    """
    total_cost = variable_cost + fixed_cost
    return revenue - total_cost