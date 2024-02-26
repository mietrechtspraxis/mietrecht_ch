from . import __version__ as app_version

app_name = "mietrecht_ch"
app_title = "mietrecht-ch"
app_publisher = "mietrecht.ch"
app_description = "Backend to mietrecht.ch"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "tech-contact@mietrecht.ch"
app_license = "AGPL"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/mietrecht_ch/css/mietrecht_ch.css"
# app_include_js = "/assets/mietrecht_ch/js/mietrecht_ch.js"

# include js, css files in header of web template
# web_include_css = "/assets/mietrecht_ch/css/mietrecht_ch.css"
# web_include_js = "/assets/mietrecht_ch/js/mietrecht_ch.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "mietrecht_ch/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}
doctype_js = {
    "Heizgradtagzahlen": "common/javascript/doctype_utils.js",
    "Heizolpreise": "common/javascript/doctype_utils.js",
    "short_url": "common/javascript/doctype_utils.js",
    "kurse_und_seminare": "common/javascript/doctype_utils.js",
}


# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "mietrecht_ch.install.before_install"
# after_install = "mietrecht_ch.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "mietrecht_ch.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

scheduler_events = {
    # "cron": {
    #     "59 23 * * *": [
    #         "mietrecht_ch.tasks.ebook_cron"
    #     ]
    # },
    # "all": [
    #     "mietrecht_ch.tasks.all"
    # ],
    "daily": [
        "mietrecht_ch.tasks.daily"
    ],
    "hourly": [
        "mietrecht_ch.tasks.hourly"
    ],
    "weekly": [
        "mietrecht_ch.tasks.weekly"
    ],
    "monthly": [
        "mietrecht_ch.tasks.monthly"
    ]
}

# Testing
# -------

# before_tests = "mietrecht_ch.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "mietrecht_ch.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "mietrecht_ch.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {
        "doctype": "{doctype_4}"
    }
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#     "mietrecht_ch.auth.validate"
# ]
