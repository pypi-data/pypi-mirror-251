import time
import os
import re
import asyncio
import pandas as pd
import argparse
import threading
from intel_toolkit import cve_prioritizer
from intel_toolkit import cisa_kev
from intel_toolkit import inthewild
from intel_toolkit import strobes_vi
from intel_toolkit import sploitus
from intel_toolkit import cveshield
from intel_toolkit import iris_api
from intel_toolkit import __version__
from intel_toolkit import __author__
from intel_toolkit import __license__
from intel_toolkit import nuclei_templates
from functools import cache
from rich import print
from rich.live import Live
from rich import box
from rich.table import Table

def args():
    parser = argparse.ArgumentParser(description="Insights about CVEs, with LIB Intel-Toolkit")
    parser.add_argument("-f", "--file", type=str, const=True, nargs='?', default='cves.txt', help="Define file.txt with CVE to analyse. (Default is cves.txt)")
    parser.add_argument("-o", "--file-output", type=str, const=True, nargs='?', default='output.xlsx', help="Define output spreedsheet to output. (Default is output.xlsx)")
    parser.add_argument("-k", "--key", type=str, const=True, nargs='?', help="Define KEY to API NVD.")
    parser.add_argument("-i", "--org-iris", type=int, nargs='?', default=0, const=True, help="Inform ORG client IRIS")
    parser.add_argument("-c", "--cve-shield", type=bool, nargs='?', const=True, default=False, help="CVE Shield consume and priorize")
    parser.add_argument("-v", "--version", type=bool, nargs='?', const=True, default=False, help="Show current version")
    arguments = parser.parse_args()
    return arguments

