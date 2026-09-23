import frappe

def after_istall():
    departments = [
        'Travel',
        'Software & Equipment',
        'Client Entertainment',
        'Training'
    ]
    expense_categories = [
        'Travel',
        'Software & Equipment',
        'Client Entertainment',
        'Training'
    ]
    
    for department in departments:
        if not frappe.exists("Department", department):
            doc = frappe.get_doc("Department", department, ignore_permissions = True)
            doc.insert()

    for expense_category in expense_categories:
        if not frappe.exists("Expense Category", expense_category):
            doc = frappe.get_doc("Expense Category", expense_category, ignore_permissions = True)
            doc.insert()

    if not frappe.exists("Spendgate Settings"):
        doc = frappe.get_doc("Spendgate Settings", finance_email="voicepython1@gmail.com", low_budget_alert_threshold_percent=90, fiscal_year_start_month=1)
        doc.insert()

    frappe.msgprint("Default values added to doctypes.")