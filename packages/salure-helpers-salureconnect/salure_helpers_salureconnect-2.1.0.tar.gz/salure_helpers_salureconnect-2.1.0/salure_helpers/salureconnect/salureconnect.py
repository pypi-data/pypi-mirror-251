import os
import requests
import json
from typing import Union


class SalureConnect:
    def __init__(self, customer: str = None, api_token: str = None, staging: str = 'prod'):
        self.customer = os.getenv("SALURECONNECT_CUSTOMER_NAME", customer)
        self.api_token = os.getenv("SALURECONNECT_API_TOKEN", api_token)
        self.environment = os.getenv("SALURECONNECT_ENVIRONMENT", staging)
        if any([self.customer is None, self.api_token is None]):
            raise ValueError("Set the customer, api_token either in your .env file or provide the customer and api_token parameters")
        possible_environments = ['dev', 'prod']
        if self.environment not in possible_environments:
            raise ValueError(f"Environment should be in {','.join(possible_environments)}")
        self.url = 'https://staging.salureconnect.com/api/v1/' if self.environment == 'dev' else 'https://salureconnect.com/api/v1/'

    def _get_sc_headers(self):
        return {
            'Authorization': f'SalureToken {self.api_token}',
            'salure-customer': self.customer
        }

    def get_system_credential(self, system: str, label: Union[str, list], test_environment: bool = False) -> json:
        """
        This method retrieves authentication credentials from salureconnect.
        It returns the json data if the request does not return an error code
        :param system: specifies which token is used. (lowercase)
        :param label: reference to the used label
        :param test_environment: boolean if the test environment is used
        :return json response from salureconnect
        """
        response = requests.get(url=f'{self.url}connector/{system}', headers=self._get_sc_headers())
        response.raise_for_status()
        credentials = response.json()
        # rename parameter for readability
        if isinstance(label, str):
            labels = [label]
        else:
            labels = label
        # filter credentials based on label. All labels specified in label parameter should be present in the credential object
        credentials = [credential for credential in credentials if all(label in credential['labels'] for label in labels)]
        if system == 'profit':
            credentials = [credential for credential in credentials if credential['isTestEnvironment'] is test_environment]

        if len(credentials) == 0:
            raise ValueError(f'No credentials found for {system}')
        if len(credentials) != 1:
            raise ValueError(f'Multiple credentials found for {system} with the specified labels')

        return credentials[0]

    def refresh_system_credential(self, system: str, system_id: int) -> json:
        """
        This method refreshes Oauth authentication credentials in salureconnect.
        It returns the json data if the request does not return an error code
        :param system: specifies which token is used. (lowercase)
        :param system_id: system id in salureconnect
        :return json response from salureconnect
        """
        response = requests.post(url=f'{self.url}connector/{system}/{system_id}/refresh', headers=self._get_sc_headers())
        response.raise_for_status()
        credentials = response.json()

        return credentials

    def get_mappings(self, task_id: int) -> dict:
        """
        Get the mappings from the task in salureconnect
        :param task_id: The id of the task in salureconnect. this does not have to be the task id of the current task
        :return: A dictionary with the following structure: {mapping_title: {tuple(input): output}}
        """
        response = requests.get(url=f'{self.url}connectors/{task_id}/data-mapping', headers=self._get_sc_headers())

        data = response.json()

        # transform the data to a dictionary where the key is the title of the mapping and the value is the mapping as a dict
        mappings = {
            item['title']: {tuple(mapping['input']) if len(mapping['input']) > 1 else mapping['input'][0]: mapping['output'] for mapping in item['mapping']} for item in data
        }

        return mappings

    def get_user_data(self):
        """
        Get all users from salureconnect
        :return: A list of users
        """
        return requests.get(url=f'{self.url}users', headers=self._get_sc_headers())

    def get_role_data(self):
        """
        Get all roles from salureconnect
        :return: A list of roles
        """
        return requests.get(url=f'{self.url}roles', headers=self._get_sc_headers())

    def create_user(self, user_data: dict) -> requests.Response:
        """
        Create a user in salureconnect
        :param user_data: A dictionary with the following structure:
        {
            "name": "string",
            "username": "string",
            "email": "string",
            "language": "string",
            "salure_connect": true,
            "qlik_sense_analyzer": true,
            "qlik_sense_professional": true
        }
        :return: A response object
        """
        data = {
            "name": user_data['name'],
            "username": user_data['username'],
            "email": user_data['email'],
            "language": user_data['language'],
            "products": {
                "salureconnect": user_data['salure_connect'],
                "qlikSenseAnalyzer": user_data['qlik_sense_analyzer'],
                "qlikSenseProfessional": user_data['qlik_sense_professional'],
            }
        }

        return requests.post(url=f'{self.url}users', headers=self._get_sc_headers(), json=data)

    def delete_user(self, user_id: str) -> requests.Response:
        """
        Delete a user in salureconnect
        :param user_id: The id of the user in salureconnect
        :return: A response object
        """
        return requests.delete(url=f'{self.url}users/{user_id}', headers=self._get_sc_headers())

    def overwrite_user_roles(self, user_id: int, roles: list) -> requests.Response:
        """
        Overwrite the roles of a user in salureconnect
        :param user_id: The id of the user in salureconnect
        :param roles: A list of role ids
        :return: A response object
        """
        data = {
            "roles": roles
        }

        return requests.put(url=f'{self.url}users/{user_id}/roles', headers=self._get_sc_headers(), json=data)
