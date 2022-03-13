from warnings import filters
import frappe
import datetime 

@frappe.whitelist(allow_guest=True)
def get_all():
    
    today = datetime.datetime.now()
    delay = datetime.timedelta(days = 3)
    threeDaysAgo = today - delay
    
    return frappe.get_all(
        'Aktualisierungsdaten', 
        fields=['index_date' ,'update_date'],
        filters = [
             ["update_date", ">=", threeDaysAgo],
        ]
    )
