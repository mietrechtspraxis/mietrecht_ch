import frappe
import re
from datetime import date
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException
import datetime 

@frappe.whitelist(allow_guest=True)
def short_url(uri):
    
    current_day = datetime.datetime.now().date()
    
    search_data = frappe.get_all('Short URL',
        fields=[
            "redirect",
            "start_date",
            "end_date"
        ],
        filters=[
            ['uri', '=', uri],
        ],
    )
    
    
    if search_data is not None and len(search_data) != 0:
        result_dict = search_data[0]
        
        start_date = result_dict.start_date
        end_date= result_dict.end_date

        if start_date <= current_day <= end_date:
            return result_dict

    return None
        
        
