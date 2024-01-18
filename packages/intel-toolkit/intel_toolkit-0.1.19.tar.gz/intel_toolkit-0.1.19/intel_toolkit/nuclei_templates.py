import re, os
from git import Repo
from functools import cache

output_folder = ".temp/nuclei-templates.git"

class gitHandle:
    '''Use this class as thread to previne leak resources of system
    '''
    def __init__(self, branch='main', base64_private_key=None, output=str) -> None:
        self.branch = branch
        self.git_url = "https://github.com/projectdiscovery/nuclei-templates.git"
        self.base64_private_key = base64_private_key
        self.output = output_folder
        self.repo = Repo

    def __valid_url_git(self, git_url):
        match = re.compile('((git|ssh|http(s)?)|(git@[\w\.]+))(:(//)?)([\w\.@\:/\-~]+)(\.git)(/)?')
        return bool(match.match(git_url))

    def clone_repo(self):
        if self.__valid_url_git(git_url=self.git_url):
            self.output = f'{self.output}'
            if os.path.exists(self.output):
                Repo(self.output).remotes.origin.pull()
            else:    
                    try:
                        self.repo = self.repo.clone_from(url=self.git_url, to_path=self.output, branch=self.branch)
                    except:
                        print(f'[-] Error not permission to write in folder {self.output} or permission to clone')
                        return None
                    return self.output
        else:
            print(f'[-] Invalid URL: {self.git_url}')
            return None

class mountDataBase:
    def __init__(self):
        self.files = []
        self.cves_templates = {}

    @cache
    def locate_yaml_cves(self):
        for (root, dirs, file) in os.walk(f'{output_folder}/http/cves'):
            for f in file:
                if '.yaml' in f:
                    self.files.append(f'{root}/{f}')
        return self.files
    
    @cache
    def list_cves_templates(self):
        for (root, dirs, file) in os.walk(f'{output_folder}/http/cves'):
            for f in file:
                if '.yaml' in f:
                    self.cves_templates[f'{f.replace(".yaml", "")}'] = True
        return self.cves_templates

if __name__ == "__main__":
    repository = gitHandle()
    repository.clone_repo()
    print(mountDataBase().list_cves_templates())