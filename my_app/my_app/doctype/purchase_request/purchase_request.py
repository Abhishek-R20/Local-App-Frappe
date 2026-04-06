# Copyright (c) 2026, abhishek raut and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PurchaseRequest(Document):
	pass


@frappe.whitelist()
def approve_purchase_request(docname):
    
    # 2. Fetch the document using the name passed from the client
    doc = frappe.get_doc("Purchase Request", docname)
    
    doc.status = "Approved"
    doc.save(ignore_permissions=True)

    # if doc.requested_by:
    #     frappe.sendmail(
    #         recipients=[doc.requested_by],
    #         subject=f"Purchase Request Approved",
    #         message=f"Your Purchase Request <b>{doc.name}</b> has been approved.",
    #         reference_doctype=doc.doctype,
    #         reference_name=doc.name
    #     )
    
    return "Approved"

@frappe.whitelist()
def reject_purchase_request(docname, reason):

    doc = frappe.get_doc("Purchase Request", docname)
    doc.status = "Rejected"
    
    # 2. Log the reason in the Timeline
    doc.add_comment("Comment", text=f"<b>Reason for Rejection:</b> {reason}")
    
    doc.save(ignore_permissions=True)
    
    # if doc.requested_by:
    #     frappe.sendmail(
    #         recipients=[doc.requested_by],
    #         subject=f"Purchase Request {doc.name} Rejected",
    #         message=f"Your request has been rejected. <br><b>Reason:</b> {reason}",
    #         reference_doctype=doc.doctype,
    #         reference_name=doc.name
    #     )
    
    return "Rejected"