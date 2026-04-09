import frappe

@frappe.whitelist()
def fetch_customer_credit(company,customer):
    if not customer or not company:
        frappe.response["message"] = {
            "credit" : 0,
            "outstanding":0,
        }
        
    credit_limit = frappe.db.get_value(
        "Customer Credit Limit",
        filters={"parent":customer, "company":company,"parenttype":"Customer"},
        fieldname=["credit_limit"]
    ) or 0
    
    outstanding = frappe.db.sql(
        """
        SELECT SUM(debit - credit) AS outstanding
        FROM `tabGL Entry`
        WHERE party_type = 'Customer' AND party = %(customer)s AND company = %(company)s
        """,{'customer' : customer, 'company':company}, as_dict=True
    )
    
    frappe.response["message"] = {
        "credit":credit_limit,
        "outstanding" : outstanding
    }

@frappe.whitelist()
def run_auto_review():
    frappe.enqueue(
        "my_app.tasks.auto_review_feedback",
        queue="long",
        timeout=600
    )
    return "Auto-review job queued"