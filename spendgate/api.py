import frappe
from frappe.query_builder import DocType
from frappe.utils import today,getdate

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

@frappe.whitelist(allow_guest = True)
def expose_expense_claim():
    doc = frappe.get_all("Expense Claim", ignore_permissions=True)
    return doc

@frappe.whitelist()
def expose_safe_expense_claim():
    docs = frappe.get_list("Expense Claim", fields=[
        '*'
    ], ignore_permissions=True)
    
    user = frappe.session.user
    roles = frappe.get_roles(user)
    user_dept = frappe.get_value("Department",filters={"department_head":user})
    
    for doc in docs:
        doc["expense_lines"] = frappe.get_list("Expense Line",{"parent":doc.name})
        if doc["department"] != user_dept:
            doc.expense_lines.pop("amount")
    return docs


@frappe.whitelist()
def get_budget_status(budget_name):
    doc = frappe.form_dict.get("budget_name")

    roles = frappe.get_roles(frappe.session.user)
    is_budget_available = frappe.db.exists("Budget", doc)

    if not is_budget_available or ("Administrator" not in roles and "SG Staff" in roles):
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
def filter_budgets(doctype, txt, searchfield, start, page_len, filters):
    filters = frappe.parse_json(filters)

    filters = filters or {}

    month = "Q" + str(((getdate(today()).month - 1 ) // 3) + 1)

    department = filters.get("department")
    if not department:
        return []
    
    data = frappe.db.sql("""
    SELECT B.name FROM `tabBudget` B WHERE B.department = %(department)s AND B.fiscal_quarter = %(quarter)s AND B.name LIKE %(txt)s ORDER BY B.name LIMIT %(start)s, %(page_len)s
    """,{
        "department":department, 
        "quarter":month, 
        "txt":f"%{txt}%",
        "start":int(start),
        "page_len":int(page_len)
        })

    return data

@frappe.whitelist()
def change_department(department_name, document_name):
    frappe.set_value("Department", document_name, "department_name", department_name)
    return {
        "department_name":department_name
    }