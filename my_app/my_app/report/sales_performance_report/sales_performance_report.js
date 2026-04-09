// Copyright (c) 2026, abhishek raut and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Performance Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label":"From Date",
			"fieldtype":"Date",
			"reqd":1,
		},
		{
			"fieldname": "to_date",
			"label":"To Date",
			"fieldtype":"Date",
			"reqd":1,
		},
		{
			"fieldname": "customer",
			"label":"Customer",
			"fieldtype":"Link",
			"options" : "Customer"
		},
		{
			"fieldname": "territory",
			"label":"Territory",
			"fieldtype":"Link",
			// "reqd":1,
			"options" :"Territory",
		},
		

	],
};
