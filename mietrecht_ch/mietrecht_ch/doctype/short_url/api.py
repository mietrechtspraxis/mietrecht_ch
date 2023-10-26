import frappe
from datetime import date
from mietrecht_ch.models.exceptions.mietrechtException import BadRequestException

@frappe.whitelist(allow_guest=True)
def short_url(uri):

    if len(uri) == 0:
        raise BadRequestException('uri must be specified')
            
    from_database = frappe.get_all('Short URL',
        fields=[
            "redirect",
            "start_date",
            "end_date"
        ],
        filters=[
            ['uri', '=', uri],
        ],
    )

    if from_database is None or len(from_database) == 0:
        return None
        
    object_to_return = from_database[0]
    
    if __is_in_range__(object_to_return.start_date, object_to_return.end_date):
        return object_to_return

    return None

def __is_in_range__(start_date, end_date):
    today = date.today()
    return (start_date is None or start_date <= today ) and (end_date is None or today <= end_date)
