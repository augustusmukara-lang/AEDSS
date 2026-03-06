from flask import Flask, request
from modules.database import create_tables
from modules.farmer import add_farmer, view_farmers, delete_farmer
from modules.cost_analysis import calculate_revenue, calculate_profit
from modules.risk_analysis import simulate_price_change, simulate_yield_change
from modules.policy_analysis import apply_subsidy, apply_tax
from modules.reporting import print_farmer_report
import pandas as pd  # for Excel export

app = Flask(__name__)

# Create database tables if they don't exist
create_tables()

# -----------------------
# HOME PAGE
# -----------------------
@app.route("/")
def home():
    return """
    <h1>AEDSS - Agricultural Economic Decision Support System</h1>
    <ul>
        <li><a href="/add_farmer">Add Farmer</a></li>
        <li><a href="/view_farmers">View Farmers</a></li>
        <li><a href="/analyze_farmer">Analyze Farmer</a></li>
        <li><a href="/export_farmers">Export Farmers to Excel</a></li>
        <li><a href="/export_analysis">Export Analysis to Excel</a></li>
    </ul>
    """

# -----------------------
# ADD FARMER
# -----------------------
@app.route("/add_farmer", methods=["GET", "POST"])
def add_farmer_page():
    if request.method == "POST":
        name = request.form.get("name")
        gender = request.form.get("gender")
        crop = request.form.get("crop")
        farm_size = float(request.form.get("farm_size"))
        variable_cost = float(request.form.get("variable_cost"))
        fixed_cost = float(request.form.get("fixed_cost"))
        yield_amount = float(request.form.get("yield_amount"))
        price = float(request.form.get("price"))

        add_farmer(name, gender, crop, farm_size, variable_cost, fixed_cost, yield_amount, price)
        return f"<h3>Farmer {name} added successfully!</h3><a href='/'>Home</a>"

    return """
    <h2>Add Farmer</h2>
    <form method="POST">
        <label>Name:</label><br>
        <input type="text" name="name" required><br><br>
        <label>Gender:</label><br>
        <input type="text" name="gender" required><br><br>
        <label>Crop:</label><br>
        <input type="text" name="crop" required><br><br>
        <label>Farm Size (acres):</label><br>
        <input type="number" name="farm_size" step="0.01" required><br><br>
        <label>Variable Cost:</label><br>
        <input type="number" name="variable_cost" step="0.01" required><br><br>
        <label>Fixed Cost:</label><br>
        <input type="number" name="fixed_cost" step="0.01" required><br><br>
        <label>Yield (kg):</label><br>
        <input type="number" name="yield_amount" step="0.01" required><br><br>
        <label>Price (per kg):</label><br>
        <input type="number" name="price" step="0.01" required><br><br>
        <input type="submit" value="Add Farmer">
    </form>
    <a href='/'>Home</a>
    """

# -----------------------
# VIEW FARMERS
# -----------------------
@app.route("/view_farmers")
def view_farmers_page():
    farmers = view_farmers()
    html = "<h2>Farmers List</h2>"
    if farmers:
        html += "<ul>"
        for f in farmers:
            html += f"<li>{f['name']} - {f['crop']} - <a href='/delete_farmer/{f['id']}'>Delete</a></li>"
        html += "</ul>"
    else:
        html += "<p>No farmers found</p>"
    html += "<br><a href='/'>Home</a>"
    return html

# -----------------------
# DELETE FARMER
# -----------------------
@app.route("/delete_farmer/<int:farmer_id>")
def delete_farmer_page(farmer_id):
    delete_farmer(farmer_id)
    return "<h3>Farmer deleted successfully</h3><a href='/view_farmers'>Back</a>"

# -----------------------
# ANALYZE FARMER
# -----------------------
@app.route("/analyze_farmer", methods=["GET", "POST"])
def analyze_farmer():
    farmers = view_farmers()
    if request.method == "POST":
        farmer_id = int(request.form.get("farmer_id"))
        selected = next((f for f in farmers if f["id"] == farmer_id), None)
        if not selected:
            return "<h3>Farmer not found</h3><a href='/analyze_farmer'>Back</a>"

        # Cost analysis
        revenue = calculate_revenue(selected["yield_amount"], selected["price"])
        profit = calculate_profit(revenue, selected["variable_cost"], selected["fixed_cost"])

        # Risk simulation
        risk_revenue = simulate_price_change(revenue)
        risk_profit = simulate_yield_change(profit)

        # Policy simulation
        total_cost = selected["variable_cost"] + selected["fixed_cost"]
        subsidy_cost = apply_subsidy(total_cost, 5)
        tax_cost = apply_tax(total_cost, 5)

        # Farmer report
        report = print_farmer_report(selected)

        return f"""
        <h2>Farmer Analysis</h2>
        <h3>Cost Analysis</h3>
        Revenue: {revenue}<br>
        Profit: {profit}<br>
        <h3>Risk Simulation</h3>
        Revenue after risk: {risk_revenue}<br>
        Profit after risk: {risk_profit}<br>
        <h3>Policy Simulation</h3>
        Cost after 5% subsidy: {subsidy_cost}<br>
        Cost after 5% tax: {tax_cost}<br>
        <h3>Farmer Report</h3>
        <pre>{report}</pre>
        <br><a href="/">Home</a>
        """

    html = "<h2>Select Farmer</h2>"
    if farmers:
        html += "<form method='POST'>"
        html += "<select name='farmer_id'>"
        for f in farmers:
            html += f"<option value='{f['id']}'>{f['name']} - {f['crop']}</option>"
        html += "</select><br><br>"
        html += "<input type='submit' value='Analyze'>"
        html += "</form>"
    else:
        html += "<p>No farmers available</p>"
    html += "<br><a href='/'>Home</a>"
    return html

# -----------------------
# EXPORT FARMERS TO EXCEL
# -----------------------
@app.route("/export_farmers")
def export_farmers_page():
    farmers = view_farmers()
    if not farmers:
        return "<h3>No farmers to export</h3><a href='/'>Home</a>"
    df = pd.DataFrame(farmers)
    df.to_excel("farmers.xlsx", index=False)
    return "<h3>Farmers exported to farmers.xlsx</h3><a href='/'>Home</a>"

# -----------------------
# EXPORT ANALYSIS TO EXCEL
# -----------------------
@app.route("/export_analysis")
def export_analysis_page():
    farmers = view_farmers()
    if not farmers:
        return "<h3>No farmers to export</h3><a href='/'>Home</a>"

    data = []
    for f in farmers:
        revenue = calculate_revenue(f["yield_amount"], f["price"])
        profit = calculate_profit(revenue, f["variable_cost"], f["fixed_cost"])
        risk_revenue = simulate_price_change(revenue)
        risk_profit = simulate_yield_change(profit)
        total_cost = f["variable_cost"] + f["fixed_cost"]
        subsidy_cost = apply_subsidy(total_cost, 5)
        tax_cost = apply_tax(total_cost, 5)
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
    df.to_excel("farmer_analysis.xlsx", index=False)
    return "<h3>Analysis exported to farmer_analysis.xlsx</h3><a href='/'>Home</a>"

# -----------------------
# RUN SERVER
# -----------------------
if __name__ == "__main__":
    app.run(debug=True)