import frappe

@frappe.whitelist()
def get_permission_query_conditions():
    if not user:
        user = frappe.session.user
    if employee == user:
        return f"`tabExpense Claim`.employee = frappe.db.escape({user})"
        
    else:
        return ""