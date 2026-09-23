import frappe
from frappe.query_builder import DocType

@frappe.whitelist()
def get_claims_pending_approval():
    EC = DocType("Expense Claim")
    result = (
        frappe.qb.from_(EC)
        .select(EC.name, EC.employee, EC.department, EC.total_amount, EC.expense_date)
        .where(EC.status.eq("Pending Approval"))
        .orderby(EC.expense_date.asc())
        .run(as_dict=True)
    )
    return result

@frappe.whitelist()
def share_expense_claim(claim_name, user_email):
    frappe.share.add(claim_name,user_email)