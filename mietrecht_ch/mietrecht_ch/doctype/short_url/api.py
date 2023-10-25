import frappe
from datetime import date

@frappe.whitelist(allow_guest=True)
def short_url(uri):
    
    search_uri =  ["like", f"%{uri}%"]
    
    current_day = date.today()
    
    searchData = frappe.get_all('Short URL',
        fields={
            "redirect",
            "start_date",
            "end_date"
        },
        filters={
            current_day: ['between', ('start_date', 'end_date')]
        },
        or_filters={
            'uri': search_uri,
        }
    )
    
    return searchData