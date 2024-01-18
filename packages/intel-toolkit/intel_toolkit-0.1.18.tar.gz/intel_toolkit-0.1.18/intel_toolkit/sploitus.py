import re, asyncio, json
import httpx
from rich import print
from functools import cache

class consult:
    def __init__(self):
        self.url_api_sploitus = 'https://sploitus.com/search'
        self.status_requests = []
        
    def __check_cve_string(self, cve):
        return re.search('CVE-\d{4}-\d{4,7}', cve)
    
    def refact_cve(self, cve: str, status_code: int):
        self.status_requests.append({
                    "cve": cve,
                    "status_code": status_code
                })
        with open('debug_cves_sploitus.json', 'w') as file:
            file.write(json.dumps(self.status_requests, indent=4))
    
    async def get_vuln_id_info(self, vulnid, type):
        if self.__check_cve_string(cve=vulnid):
            body_search = {
                    "type": type, 
                    "sort": "default",
                    "query": vulnid,
                    "title": False,
                    "offset": 0
                }
            
            headers = {
                "authority": "sploitus.com",
                "accept": "application/json",
                "accept-language": "en-US,en;q=0.9",
                "content-type": "application/json",
                "origin": "https://sploitus.com",
                "referer": f"https://sploitus.com/?query={vulnid}",
                "sec-ch-ua": "^\\^Google",
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": "^\\^Windows^^",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin"
            }
            async with httpx.AsyncClient(http2=True) as client:
                response = await client.post(self.url_api_sploitus, json=body_search, headers=headers, timeout=10)
                await asyncio.sleep(1)
                self.refact_cve(cve=vulnid, status_code=response.status_code)
                if response.status_code == 200: return response.json()
                return None
        
    async def check_vuln_has_exploit(self, vulnid):
        vulnid_data = await self.get_vuln_id_info(vulnid, 'exploits')
        if vulnid_data.get('exploits_total') > 0:
            return True
        else:
            return False
    
    async def get_types_exploits(self, vulnid):
        types_exploits = []
        vulnid_data = await self.get_vuln_id_info(vulnid, 'exploits')
        if vulnid_data:
            if vulnid_data.get('exploits'):
                for exploit in vulnid_data.get('exploits'):
                    types_exploits.append(exploit.get('type'))
                types_exploits = set(list(types_exploits))
            return list(types_exploits)

    async def get_vuln_exploits(self, vulnid):
        vulnid_data = await self.get_vuln_id_info(vulnid, 'exploits')
        return vulnid_data.get('exploits')
    
    async def get_vuln_total_exploits(self, vulnid):
        vulnid_data = await self.get_vuln_id_info(vulnid, 'exploits')
        return vulnid_data.get('exploits_total')
    
    async def check_vuln_has_tool(self, vulnid):
        vulnid_data = await self.get_vuln_id_info(vulnid, 'tools')
        if vulnid_data.get('exploits_total') > 0:
            return True
        else:
            return False
    
    async def get_vuln_tools(self, vulnid):
        vulnid_data = await self.get_vuln_id_info(vulnid, 'tools')
        return vulnid_data.get('exploits')
    
    async def get_vuln_total_tools(self, vulnid):
        vulnid_data = await self.get_vuln_id_info(vulnid, 'tools')
        return vulnid_data.get('exploits_total')
    

if __name__ == "__main__":
    c = consult()
    re = asyncio.run(c.get_types_exploits('CVE-2023-36745'))
    print(re)