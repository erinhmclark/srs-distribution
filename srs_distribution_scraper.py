""" Scrape branch and individual content from:
    https://www.srsdistribution.com/en/markets/find-a-branch/
"""
import requests
from bs4 import BeautifulSoup
import chompjs
from insert_to_gsheet import insert_from_dict

BASE_URL = 'https://www.srsdistribution.com'
# Update the sheet ID here:
SHEET_ID = ""


def get_page_soup(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_data_list(soup):
    """ Get the main JSON data from JavaScript within a <script> tag. """

    script = soup.find('a', id="gdpr_optIn").findNext('script')
    script_str = script.string.split('active: undefined,')[-1].strip()
    data = chompjs.parse_js_object(script_str)
    return data


def get_branch_details(branch):
    branch_url = f'{BASE_URL}{branch["BranchUrl"]}'
    branch_soup = get_page_soup(branch_url)
    team_list = branch_soup.find('h4', text='Meet the Team').findNext('div')\
                            .findAll('div', {'class': 'col-12 col-xs-6 col-sm-6 col-md-6 col-lg-6 col-xl-4 col-xxl-4 col-xxxl-3 mb-3'})

    for person in team_list:
        names = person.find('h6').text.split()
        first_name = ' '.join(names[0:-1])
        last_name = names[-1]
        job_role = person.find('span').text
        email_address = person.find('a')['href'].replace('mailto:', '')
        if '@' not in email_address:
            email_address = ''
        phone_number = ''
        if 'tel' in person.findAll('a')[-1]['href']:
            phone_number = person.findAll('a')[-1].text

        person_data = {
            'company_name': branch['BranchName'],
            'first_name': first_name,
            'last_name': last_name,
            'job_role': job_role,
            'email_address': email_address,
            'phone_number': phone_number,
            'street_address': branch['StreetAddr'],
            'city': branch['City'],
            'state': branch['State'],
            'zipcode': branch['ZipCd'],
            'url': branch_url
        }
        insert_from_dict(SHEET_ID, 'Sheet1', person_data, )


if __name__ == '__main__':
    find_branches_url = f'{BASE_URL}/en/markets/find-a-branch/'
    page_soup = get_page_soup(find_branches_url)
    branches_data = get_data_list(page_soup)
    for branch_item in branches_data:
        get_branch_details(branch_item)
