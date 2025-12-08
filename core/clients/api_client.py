from http.client import responses

import requests
import os
import allure

from dotenv import load_dotenv
from core.settings.environments import Environment
from core.clients.endpoint import Endpoints
from core.settings.config import Users, Timeouts
from requests.auth import HTTPBasicAuth


load_dotenv()

class APIClient:
    def __init__(self):
        environment_str = os.getenv('ENVIRONMENT')
        try:
            environment = Environment[environment_str]
        except KeyError:
            raise ValueError(f'Unsupported environment value: {environment_str}')

        self.base_url = self.get_base_url(environment)
        self.session = requests.Session()


    def get_base_url(self, environment: Environment) -> str:
        if environment == Environment.TEST:
            return os.getenv('TEST_BASE_URL')
        else:
            raise ValueError(f'Unsupported environment: {environment}')


    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()


    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()


    def auth(self):
        with allure.step('Getting authenticate'):
            url = f'{self.base_url}{Endpoints.USERS_LOGIN_ENDPOINT.value}'
            payload = {'email': Users.EMAIL.value, 'password': Users.PASSWORD.value}
            response = self.session.post(url, json=payload, timeout=Timeouts.TIMEOUT.value)
            response.raise_for_status()

        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'

        response_json = response.json()

        # ВАЖНО: Токен находится в response.json()['data']['token']
        token = response_json['data']['token']
        with allure.step('Updating header with authorization'):
            self.session.headers.update({'Authorization': f'Bearer {token}'})


    def get_notes_by_id(self, notes_id):
        with allure.step('Getting a notes by ID'):
            url = f'{self.base_url}{Endpoints.NOTES_ENDPOINT.value}/{notes_id}'
            response = self.session.get(url)
            response.raise_for_status()

        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()


    def create_notes(self, notes_data):
        with allure.step('Creating notes'):
            url = f'{self.base_url}{Endpoints.NOTES_ENDPOINT.value}'
            headers = {
                'Content-Type': 'application/json'
            }
            response = self.session.post(url, headers=headers, json=notes_data)
            response.raise_for_status()

        with allure.step('Checking status code'):
            assert response.status_code == 200, f'Expected status 200 but got {response.status_code}'
        return response.json()