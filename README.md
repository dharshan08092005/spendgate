### spendgate

a custom Frappe app for department budget tracking & expense consumption

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch version-16
bench install-app spendgate
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/spendgate
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade
### CI

This app can use GitHub Actions for CI. The following workflows are configured:

- CI: Installs this app and runs unit tests on every push to `develop` branch.
- Linters: Runs [Frappe Semgrep Rules](https://github.com/frappe/semgrep-rules) and [pip-audit](https://pypi.org/project/pip-audit/) on every pull request.


### License

mit

# B2d — The Race Condition Question
## In README_internals.md: two employees submit Expense Claims against the same Budget within the same second. Both controllers compute spent_so_far before either transaction commits. Could both submissions succeed even though, combined, they exceed the budget? Explain why or why not, and name the Frappe/MariaDB mechanism (if any) that protects against it. (One paragraph — this is a real question, not a trick; it's fine if your honest answer is "nothing currently protects against this.")

### `Answer`: Nothing currently protects against this, frappe/MariaDB does not automatically handle this scenario. Both transactions will succeed, So we should manually include a mechanism to prevent this condition.

# B2c — Dangerous Patterns
## The snippet below has two bugs. One is generic (you've seen its shape before). The other is specific to this app and explains exactly why SpendGate computes spend with a live aggregate query instead of a running balance field. Identify both and write the corrected version in README_internals.md
`def validate(self):
    self.total_amount = sum(r.amount for r in self.expense_lines)
    self.save()
    budget = frappe.get_doc("Budget", self.budget)
    budget.total_allocated -= self.total_amount
    budget.save()

### `ANSWER`: 
#### self.save() saves the document during validation.
#### budget will be subtracted everytime again and again
def validate(self):
    self.total_amount = sum(r.amount for r in self.expense_lines)
    spent_so_far = frappe.db.sql("""
			SELECT COALESCE(SUM(total_amount), 0) FROM `tabExpense Claim`
			WHERE budget = %s AND docstatus = 1 AND name != %s
		""",(self.budget, self.name or ""))[0][0]
    budget = frappe.get_doc("Budget", self.budget)
    budget.total_allocated -= self.total_amount
    budget.total_allocated -= spent_so_far
    budget.save()

# C3
## In README_internals.md: rename a test Department record. Does department on linked Budgets and Expense Claims update automatically? Why or why not?
### `ANSWER`: Yes renaming a test departement record will change departments on linked budget and expense claim.

# D2
## In README_internals.md: why is `frappe.get_all` dangerous in a whitelisted method exposed to low-privilege users?
### `ANSWER`: frappe.get_all bypass all role permission, exposing high level permission data to all users including low-privilege users.