# srs-distribution
A scraper to collect branch information from https://www.srsdistribution.com.


# Description
The scraper collects the main branch information, then iterates through each branch URL and collects the individual
data. This is then inserted into a google sheet using the [gspread](https://pypi.org/project/gspread/) module.

# Setup

## Install Requirements

- Initialise the [Poetry](https://python-poetry.org/) environment.
- In a terminal change directories into the current project.
- run `poetry init`

## Setting up Google Drive API access

There are a few steps needed to authenticate this application to insert into a Google sheet.
The first are of course to have an account and create a sheet, and the rest of the process is explained in detail 
in the [documentation](https://docs.gspread.org/en/latest/oauth2.html). 
Note that as this is a bot, the authentication method will be via Service Account.


### Quickstart

- Create a project [here](https://console.cloud.google.com/apis/dashboard).
- Enable [google drive api](https://console.cloud.google.com/marketplace/product/google/drive.googleapis.com)
- Enable [google sheets aip](https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com)
- Go to [credentials](https://console.cloud.google.com/apis/credentials) and create a service account.
- Under 'Actions' select 'manage keys' and create a key in JSON. Store the output in a file named 'google_service_account.json' in this repository. 
- Copy the service account email.
- Create Google sheet.
- Share the google sheet with the service account email.