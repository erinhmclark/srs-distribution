""" Scrape branch and individual contact content from:
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
    """ Return a BeautifulSoup object for a given url. """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_data_list(soup):
    """ Get the main JSON data list of the branches from JavaScript within a <script> tag. """
    script = soup.find('a', id="gdpr_optIn").findNext('script')
    script_str = script.string.split('active: undefined,')[-1].strip()
    data = chompjs.parse_js_object(script_str)
    return data


def get_person_details(person):
    """ Get the details of a single person from the branch details page.  """
    names = person.find('h6').string.split()
    first_name = ' '.join(names[0:-1])
    last_name = names[-1]
    job_role = person.find('span').string
    email_address = person.find('a')['href'].replace('mailto:', '')
    email_address = email_address if '@' in email_address else ''
    phone_number_obj = person.find_all('a')[-1]
    phone_number = phone_number_obj.string if 'tel' in phone_number_obj['href'] else ''

    person_details = {
        'first_name': first_name,
        'last_name': last_name,
        'job_role': job_role,
        'email_address': email_address,
        'phone_number': phone_number
    }
    return person_details


def get_team_details(soup):
    """ Extract information for a branch. """
    team_list = soup.find('h4', string='Meet the Team').find_next('div').find_all('div',
                    {'class': 'col-12 col-xs-6 col-sm-6 col-md-6 col-lg-6 col-xl-4 col-xxl-4 col-xxxl-3 mb-3'})
    return team_list


def scrape_branch(branch):
    branch_url = f'{BASE_URL}{branch["BranchUrl"]}'
    branch_soup = get_page_soup(branch_url)
    team_list = get_team_details(branch_soup)

    company = {'company_name': branch['BranchName']}
    branch_data = {
        'street_address': branch['StreetAddr'],
        'city': branch['City'],
        'state': branch['State'],
        'zipcode': branch['ZipCd'],
        'url': branch_url
    }
    for person in team_list:
        person_data = get_person_details(person)
        # This ensures the correct order for the Google sheet:
        final_dict = {**company, **person_data, **branch_data}
        insert_from_dict(SHEET_ID, 'Sheet1', final_dict)


if __name__ == '__main__':
    find_branches_url = f'{BASE_URL}/en/markets/find-a-branch/'
    page_soup = get_page_soup(find_branches_url)
    branches_data = get_data_list(page_soup)
    for branch in branches_data:
        scrape_branch(branch)
