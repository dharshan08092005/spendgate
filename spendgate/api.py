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
    frappe.share.add("Expense Claim", claim_name, user_email, read = 1)

# "Don't leak data" task: write a whitelisted method returning Expense Claim data in two versions — the unsafe one that returns every field (including line-item detail) to any caller, and the safe one that uses frappe.get_list (permission-aware, not frappe.get_all) and strips line-item amounts for callers outside the claimant's department

@frappe.whitelist(allow_guest = True)
def expose_expense_claim():
    doc = frappe.get_all("Expense Claim")
    return doc

@frappe.whitelist()
#yaru claim panrangalo avanga dept thavara iruka dept lam amount not show
def expose_safe_expense_claim():
    docs = frappe.get_list("Expense Claim", fileds=[
      'name, department'
    ])

    user = frappe.session.user
    roles = frappe.get_roles(user)
    user_dept = frappe.get_value("Department",filters={"department_head":user})
    
    for document in docs:
        if document["department"] != user_dept:
            doc = frappe.get_list("Expense Claim", filters={"name":document["name"]}, fields=[
              'name',
              'employee',
              'department',
              'budget',
              'expense_date',
              'description',
              'expense_lines',
              'total_amount',
              'remaining_budget_at_submission',
              'status',
              'approved_by'
            ])

@frappe.whitelist()
def get_budget_status(budget_name):
    doc = frappe.form_dict(budget_name)

    roles = frappe.get_roles(frappe.session.user)
    is_budget_available = frappe.db.exists("Budget", doc)

    if is_budget_available or "SG Staff" in roles:
        frappe.local.response["http_status_code"] = 404
        return {
          'error': 'Not found'
        }

    allocated = frappe.get_value("Budget", doc, "total_allocated")

    spent = sum(frappe.get_list("Expense Claim",{"budget":doc}, pluck="total_amount"))

    remaining = allocated - spent

    utilization_percent = (spent * 100) / allocated
    
    return {
        "allocated":allocated,
        "spent":spent,
        "remaining":remaining,
        "utilization_percent":utilization_percent
    }

@frappe.whitelist()
def change_depart(department_name, document_name):
    doc = frappe.set_value("Department", document_name, "department_name", department_name)
    frappe.commit()