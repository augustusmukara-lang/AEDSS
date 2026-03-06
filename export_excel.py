import pandas as pd
from modules.cost_analysis import calculate_revenue, calculate_profit
from modules.risk_analysis import simulate_price_change, simulate_yield_change
from modules.policy_analysis import apply_subsidy, apply_tax

# -----------------------
# EXPORT RAW FARMERS TO EXCEL
# -----------------------
def export_farmers_to_excel(farmers, filename="farmers.xlsx"):
    """
    Export raw farmer data to Excel.
    """
    if not farmers:
        return "No farmers to export"

    df = pd.DataFrame(farmers)
    df.to_excel(filename, index=False)
    return f"Farmers exported to {filename} successfully"

# -----------------------
# EXPORT FULL ANALYSIS TO EXCEL
# -----------------------
def export_analysis_to_excel(farmers, filename="farmer_analysis.xlsx"):
    """
    Export full analysis (cost, profit, risk, policy) for each farmer to Excel.
    """
    if not farmers:
        return "No farmers to export"

    data = []
    for f in farmers:
        # Cost analysis
        revenue = calculate_revenue(f["yield_amount"], f["price"])
        profit = calculate_profit(revenue, f["variable_cost"], f["fixed_cost"])

        # Risk simulation
        risk_revenue = simulate_price_change(revenue)
        risk_profit = simulate_yield_change(profit)

        # Policy simulation
        total_cost = f["variable_cost"] + f["fixed_cost"]
        subsidy_cost = apply_subsidy(total_cost, 5)  # 5% subsidy
        tax_cost = apply_tax(total_cost, 5)          # 5% tax

        data.append({
            "Name": f["name"],
            "Gender": f["gender"],
            "Crop": f["crop"],
            "Farm Size (acres)": f["farm_size"],
            "Variable Cost": f["variable_cost"],
            "Fixed Cost": f["fixed_cost"],
            "Yield (kg)": f["yield_amount"],
            "Price per kg": f["price"],
            "Revenue": revenue,
            "Profit": profit,
            "Risk Revenue": risk_revenue,
            "Risk Profit": risk_profit,
            "Cost after Subsidy": subsidy_cost,
            "Cost after Tax": tax_cost
        })

    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return f"Analysis exported to {filename} successfully"