## mietrecht-ch

Backend to mietrecht.ch

#### License

AGPL (Waiting for final decision)

## Requirements

### CORS

Site must allow CORS from staging/prod URLs so that Angular app can make API calls to the ERPNext app. This can be configured in the `common_site_config.json` file at the root of the sites folder or in the `site_config.json` in the site folder in ERPNext.

In this file, add the value `"allow_cors": "[<allowed_url_1, <allowed_url_2>]"`

See [documentation](https://github.com/resilient-tech/frappe_docs/blob/e07382bfbfb54b6575918df55b68b72c0fedf4ba/frappe_docs/www/docs/user/en/basics/site_config.md#optional-settings)

### Update log
- Updated to 0.0.5