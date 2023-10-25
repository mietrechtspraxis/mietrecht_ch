import frappe
from datetime import date

@frappe.whitelist(allow_guest=True)
def short_url(uri):
    
    current_day = date.today()
    
    search_data = frappe.get_all('Short URL',
        fields=[
            "redirect",
            "start_date",
            "end_date"
        ],
        filters=[
            ['uri', '=', uri],
            ['start_date', '>=', current_day],
            ['end_date', '<=', current_day]
        ],
    )
    
    return search_data