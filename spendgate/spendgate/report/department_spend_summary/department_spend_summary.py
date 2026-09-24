# Copyright (c) 2026, SD and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from spendgate.api import get_budget_status


def execute(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for the report. It accepts the filters as a
	dictionary and should return columns and data. It is called by the framework
	every time the report is refreshed or a filter is updated.
	"""
	columns = get_columns()
	# data = get_data()

	data = frappe.db.sql("""
					SELECT d.department_name, SUM(b.total_allocated) as Budget Allocated,
					SUM(ec.total_amount) as Spent
					FROM `tabDepartment` d
					LEFT JOIN `tabBudget` b
					ON d.department_name = b.department
					LEFT JOIN `tabExpense Claim` ec
					ON b.name = ec.budget
					GROUP BY d.department
				""")
# GROUP BY d.department because 4quarters are there, so we use SUM(b.total_allocated) to calculate total budget.


	return columns, data

def execute_snapshot_report(filters: dict | None = None):
	"""Return columns and data for the report.

	This is the main entry point for snapshot report. When 'Synced
	Report' is enabled in report, framework will call this method
	every time the report is refreshed or a filter is updated. It
	accepts the same filters as normal execute. But a utility method -
	get_latest_sync, is also imported.

	"""
	from frappe.database.duckdb.database import get_latest_sync

	columns = get_columns()
	data = get_data()

	return columns, data

def get_columns() -> list[dict]:
	"""Return columns for the report.

	One field definition per column, just like a DocType field definition.
	"""
	return [
		{
			"label": _("Department"),
			"fieldname": "department",
			"fieldtype": "Link",
			"options":"Department",
		},
		{
			"label": _("Budget Allocated"),
			"fieldname": "budget_allocated",
			"fieldtype": "Currency",
		},
		{
			"label": _("Spent"),
			"fieldname": "spent",
			"fieldtype": "Currency",
		},
		{
			"label": _("Remaining"),
			"fieldname": "remaining",
			"fieldtype": "Currency",
		},
		{
			"label": _("Utilization %"),
			"fieldname": "utilization",
			"fieldtype": "Percentage",
		},
		{
			"label": _("Claim Count"),
			"fieldname": "claim_count",
			"fieldtype": "Int",
		}
	]


def get_data() -> list[list]:
	"""Return data for the report.

	The report data is a list of rows, with each row being a list of cell values.
	"""
	# data = []
	# records = frappe.get_list("Budget")
	# for record in records:
	# 	method_data = get_budget_status(record.name)
	# 	method_data["department"] = frappe.get_value("Expense Claim",filters={'name':record.name},fields=[
	# 		'department_name'
	# 	])
	# 	data.append(method_data)

	

	return [
		[
			'Row 1',
			1
		],
		[
			'Row 2',
			2
		]
	]



# def get_budget_status(budget_name):
#     doc = frappe.form_dict(budget_name)

#     roles = frappe.get_roles(frappe.session.user)
#     is_budget_available = frappe.db.exists("Budget", doc)

#     if is_budget_available or "SG Staff" in roles:
#         frappe.local.response["http_status_code"] = 404
#         return {
#         	'error': 'Not found'
#         }

#     allocated = frappe.get_value("Budget", doc, "total_allocated")

#     spent = sum(frappe.get_list("Expense Claim",{"budget":doc}, pluck="total_amount"))

#     remaining = allocated - spent

#     utilization_percent = (spent * 100) / allocated
    
#     return {
#         "allocated":allocated,
#         "spent":spent,
#         "remaining":remaining,
#         "utilization_percent":utilization_percent
#     }