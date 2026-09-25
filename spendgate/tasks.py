import frappe
from frappe.utils import today, getdate

def check_budget_thresholds():
    last_run = frappe.db.get_value("Audit Log",
        {"action": "budget_threshold_check", "date": today()}, "name")
    if last_run:
        return

    low_budget_alert_threshold_percent = frappe.db.get_single_value("Spendgate Settings", "low_budget_alert_threshold_percent")

    if not low_budget_alert_threshold_percent:
        low_budget_alert_threshold_percent = 90
    date = today()
    fiscal_year = getdate(date).year
    fiscal_quarter = "Q"+(((getdate(date).month - 1) // 3) + 1)
    
    budgets = frappe.db.get_list("Budget",filters={
        'fiscal_year': fiscal_year,
        'fiscal_quarter': fiscal_quarter
    }, fields={
        'name',
        'department',
        'total_allocated'
    })

    for budget in budgets:
        spent_so_far = frappe.db.sql("""
            SELECT COALESCE(SUM(total_amount), 0) FROM `tabExpense Claim`
            WHERE budget = %s AND status IN ('Approved', 'Reimbursed')
        """,(budget.name))[0][0]

        utilization_percent = (spent_so_far / budget.total_allocated) * 100

        if utilization_percent >= low_budget_alert_threshold_percent:
            dept_head = frappe.db.get_value("Department",budget.department,"department_head")
            if not dept_head:
                dept_head = "Administrator"
            
            frappe.enqueue("spendgate.notifications.alert_head_on_limit", department_head=dept_head, budget_name=budget.name)

            doc = frappe.new_doc("Audit Log")
            doc.doctype_name = "Budget"
            doc.docuent_name = budget.name
            doc.action = "budget_threshold_check"
            doc.user = frappe.session.user
            doc.timestamp = today()
            doc.insert(ignore_permissions=True)