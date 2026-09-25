# B2c — Dangerous Patterns
## The snippet below has two bugs. One is generic (you've seen its shape before). The other is specific to this app and explains exactly why SpendGate computes spend with a live aggregate query instead of a running balance field. Identify both and write the corrected version in README_internals.md
```def validate(self):
    self.total_amount = sum(r.amount for r in self.expense_lines)
    self.save()
    budget = frappe.get_doc("Budget", self.budget)
    budget.total_allocated -= self.total_amount
    budget.save()```

### `ANSWER`: 
#### self.save() saves the document during validation.
#### budget will be subtracted everytime again and again
```def validate(self):
    self.total_amount = sum(r.amount for r in self.expense_lines)
    spent_so_far = frappe.db.sql("""
			SELECT COALESCE(SUM(total_amount), 0) FROM `tabExpense Claim`
			WHERE budget = %s AND docstatus = 1 AND name != %s
		""",(self.budget, self.name or ""))[0][0]
    budget = frappe.get_doc("Budget", self.budget)
    budget.total_allocated -= self.total_amount
    budget.total_allocated -= spent_so_far
    budget.save()```

---

# B2d — The Race Condition Question
## In README_internals.md: two employees submit Expense Claims against the same Budget within the same second. Both controllers compute spent_so_far before either transaction commits. Could both submissions succeed even though, combined, they exceed the budget? Explain why or why not, and name the Frappe/MariaDB mechanism (if any) that protects against it. (One paragraph — this is a real question, not a trick; it's fine if your honest answer is "nothing currently protects against this.")

### `Answer`: Nothing currently protects against this, frappe/MariaDB does not automatically handle this scenario. Both transactions will succeed, So we should manually include a mechanism to prevent this condition.

---

# C3
## In README_internals.md: rename a test Department record. Does department on linked Budgets and Expense Claims update automatically? Why or why not?

### `ANSWER`: Yes renaming a test departement record will change departments on linked budget and expense claim.

---

# D2
## In README_internals.md: why is `frappe.get_all` dangerous in a whitelisted method exposed to low-privilege users?

### `ANSWER`: frappe.get_all bypass all role permission, exposing high level permission data to all users including low-privilege users.

---

# E1 — Complete Lifecycle
## Call self.save() inside on_update and observe what breaks. Explain it and correct the pattern in README_internals.md

### `ANSWER`: When we call self.save() inside on_update(), the save triggers on_update() and become a loop causing stack overflow or loop condition.

---

# E3 — One Performance Judgment Call frappe.db.get_value vs get_doc
## Somewhere in your controller you need just the low_budget_alert_threshold_percent value from SpendGate Settings. Which pattern would you use and why?

```doc = frappe.get_doc("SpendGate Settings", "SpendGate Settings")
threshold = doc.low_budget_alert_threshold_percent
threshold = frappe.db.get_value("SpendGate Settings", None, "low_budget_alert_threshold_percent")```

### `ANSWER`: I would use `frappe.db.get_value` because we just need the value from the settings and we are not going to modify the value as per the question, if we use `get_doc` it will get the entire document object which increase the server load.

---

# H1 — Expense Claim Form Script
## In README_internals.md: why does a frappe.call inside the validate client event not work, and why must async fetches happen in onload/refresh instead?

### `ANSWER`: 

---

# I1 — Query Report: Pending Approvals
##  In README_internals.md: show the f-string version side by side with the parameterized version, and explain why the latter is always preferred.

### `ANSWER`:
#### Parameterized version is always prefered because it prvents from sql injection.

### Parametrized version:
#### """SELECT EC.name, EC.employee, EC.department, EC.total_amount, EC.expense_date
#### FROM `tabExpense Claim` EC
#### WHERE EC.status = "Pending Approval" and EC.department = %(department)s"""

### f-Strinf version:
#### f"""SELECT EC.name, EC.employee, EC.department, EC.total_amount, EC.expense_date
#### FROM `tabExpense Claim` EC
#### WHERE EC.status = "Pending Approval" and EC.department = {department}"""

---

# J1 — Expense Claim Voucher
## In README_internals.md: explain the difference between putting a frappe.get_all() call directly inside the Jinja template versus pre-computing in before_print() and referencing doc.precomputed_field.

### `ANSWER`: Putting directly in Jinja template will store the values in cache when the HTML page is rendered. But if we calculate and send as doc.precomputed_field the correct value is calculated every time.

---

# K2 — Spot the N+1
## The snippet below has an N+1 query problem. Identify it and rewrite it:
## N+1 PROBLEM - fix this
```claims = frappe.get_all("Expense Claim", fields=["name","department"])
for c in claims:
    dept = frappe.get_doc("Department", c.department)
    print(dept.department_name, dept.department_head)```

### `ANSWER`:

---

# N1 — ignore_permissions Audit & JS-Hiding Pitfall
## Explain in README_internals.md why hiding a field in JavaScript is not a security measure.

### `ANSWER`: Hiding a field in JS is not a security measure because JS runs in User's browser, so it become acessible.

# L1 — Custom Whitelisted Method
## curl http://127.0.0.1:8000/api/resource/Expense%20Claim -H "Authorization": token 0c29be0010dbaa9:3c007325edcc55d

### Response:
```{
  "data": [
    {
      "name": "EXP-2026-00001"
    }
  ]
}```