class Live_Table:
    def __init__(self, file_txt, key_nvd, org_client_iris, cve_shield) -> None:
        self.cveshield = cveshield.consult()
        if org_client_iris > 0:
            self.iris = iris_api.consult(orgID=org_client_iris)
            self.cves = self.iris.get_all_vulnerabilities()
        elif cve_shield:
            self.cves = self.cveshield.get_list_cves_trends()
        else:
            if type(file_txt) == str:
                with open(file_txt, 'r') as file:
                    self.cves = [line.rstrip() for line in file]
            elif type(file_txt) == list:
                self.cves = file_txt

        self.nuclei_templates = {}
        self.itwild = inthewild.consult()
        self.strobes = strobes_vi.consult()
        self.sploitus = sploitus.consult()
        self.cve_trends = {}
        self.cve_info = cve_prioritizer.consult(api_key_nvd=key_nvd)
        self.cisa_kev = cisa_kev.consult()
        self.total_exploitations = {}
        self.exist_patch = {}
        self.types_exploits = {}
        self.ransomwareCampaign = {}
        self.sheet_list = []

    def t_nuclei_templates(self):
        nuclei_templates.gitHandle().clone_repo()
        self.nuclei_templates = nuclei_templates.mountDataBase().list_cves_templates()

    def t_cve_shield(self):
        self.cveshield.load_cve_trending()
        for cve in self.cves:
            self.cve_trends[cve] = self.cveshield.get_audience_total_cve(cve)

    def t_exploitation(self):
        for cve in self.cves:
            self.total_exploitations[cve] = self.itwild.get_vuln_total_exploitation(cve)
    
    def t_exploits(self):
        for cve in self.cves:
            self.types_exploits[cve] = asyncio.run(self.sploitus.get_types_exploits(cve))
            
    def s_patch(self):
        for cve in self.cves:
            self.exist_patch[cve] = self.strobes.check_vuln_has_patch(cve)
    
    def t_ransomware(self):
        for cve in self.cves:
            self.ransomwareCampaign[cve] = self.cisa_kev.is_Ransomware_Campaign_Use(cve)
        # return self.ransomwareCampaign

    def get_item_exploitation(self, cve):
        return str(self.total_exploitations[f'{cve}'])
    
    def generate_spreedsheet(self, file_output):
        df = pd.DataFrame(self.sheet_list)
        df.to_excel(file_output, index=False, sheet_name="CVES_ANALYSED", header=True)

    def return_data_frame(self):
        return pd.DataFrame(self.sheet_list)
    
    @cache
    def __get_type_exploit_from_cache(self, cve, type):
        exploit = [x for x in self.types_exploits[cve] if x == type]
        if len(exploit) != 0:
            return True
        else:
            return False
    
    @cache
    def __exist_nuclei_template(self, cve):
        if self.nuclei_templates.get(cve):
            return True
        else:
            return False

    def generate_table(self) -> Table:
        self.sheet_list = []
        """Make a new table."""
        row = 1
        table = Table(title="CVE Risk-Based Patch Prioritization", box=box.DOUBLE_EDGE)
        table.add_column("Row ID")
        table.add_column("Priority")
        table.add_column("Severity")
        table.add_column("CVE")
        table.add_column("CVSS")
        table.add_column("EPSS")
        table.add_column("Status")
        table.add_column("Interest Status")
        table.add_column("Exploitation Status")
        table.add_column("Mitigation Status")
        table.add_column("Ransomware Campaign")
        table.add_column("CVE Trends")
        table.add_column("Has Nuclei Template")

        for cve in self.cve_info.PRIORITIES_LIST:
            cve_exploitation = self.get_item_exploitation(cve=cve.get('cve'))
            exploitation = ":stop_sign:"
            patch = ":skull: Unavailable"
            exploit = ':warning: Unobserved'
            owasp_top_10 = self.strobes.get_owasp_top_10(cve.get('cve')).get('owasp_2021')
            if owasp_top_10:
                owasp_top_10 = f'{owasp_top_10[0].get("id")} - {owasp_top_10[0].get("description")}'
            else:
                owasp_top_10 = ""
            
            if self.cve_trends.get(cve.get('cve')):
                audience = self.cve_trends.get(cve.get('cve'))
                twitter_cve = f":bird: Audience {audience}"
            else:
                twitter_cve = "-"

            if self.ransomwareCampaign.get(cve.get('cve')):
                ransomwareCampaign = ":locked: In use"
            else:
                ransomwareCampaign = ":unlocked: Not in use"
            
            if cve_exploitation == "0":
                exploitation = ":snowflake: Not exploited"
            if cve_exploitation == "1": 
                exploitation = ":collision: Exploited"

            if self.__exist_nuclei_template(cve.get('cve')):
                nuclei_template = ":bow_and_arrow: Finded"
            else:
                nuclei_template = ":cross_mark: Not finded"
            
            try:
                if len(self.types_exploits.get(cve.get('cve'))) == 0:
                    exploit = ':warning: Unobserved'
            except:
                exploit = ':warning: Unobserved'
            if self.types_exploits.get(cve.get('cve')):
                if self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='metasploit'): 
                    exploit = ':bomb: Productized'
                elif self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='packetstorm'):
                    exploit = ':bomb: Productized'
                elif self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='zdt'):
                    exploit = ':bomb: Productized'
                elif self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='canvas'):
                    exploit = ':bomb: Productized'
                elif self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='dsquare'):
                    exploit = ':bomb: Productized'
                elif self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='wpexploit'):
                    exploit = ':bomb: Productized'
                elif self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='githubexploit'):
                    exploit = ':lady_beetle: Code Available'
                elif self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='seebug'):
                    exploit = ':lady_beetle: Code Available'
                elif self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='zeroscience'):
                    exploit = ':lady_beetle: Code Available'
                elif self.__get_type_exploit_from_cache(cve=cve.get('cve'), type='exploitdb'):
                    exploit = ':lady_beetle: Code Available'
            try:
                if self.exist_patch.get(cve.get('cve')):
                    patch = ":hammer_and_wrench: Available"
            except:
                patch = ":skull: Unavailable"

            table.add_row(
                f'{row}',
                f"{cve.get('priority')}",
                f"{cve.get('severity')}",
                f"{cve.get('cve')}", 
                f"{cve.get('cvss_baseScore')}", 
                f"{cve.get('epss')}", 
                f"{cve.get('status')}",
                f"{exploitation}",
                f"{exploit}",
                f"{patch}",
                f"{ransomwareCampaign}",
                f"{twitter_cve}",
                f"{nuclei_template}"
            )
            line = {
                "ORDER": f'{row}',
                "PRIORITY": f"{cve.get('priority')}",
                "SEVERITY": f"{cve.get('severity')}",
                "CVE": f"{cve.get('cve')}", 
                "CVSS_SCORE": f"{cve.get('cvss_baseScore')}", 
                "EPSS": f"{cve.get('epss')}", 
                "STATUS": f"{cve.get('status')}",
                "INTEREST_STATUS": re.sub(r':\w+: ', '', f"{exploitation}"),
                "EXPLOITATION_STATUS": re.sub(r':\w+: ', '', f"{exploit}"),
                "MITIGATION_STATUS": re.sub(r':\w+: ', '', f"{patch}"),
                "RANSOMWARE_CAMPAIGN": re.sub(r':\w+: ', '', f"{ransomwareCampaign}"),
                "CVE_SHIELD": re.sub(r':\w+: ', '', f"{twitter_cve}"),
                "HAS_NUCLEI_TEMPLATE": re.sub(r':\w+: ', '', f"{nuclei_template}"),
                "OWASP_TOP_10": owasp_top_10
            }
            self.sheet_list.append(line)
            row += 1

        return table
    
    def process(self):
        self.cve_info.process_list(self.cves)

