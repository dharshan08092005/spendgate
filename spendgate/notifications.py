import frappe

def notify_finance_of_new_claim(doc_name):

    email_list = frappe.get_list("Has Role",{"parent_type":"User", "role":"SG Finance Manager"}, pluck="parent")
    
    frappe.sendmail(
        receipients=email_list,
        subject="New Expense is submitted",
        message=f"""
        <h4>New Expense record {doc_name} is submitted by {frappe.session.user}<h4>
        """,
        delayed=False
    )