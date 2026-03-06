# modules/policy_analysis.py

def apply_subsidy(total_cost, percent_subsidy):
    """
    Apply a subsidy to the total cost.
    percent_subsidy: percentage of cost to reduce (e.g., 5 for 5%)
    Returns the cost after subsidy.
    """
    return total_cost * (1 - percent_subsidy / 100)

def apply_tax(total_cost, percent_tax):
    """
    Apply a tax to the total cost.
    percent_tax: percentage of cost to increase (e.g., 5 for 5%)
    Returns the cost after tax.
    """
    return total_cost * (1 + percent_tax / 100)