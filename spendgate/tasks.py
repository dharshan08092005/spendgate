import frappe
from frapppe.utils import today

def check_budget_thresholds():
    last_run = frappe.db.get_value("Audit Log",
        {"action": "budget_threshold_check", "date": today()}, "name")
    if last_run:
        return



    # spent_so_far = frappe.db.sql("""
    #     SELECT COALESCE(SUM(total_amount), 0) FROM `tabExpense Claim`
    #     WHERE status = %s AND docstatus = 1
    # """,("Approved"))[0][0]
    
    # budget = frappe.db.get_value("Budget",filters={"name":budget},fields=["total_allocated"], as_dict=True)

    # if spent_so_far + total_amount > budget.total_allocated:
    #     frappe.throw(f"{department} budget exceeded as {spent_so_far + total_amount} out of {budget.total_allocated}")

    