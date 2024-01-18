import json
import httpx as requests
from rich import print
from functools import cache

class consult:
    def __init__(self, orgID, file_auth='auth_iris.json') -> None:
        self.org_client = orgID
        self.all_vulnerabilities = []
        self.url_iris = 'https://iris.morphuslabs.com'

        with open(file_auth, 'r') as file:
            self.headers = json.loads(file.read()).get('headers')

    @cache
    def get_all_vulnerabilities(self):
        has_next = True
        params = {
            "format": "json",
            "organization": self.org_client,
            "page": 1
        }
        while has_next == True:
            print(f'Page: {params["page"]}')
            response = requests.get(url=f'{self.url_iris}/pt-br/api/nessus/plugins-output/vulnerabilities', params=params, headers=self.headers, timeout=120)
            r_json = response.json()
            for result in r_json.get('results'):
                if result.get('cves'):
                    for cve in result.get('cves'):
                        self.all_vulnerabilities.append(cve)

            has_next = r_json.get('has_next')
            params['page'] += 1

        self.all_vulnerabilities = list(set(self.all_vulnerabilities))
        return self.all_vulnerabilities

if __name__ == "__main__":
    iris = consult(orgID=111)
    print(iris.get_all_vulnerabilities())