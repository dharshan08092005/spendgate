# Copyright (c) 2026, SD and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class Budget(Document):
	def validate(self):
			if self.total_allocated <= 0:
				frappe.throw("Total Allocated amount should be greater than 0.")

			if frappe.db.exists("Budget",
				{
					"department":self.department,
					"fiscal_year":self.fiscal_year,
					"fiscal_quarter":self.fiscal_quarter
		 		}
			):
				frappe.throw("Budget Already Exists.")
