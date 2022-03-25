import re
from pprint import pprint

import requests
from bs4 import BeautifulSoup

from my_exceptions import ErrorHtml


class GetJobs:
    def __init__(self):
        self.url = 'https://netologygroup.potok.io/constructor.json'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0',
            'Sec-Fetch-Site': 'same-origin',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'Sec-Fetch-Dest': 'empty',
            'cookie': 'potok_current=%7B%22src%22%3A%22%28direct%29%22%2C%22mdm%22%3A%22%28none%29%22%2C%22cmp%22%3A%22%28none%29%22%2C%22cnt%22%3A%22%28none%29%22%2C%22trm%22%3A%22%28none%29%22%2C%22knd%22%3A%22direct%22%2C%22pci%22%3Anull%7D; _hr_crm_session=5f596216b78b3fecfbc8d483070fafb6; ph_phc_Sg2bD5KGfCC1XZGc7u3Ak8SBOV8gHN012Ab8E7qYI6J_posthog=%7B%22distinct_id%22%3A%2217dbdbd2fb60-0cc7ed90ec1664-5919195f-1fa400-17dbdbd2fb73fd%22%2C%22%24device_id%22%3A%2217dbdbd2fb60-0cc7ed90ec1664-5919195f-1fa400-17dbdbd2fb73fd%22%2C%22%24initial_referrer%22%3A%22%24direct%22%2C%22%24initial_referring_domain%22%3A%22%24direct%22%2C%22%24referrer%22%3A%22%24direct%22%2C%22%24referring_domain%22%3A%22%24direct%22%2C%22%24sesid%22%3A%5B1646056359360%2C%2217f409ac490798-0690609880f795-4e607a6f-240000-17f409ac491c25%22%5D%2C%22%24session_recording_enabled%22%3Afalse%2C%22%24active_feature_flags%22%3A%5B%5D%2C%22%24enabled_feature_flags%22%3A%7B%7D%7D'
        }
        self.job_url = 'https://netologygroup.potok.io/open/jobs/'
        self.container_jobs = []

    def check_via_regex(self, string):
        pattern = r"ython"     # python
        result = re.search(pattern=pattern, string=string, flags=0)
        print(result)
        if result is not None:
            return True

    def get_data_in_json(self):
        response = requests.get(self.url, headers=self.headers)

        if response.status_code != 200:
            raise ErrorHtml

        vacancies = response.json()
        vacancies_list = vacancies['jobs']

        return vacancies_list

    def get_info(self):
        vacancies_list = self.get_data_in_json()
        for city in vacancies_list:
            info_above_jobs_list = city['departments'][0]['jobs']
            for job_info in info_above_jobs_list:
                print(job_info['id'])
                # print(job_info['name'])

                if self.check_via_regex(job_info['name']):
                    self.container_jobs.append({'url': self.job_url + str(job_info['id']),
                                                'description': job_info['name']})

        print()
        return self.container_jobs



