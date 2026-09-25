import frappe

def notify_finance_of_new_claim(doc_name):
    email_list = frappe.get_list("Has Role",{
        'parent_type': 'User',
        'role': 'SG Finance Manager'
    }, pluck="parent")
    
    frappe.sendmail(
        recipients=email_list,
        subject="New Expense is submitted",
        message=f"""
        <h4>New Expense record {doc_name} is submitted by {frappe.session.user}</h4>
        """,
        delayed=False
    )

def send_webhook(claim_name):
	import requests
	settings = frappe.get_single("SpendGate Settings")
	if not settings.finance_webhook_url:
		return
	doc = frappe.get_doc("Expense Claim", claim_name)
	payload = {"event": "claim_submitted", "claim": doc.name, "amount": doc.total_amount}
	try:
		r = requests.post(settings.finance_webhook_url, json=payload, timeout=5)
		r.raise_for_status()

	except Exception as e:
		frappe.log_error(f"Webhook failed: {e}", "Webhook Error")

	else:
		logger = frappe.logger("spendgate")
		logger.info(f"Request sent successfully with Payload:{payload}")

def alert_head_on_limit(department_head, budget_name):
    frappe.sendmail(
        recipients=department_head,
        subject="Budget Near Threshold limit",
        message=f"""
        <h4>{budget_name} is Exceeding the threshold!</h4>
        """,
        delayed=False
    )