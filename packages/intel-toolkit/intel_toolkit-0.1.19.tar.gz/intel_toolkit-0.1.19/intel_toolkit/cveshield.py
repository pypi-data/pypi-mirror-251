import json
import re
import httpx as requests
from rich import print
from functools import cache
import threading

class consult:
    def __init__(self):
        self.headers = {
            'authority': 'pirqfxayczkszwoyltgs.supabase.co',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9,pt;q=0.8',
            'accept-profile': 'public',
            'apikey': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpcnFmeGF5Y3prc3p3b3lsdGdzIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODIwODIxMzksImV4cCI6MTk5NzY1ODEzOX0.6mcYujfaOoulklwDoO39hn2mWSBO4hhZBiNki1l8E0I',
            'authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBpcnFmeGF5Y3prc3p3b3lsdGdzIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODIwODIxMzksImV4cCI6MTk5NzY1ODEzOX0.6mcYujfaOoulklwDoO39hn2mWSBO4hhZBiNki1l8E0I',
            'cache-control': 'no-cache',
            'origin': 'https://www.cveshield.com',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-client-info': 'supabase-js/2.25.0',
        }
        # self.cve_treanding_data = self.__load_cve_trending()

    @cache
    def load_cve_trending(self):
        self.cve_treanding_data = []
        try:
            r_day = requests.get(
                'https://pirqfxayczkszwoyltgs.supabase.co/rest/v1/social_media_top_20_cve_day?select=*',
                headers=self.headers, timeout=50
            ).json()
            r_week = requests.get(
                'https://pirqfxayczkszwoyltgs.supabase.co/rest/v1/social_media_top_20_cve_week?select=*',
                headers=self.headers, timeout=50
            ).json()
            r_month = requests.get(
                'https://pirqfxayczkszwoyltgs.supabase.co/rest/v1/social_media_top_20_cve_month?select=*',
                headers=self.headers, timeout=50
            ).json()
            for day in r_day:
                self.cve_treanding_data.append(day)
            for week in r_week:
                self.cve_treanding_data.append(week)
            for month in r_month:
                self.cve_treanding_data.append(month)
            with open('cve_shield.json', 'w') as file:
                file.write(json.dumps(self.cve_treanding_data, indent=4))
            return self.cve_treanding_data
        except:
            return {'error': 'Error API CVEShield'}
        
    def __check_cve_string(self, cve):
        return re.search('CVE-\d{4}-\d{4,7}', cve)
    
    @cache
    def get_all_cves_from_treanding(self):
        cves = []
        for cve in self.cve_treanding_data:
            cves.append(cve.get('cve'))
        return cves
    
    @cache
    def get_data_cve_from_treading(self, cve_id: str):
        if self.__check_cve_string(cve=cve_id):
            for cve in self.cve_treanding_data:
                if cve.get('cve') == cve_id:
                    return cve
        else:
            return None
        return None
    
    @cache
    def check_if_cve_exist_in_treading(self, cve_id: str):
        if self.__check_cve_string(cve=cve_id):
            for cve in self.cve_treanding_data:
                if cve.get('cve') == cve_id:
                    return True
        else:
            return False
        return False
    
    @cache
    def get_list_cves_trends(self):
        cves = []
        for cve in self.cve_treanding_data:
            if cve.get('cve'):
                cves.append(cve.get('cve'))
        return cves
    
    @cache
    def get_audience_total_cve(self, cve_id):
        audience = 0
        if self.__check_cve_string(cve=cve_id):
            for cve in self.cve_treanding_data:
                if cve.get('cve') == cve_id:
                    if cve.get('audience_total') > audience:
                        audience = cve.get('audience_total')
            return audience
        else:
            return None
if __name__ == "__main__":
    cve = consult()
    print(cve.get_audience_total_cve('CVE-2023-7028'))