import frappe

@frappe.whitelist()
def get_permission_query_conditions(user = None):
    if not user:
        user = frappe.session.user

    roles = frappe.get_roles(user)

    if "SG Staff" in roles:
        return f"`tabExpense Claim`.employee = {frappe.escape(user)}"


    if "SG Department Head" in roles:
        user_dept = frappe.get_value("Department",filters={"department_head":user})
        return f"`tabExpense Claim`.department = {frappe.escape(user_dept)}"