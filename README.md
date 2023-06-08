# srs-distribution
A scraper to collect branch information from https://www.srsdistribution.com.


# Description
The scraper collects the main branch information, then iterates through each branch URL and collects the individual
data. This is then inserted into a google sheet using the gsheets module.

# Setup

## Install Requirements
- Initialise the [Poetry](https://python-poetry.org/) environment
- In a terminal change directories into the current project.
- run `poetry init`

## Setting up Google Drive API access
- Create a project [here](https://console.cloud.google.com/apis/dashboard).
- Enable [google drive api](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com)
- Enable [google sheets aip](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com)
- Go to [credentials](https://console.cloud.google.com/apis/credentials) and create a service account.
- Under 'Actions' select 'manage keys' and create a key in JSON. Store the output in a file named 'google_service_account.json' in this repository. 
- Copy the service account email.
- Create Google sheet.
- Share the google sheet with the service account email.