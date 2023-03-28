from align_data.common.alignment_dataset import AlignmentDataset, DataEntry
from dataclasses import dataclass
from git import Repo
import logging
from tqdm import tqdm

import requests
import os
from path import Path
import re
from typing import List, Tuple

logger = logging.getLogger(__name__)

@dataclass
class AgentModels(AlignmentDataset):
    """
    Grabs the "Modeling Agents with Probabilistic Programs" by Owain Evans, Andreas Stuhlmüller,
    John Salvatier, and Daniel Filan as .md from GitHub
    """
    repo_owner: str = "agentmodels"
    repo_name: str = "agentmodels.org"
    folder_path: str = "chapters"
    
    base_url: str = f"https://api.github.com/repos/{repo_owner}/{repo_name}/contents/{folder_path}"
    
    def _process_md_file(self, file):
        raw_url = f"https://raw.githubusercontent.com/{self.repo_owner}/{self.repo_name}/gh-pages/{file['path']}"
        response = requests.get(raw_url)
        if response.status_code == 200:
            text = response.text
            title_pattern = re.compile(r'^title:\s*(.*?)\s*$', flags=re.MULTILINE)
            match = title_pattern.search(text)
            title = match.group(1) if match else "No title found"
            html_filename = os.path.splitext(file['name'])[0] + ".html"
            url = f"https://agentmodels.org/chapters/{html_filename}"
        else:
            raise Exception("Error: {response.status_code}")
        return title, url, text
    
    def setup(self):
        self._setup()
        self.raw_path = self.write_jsonl_path.parent / 'raw'
        self._get_files()

    def _get_files(self) -> List[Tuple[str, str, str]]:
        # Get the list of files in the repo
        self.files_info: List[Tuple[str, str, str]] = []
        
        response = requests.get(self.base_url)
        
        if response.status_code == 200:
            files = response.json()
            for file in files:
                if file['type'] == 'file' and file['name'].endswith('.md'):
                    title, url, text = self._process_md_file(file)
                    self.files_info.append((title, url, text))
        else:
            raise Exception("Error: {response.status_code}")
    
        # if not self.raw_path.exists:
        #     self.raw_path.mkdir()
        # if not (self.raw_path / 'agentmodels.org').exists():
        #     logger.info("Cloning repo")
        #     Repo.clone_from(self.repo, self.raw_path / 'agentmodels.org')
        # self.repo_path = self.raw_path / 'agentmodels.org' / 'chapters'

    def fetch_entries(self):
        self.setup()
        for (title, url, text) in tqdm(self.files_info):
            new_entry = DataEntry({
                'source': 'ebook',
                'title': f'Modeling Agents with Probabilistic Programs - {title}',
                'authors': ['Owain Evans', 'Andreas Stuhlmüller', 'John Salvatier', 'Daniel Filan'],
                'date_published': '2016',
                'url': url,
                'text': text
            })
            new_entry.add_id()
            yield new_entry