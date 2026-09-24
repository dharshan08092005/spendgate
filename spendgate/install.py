import frappe

def after_install():
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
        if not frappe.db.exists("Department", department):
            doc = frappe.new_doc("Department")
            doc.name = department
            doc.department_name = department
            doc.insert(ignore_permissions = True)

    for expense_category in expense_categories:
        if not frappe.db.exists("Expense Category", expense_category):
            doc = frappe.new_doc("Expense Category", )
            doc.name = expense_category
            doc.category_name = expense_category
            doc.insert(ignore_permissions = True)

    if not frappe.db.exists("Spendgate Settings", "voicepython1@gmail.com"):
        doc = frappe.get_single("Spendgate Settings")
        doc.finance_email="voicepython1@gmail.com"
        doc.low_budget_alert_threshold_percent=90
        doc.fiscal_year_start_month=1
        doc.save(ignore_permissions = True)
        frappe.db.commit()

    frappe.msgprint("Default values added to doctypes.")