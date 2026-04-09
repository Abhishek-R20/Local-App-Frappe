# Copyright (c) 2026, abhishek raut and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = get_columns(), get_data(filters) or []

	
	summery = get_summery(data)
 
	data = add_total_row(data)

	return columns, data, None, None, summery


def add_total_row(data):
	total_amount = sum(row.get("total_amount", 0) for row in data)
	total_order = sum(row.get("total_orders",0) for row in data)
	
	avg_order_value = 0 
	if total_order :
		avg_order_value = total_amount/total_order
	
	data.append({
		"customer" : f"<b>{_('TOTAL')}</b>",
		# "territory" : "",
		"total_amount" : total_amount,
		"total_orders" : total_order,
		"avg_order_value" : avg_order_value,
		# "last_order_date": ""
	})
	
	return data


def get_summery(data):
	total_amount = sum(row.get("total_amount", 0) for row in data)
	total_order = sum(row.get("total_orders",0) for row in data)
	
	avg_order_value = 0 
	if total_order :
		avg_order_value = total_amount/total_order

	return [
		{
			"label":"Total Orders",
			"value" : total_order,
			"indicator" : "blue"
		},
		{
			"label":"Total Amount",
			"value" : total_amount,
			"indicator" : "yellow"
		},
		{
			"label":"Avg Order Value",
			"value" : avg_order_value,
			"indicator" : "red"
		}
	]

def get_columns():
    return[
		{"label":"Customer","fieldname":"customer","fieldtype":"Data","options":"Customer","width":180},
		{"label":"Territory","fieldname":"territory","fieldtype":"Link","options":"Territory","width":180},
		{"label":"Total Orders","fieldname":"total_orders","fieldtype":"Int","width":180},
		{"label":"Total Amount","fieldname":"total_amount","fieldtype":"Currency","width":180},
		{"label":"Avg Order Value","fieldname":"avg_order_value","fieldtype":"Currency","width":180},
		{"label":"Last Order Date","fieldname":"last_order_date","fieldtype":"Date","width":180},
	]


def get_data(filters):
	conditions = "WHERE docstatus = 1"
    
	if filters.get("from_date"):
		conditions += " AND transaction_date >= %(from_date)s"
    
	if filters.get("to_date"):
		conditions += " AND transaction_date <= %(to_date)s"
    
	if filters.get("customer"):
		conditions += " AND customer= %(customer)s"
    
	if filters.get("territory"):
		conditions += " AND territory= %(territory)s"
        
	data = frappe.db.sql(f"""
							SELECT 
								customer, 
								territory,
								COUNT(name) AS total_orders,
								SUM(grand_total) AS total_amount,
								AVG(grand_total) AS avg_order_value,
								MAX(transaction_date) AS last_order_date
							FROM `tabSales Order`
							{conditions}
							GROUP BY customer,territory
                        """, filters, as_dict=True)

	for row in data:
		if row.get("total_amount") and row["total_amount"] > 100000:
			row["color"] = "orange"
		
	return data