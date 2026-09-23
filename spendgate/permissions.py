import frappe

@frappe.whitelist()
def get_permission_query_conditions(user = None):
    if not user:
        user = frappe.session.user
    
        
    else:
        return ""