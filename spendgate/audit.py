import frappe
from frappe.utils import now

def log_change(doc, method):
    if doc.doctype == "Audit Log":
        return
    
    audit_log = frappe.new_doc("Audit Log")
    audit_log.doctype_name = doc.doctype
    audit_log.document_name = doc.name
    audit_log.action = method
    audit_log.user = frappe.session.user
    audit_log.timestamp = now()
    audit_log.insert(ignore_permissions=True)
