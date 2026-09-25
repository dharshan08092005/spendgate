# Copyright (c) 2026, SD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
class ExpenseClaim(Document):

	def validate(self):

		if self.department != frappe.db.get_value("Budget", self.budget, "department"):
			frappe.throw("Department does not match with Budget")

		self.total_amount = 0

		for row in self.expense_lines:
			if row.amount <= 0:
				frappe.throw("Amount must be greater than 0")
			else:
				self.total_amount += row.amount

	def before_submit(self):
		self.spent_so_far = frappe.db.sql("""
			SELECT COALESCE(SUM(total_amount), 0) FROM `tabExpense Claim`
			WHERE budget = %s AND docstatus = 1 AND name != %s
		""",(self.budget, self.name or ""))[0][0]

		total_allocated = frappe.db.get_value("Budget",self.budget,'total_allocated')

		if self.spent_so_far + self.total_amount > total_allocated:
			frappe.throw(f"{self.department} budget exceeded as {self.spent_so_far + self.total_amount} out of {total_allocated}")

	def on_submit(self):
		total_allocated = frappe.db.get_value("Budget",self.budget,'total_allocated')
		self.remaining_budget_at_submission = total_allocated - self.spent_so_far - self.total_amount

		frappe.enqueue("spendgate.notifications.notify_finance_of_new_claim",doc_name = self.name)
		frappe.enqueue("spendgate.notificatins.send_webhook",doc_name = self.name)

	def on_cancel(self):
		if self.status == "Reimbursed":
			frappe.throw("Cannot Cancel - money has already left the building, and a cancel here would silently corrupt the books.")
		
		self.status = "Cancelled"
			
	def on_trash(self):
		if self.status not in [
			'Cancelled',
			'Draft'
		]:
			frappe.throw("Cannot delete Expense claim not in Cancelled or Draft.")

	# def on_update(self):
	# 	self.save()

	def before_print(self, print_settings=None):
		self.print_summary = f"{self.employee} - {self.department} - {self.expense_date}"


def reassign_department_claims(from_dept, to_dept):
	values = {"from_department":from_dept, "to_department":to_dept}
	try:
		data = frappe.db.sql("""
		UPDATE `tabExpense Claim` EC set EC.department = %(to_departmnt)s
		WHERE EC.department = %(from_department)s and EC.status = "Draft"
		""",values=values, as_dict=0)

		frappe.db.commit()

	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(e)


		
