import frappe
from frappe.utils import add_days,today

def send_notifications(processed):
    try:
        admin = frappe.get_single("Admin")
        admin_email = frappe.db.get_single_value("Admin", "admin_email") or "abhishekraut695@gmail.com"
        frappe.sendmail(
        recipients=[admin_email],
        subject="Auto Review Customer Feedback Records",
        message=f"Processed {len(processed)} docs : \n" + ", ".join(processed),
        now=True,
    )
    except Exception as e:
        frappe.log_error(title="Error in email",message=frappe.get_traceback(e))
        
    


def auto_review_feedback():
    """
        Daily task: auto-review Customer Feedback records open for > 7 days.
        Should be called from hooks.py scheduler_events.
    """
    # cutoff_days = add_days(today(),-7)
    
    customer_feedbacks = frappe.get_all(
            "Customer Feedback",
            filters={
                "status" : "Open",
                # "feedback_date":["<", cutoff_days],
                "feedback_date":["<", today()],
                },
            fields=["name"]
        )
    if not customer_feedbacks:
        return
    
    processed=[]
    for f in customer_feedbacks:
        try:
            doc = frappe.get_doc("Customer Feedback", f.name)
            doc.status = "Reviewed"
            doc.add_comment("Comment","Auto Reviewd : No Action taken in 7 days")
            doc.save(ignore_permissions = True)
            processed.append(f.name)
        except Exception as e:
            frappe.log_error(title="Auto review failed", message= frappe.get_traceback(e))
            
    frappe.db.commit()
    if processed:
        send_notifications(processed)
    
    return f"{len(processed)} records processed"
        

@frappe.whitelist()
def run_auto_review():
    frappe.enqueue(
        "my_app.tasks.auto_review_feedback",
        queue="long",
        timeout=600
    )
    return "Auto-review job queued"