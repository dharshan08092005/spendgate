import frappe

@frappe.whitelist()
def get_permission_query_conditions(user = None):
    if not user:
        user = frappe.session.user

    roles = frappe.get_roles(user)

    if user == "Administrator" or "SG Finance Manager" in roles:
        return ""

    if "SG Staff" in roles:
        return f"`tabExpense Claim`.employee = {frappe.db.escape(user)}"


    if "SG Department Head" in roles:
        user_dept = frappe.get_value("Department",{"department_head":user},"name")
        return f"`tabExpense Claim`.department = {frappe.db.escape(user_dept)}"