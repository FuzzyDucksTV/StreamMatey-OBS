"""
The `twitch_api.py` script is part of the StreamMatey OBS Plugin software. It provides a `TwitchAPI` class for interacting with the Twitch API.

The `TwitchAPI` class is initialized with the client ID, client secret, and redirect URI for the Twitch API. It also sets the base URL for the Twitch API and the URL for OAuth authentication.

The `TwitchAPI` class provides the following methods:

- `authenticate(code)`: This method takes an authorization code as input and uses it to authenticate with the Twitch API. It sends a POST request to the OAuth URL with the client ID, client secret, authorization code, grant type, and redirect URI. If the request is successful, it sets the access token for the `TwitchAPI` instance.

- `get_user_info()`: This method retrieves the user's information from the Twitch API. It sends a GET request to the `/users` endpoint of the Twitch API with the client ID and access token in the headers. If the request is successful, it returns the first user object in the response data.

- `get_channel_info(broadcaster_id)`: This method takes a broadcaster ID as input and retrieves the channel's information from the Twitch API. It sends a GET request to the `/channels` endpoint of the Twitch API with the broadcaster ID, client ID, and access token in the headers. If the request is successful, it returns the first channel object in the response data.

In the main part of the script, an instance of the `TwitchAPI` class is created with the client ID, client secret, and redirect URI. The `authenticate` method is then called with an authorization code to authenticate with the Twitch API and set the access token.
"""

import requests

class TwitchAPI:
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.base_url = 'https://api.twitch.tv/helix'
        self.oauth_url = 'https://id.twitch.tv/oauth2/token'
        self.access_token = None

    def authenticate(self, code):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        response = requests.post(self.oauth_url, data=data)
        response.raise_for_status()  # Raise exception if the request failed
        self.access_token = response.json().get('access_token')

    def get_user_info(self):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.get(f'{self.base_url}/users', headers=headers)
        response.raise_for_status()  # Raise exception if the request failed
        return response.json().get('data', [{}])[0]  # Return the first user object

    def get_channel_info(self, broadcaster_id):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': f'Bearer {self.access_token}'
        }
        response = requests.get(f'{self.base_url}/channels?broadcaster_id={broadcaster_id}', headers=headers)
        response.raise_for_status()  # Raise exception if the request failed
        return response.json().get('data', [{}])[0]  # Return the first channel object