def run(file, api_key_nvd, file_output, org_iris, cve_shield):
    live_t = Live_Table(file_txt=file, key_nvd=api_key_nvd, org_client_iris=org_iris, cve_shield=cve_shield)
    t1 = threading.Thread(target=live_t.process)
    t2 = threading.Thread(target=live_t.t_ransomware)
    t3 = threading.Thread(target=live_t.t_exploitation)
    t4 = threading.Thread(target=live_t.s_patch)
    t5 = threading.Thread(target=live_t.t_exploits)
    t6 = threading.Thread(target=live_t.t_cve_shield)
    t7 = threading.Thread(target=live_t.t_nuclei_templates)

    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    t6.start()
    t7.start()

    try:
        with Live(live_t.generate_table(), refresh_per_second=4) as live:
            while True:
                time.sleep(0.4)
                live.update(live_t.generate_table())
                if threading.active_count() == 2:
                    live_t.generate_spreedsheet(file_output)
                    break
    except KeyboardInterrupt:
        print('[red]Exiting')

def cli():
    ARGS = args()
    if ARGS.version:
        print(f'Created by {__author__}\nLicense {__license__}\nVERSION {__version__}')
        exit(0)
    if ARGS.file_output:
        file_output = ARGS.file_output
    if ARGS.file:
        file = ARGS.file

    cve_shield = ARGS.cve_shield

    org_iris = ARGS.org_iris

    if os.path.exists(file):
        pass
    else:
        print(f"[red]File {file} not exist.")
        exit(1)
    if ARGS.key:
        key_nvd = ARGS.key
        run(file=file,api_key_nvd=key_nvd)
    elif os.environ.get("API_KEY_NVD"):
        key_nvd = os.environ.get("API_KEY_NVD")
        run(file=file,api_key_nvd=key_nvd, file_output=file_output, org_iris=org_iris, cve_shield=cve_shield)
    else:
        print(f'[red]API Key NVD not define. Please inform argument -k or API_KEY_NVD variable environment')

if __name__ == "__main__":
    cli()
    
    # print(Live_Table(file_txt='cves.txt', key_nvd=os.environ.get("API_KEY_NVD")).t_ransomware())