# modules/reporting.py

def print_farmer_report(farmer):
    """
    Returns a string report for a single farmer.
    Includes: Name, Gender, Crop, Farm Size, Costs, Yield, Price
    """
    report = f"""
    Farmer Report
    ------------------------
    Name       : {farmer.get('name')}
    Gender     : {farmer.get('gender')}
    Crop       : {farmer.get('crop')}
    Farm Size  : {farmer.get('farm_size')} acres
    Variable Cost : {farmer.get('variable_cost')}
    Fixed Cost    : {farmer.get('fixed_cost')}
    Yield         : {farmer.get('yield_amount')} kg
    Price         : {farmer.get('price')} per kg
    ------------------------
    """
    return report