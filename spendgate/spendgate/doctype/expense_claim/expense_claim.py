# Copyright (c) 2026, SD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ExpenseClaim(Document):

	def validate(self):

		if self.department != frappe.db.get_value("Budget", self.Budget, "department"):
			frappe.throw("Department does not match with Budget")

		for row in self.expense_lines:
			if row.amount <= 0:
				frappe.throw("Amount must be greater than 0")
			else:
				self.total_amount += row.amount

	def before_submit(self):
		spent_so_far = frappe.db.sql("""
			SELECT COALESCE(SUM(total_amount), 0) FROM `tabExpense Claim`
			WHERE budget = %s AND docstatus = 1 AND name != %s
		""",(self.budget, self.name or ""))[0][0]

		budget = frappe.db.get_value("Budget",filters={"name":self.budget},fields=["total_allocated"], as_dict=True)

		if spent_so_far + self.total_amount > budget.total_allocated:
			frappe.throw(f"{self.department} budget exceeded as {spent_so_far + self.total_amount} out of {budget.total_allocated}")

	def on_submit(self):
		slef.remaining_budget_at_submission = budget.total_allocated - spent_so_far - self.total_amount
		
		if not self.approved_by:
			self.approved_by = frappe.session.user
			

	def on_trash(self):
		if self.status not in ["Cancelled","Draft"]:
			frappe.throw("Cannot delete Expense claim")
		

		

