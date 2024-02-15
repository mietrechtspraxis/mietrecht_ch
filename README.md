## mietrecht-ch

Backend to mietrecht.ch

#### License

AGPL v3 (Waiting for final decision)

## Requirements

### CORS

Site must allow CORS from staging/prod URLs so that Angular app can make API calls to the ERPNext app. This can be configured in the `common_site_config.json` file at the root of the sites folder or in the `site_config.json` in the site folder in ERPNext.

In this file, add the value `"allow_cors": "[<allowed_url_1, <allowed_url_2>]"`

See [documentation](https://github.com/resilient-tech/frappe_docs/blob/e07382bfbfb54b6575918df55b68b72c0fedf4ba/frappe_docs/www/docs/user/en/basics/site_config.md#optional-settings)

### SCHEDULER

Site must enable scheduler in order to make cron jobs work. In frappe-bench -> sites -> `"common_site_config.json"` tweak `"pause_scheduler": 1"` to `"pause_scheduler": 0"`


### Update log
- Updated to 0.0.5
- Updated to 0.0.6: ERPNextSwiss Dependencies.
- Updated to 0.0.9: Login feature \
Developed and Reviewed by Liip until Nov 24, 2023.
- Updated to 0.1.0 (fully running on ERPNext at libracore.com)
