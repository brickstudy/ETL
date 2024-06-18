import pytest
import requests
from airflow.hooks.base_hook import BaseHook

base_url = "https://api.github.com"
repo_name = "brickstudy/ETL"



def test_github_hook_can_get_repo_info():
    # given : repo name
    headers = {
            'Authorization': f'token {self.token}'
        }
    response = requests.get(f'{base_url}/repos/{repo_name}', headers=headers)
    response.raise_for_status()
    # when : request

    # return : repo info
