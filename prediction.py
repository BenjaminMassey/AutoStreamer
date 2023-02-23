from urllib.parse import urlparse
from urllib.parse import parse_qs
import urllib.request as urlget
import requests, json, webbrowser

class Predictor:
    
    channel = None
    client_id = None
    client_secret = None
    access_token = None
    broadcaster_id = None
    auth_code = None
    auth_token = None
    prediction_id = None
    outcome_ids = []
    
    def __init__(self, channel, id, secret):
        self.channel = channel
        self.client_id = id
        self.client_secret = secret
        self.access_token = self.getAccessToken()
        self.broadcaster_id = self.getBroadcasterId()
        self.auth_code = self.getAuthCode()
        self.auth_token = self.getAuthToken()
    
    def getAccessToken(self):
        url = "https://id.twitch.tv/oauth2/token"
        request = requests.post(url, data=\
        {\
            "client_id": str(self.client_id),\
            "client_secret": str(self.client_secret),\
            "grant_type": "client_credentials"\
        })
        response = request.json()

        if "access_token" in response.keys():
            return response["access_token"]
        return None
    
    def getBroadcasterId(self):
        url = "https://api.twitch.tv/helix/users?login=" + self.channel
        request = requests.get(url, headers=\
        {\
            "Authorization": "Bearer " + self.access_token,\
            "Client-Id": self.client_id\
        })
        response = request.json()
        
        if "data" in response.keys():
            if "id" in response["data"][0].keys():
                return str(response["data"][0]["id"])
        return None
        
    def getAuthCode(self):
        url = "https://id.twitch.tv/oauth2/authorize"
        url += "?response_type=code&"
        url += "force_verify=false&"
        url += "client_id=" + self.client_id + "&"
        url += "redirect_uri=http://localhost:3000&"
        url += "scope=channel%3Amanage%3Apredictions"
        
        webbrowser.open(url)
        
        response = input("Response URL: ")
        
        parsed_response = urlparse(response)
        params = parse_qs(parsed_response.query)
        if "code" in params.keys():
            return params["code"][0]
        return None
    
    def getAuthToken(self):
        url = "https://id.twitch.tv/oauth2/token"
        request = requests.post(url, data=\
        {\
            "client_id": self.client_id,\
            "client_secret": self.client_secret,\
            "code": self.auth_code,\
            "grant_type": "authorization_code",\
            "redirect_uri": "http://localhost:3000"\
        })
        response = request.json()

        if "access_token" in response.keys():
            return response["access_token"]
        return None
    
    def createPrediction(self, title, outcomes):
        url = "https://api.twitch.tv/helix/predictions"
        request = requests.post(url, \
        json= \
            { \
                "broadcaster_id": self.broadcaster_id, \
                "title": title, \
                "outcomes": outcomes, \
                "prediction_window": 100 \
            }, \
        headers= \
            { \
                "Authorization": "Bearer " + self.auth_token, \
                "Client-Id": self.client_id \
            } \
        )
        response = request.json()
        print(response)
        if "data" in response.keys():
            if "id" in response["data"][0].keys():
                self.prediction_id = response["data"][0]["id"]
            if "outcomes" in response["data"][0].keys():
                outcomes_list = response["data"][0]["outcomes"]
                self.outcome_ids = []
                for outcome in outcomes_list:
                    if "id" in outcome.keys():
                        self.outcome_ids.append(outcome["id"])
    
    def endPrediction(self, outcome_index):
        url = "https://api.twitch.tv/helix/predictions?"
        url += "broadcaster_id=" + self.broadcaster_id + "&"
        url += "id=" + self.prediction_id + "&"
        url += "status=RESOLVED&"
        url += "winning_outcome_id=" + self.outcome_ids[outcome_index]
        
        request = requests.patch(url, headers=\
        {\
            "Authorization": "Bearer " + self.auth_token,\
            "Client-Id": self.client_id\
        })
        
        print(request.json())


run_example = False

if run_example:

    import settings
    
    app_settings = settings.Settings()
    
    channel = app_settings.get("twitch_channel")
    client_id = app_settings.get("twitch_client_id")
    client_secret = app_settings.get("twitch_client_secret")

    puck = Predictor(channel, client_id, client_secret)

    puck.createPrediction( "What level will I reach?", \
        [\
            {\
                "title": "Level 1"\
            },\
            {\
                "title": "Level 2"\
            },\
            {\
                "title": "Level 3"\
            },\
            {\
                "title": "Level 4"\
            }\
        ])
        
    result = int(input("Index to win: "))

    puck.endPrediction(result)