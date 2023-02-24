from urllib.parse import urlparse
from urllib.parse import parse_qs
import urllib.request as urlget
from datetime import timedelta
import requests, json, webbrowser, random

class TwitchAPI:
    
    channel = None
    client_id = None
    client_secret = None
    access_token = None
    broadcaster_id = None
    auth_code = None
    auth_token = None
    prediction_id = None
    outcome_ids = []
    subscribers = []
    
    def __init__(self, channel, id, secret):
        self.channel = channel
        self.client_id = id
        self.client_secret = secret
        self.access_token = self.getAccessToken()
        self.broadcaster_id = self.getBroadcasterId()
        self.auth_code = self.getAuthCode()
        self.auth_token = self.getAuthToken()
        self.newSubscribers()
    
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
        print("Error with access token:", response)
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
        print("Error with broadcaster id:", response)
        return None
        
    def getAuthCode(self):
        # TODO: no user input
    
        url = "https://id.twitch.tv/oauth2/authorize"
        url += "?response_type=code&"
        url += "force_verify=false&"
        url += "client_id=" + self.client_id + "&"
        url += "redirect_uri=http://localhost:3000&"
        url += "scope=channel%3Amanage%3Apredictions"
        url += "+channel%3Aread%3Asubscriptions"
        
        webbrowser.open(url)
        
        response = input("Response URL: ")
        
        parsed_response = urlparse(response)
        params = parse_qs(parsed_response.query)
        if "code" in params.keys():
            return params["code"][0]
        print("Error with auth code:", response)
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
        print("Error with auth token:", response)
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
        
    def newSubscribers(self):
        url = "https://api.twitch.tv/helix/subscriptions"
        url += "?broadcaster_id=" + self.broadcaster_id
        
        request = requests.get(url, headers=\
        {\
            "Authorization": "Bearer " + self.auth_token,\
            "Client-Id": self.client_id\
        })
        response = request.json()
        
        old_list = self.subscribers
        self.subscribers = []
        new_subscribers = []
        if "data" in response.keys():
            for datum in response["data"]:
                if "user_name" in datum.keys():
                    entry = datum["user_name"]
                    self.subscribers.append(entry)
                    if entry not in old_list:
                        new_subscribers.append(entry)
        return new_subscribers

    def generatePrediction(self):
        # TODO: think about this generation more
        time_range = (1 * 60, 46 * 60) # from 1 minute to 46 minutes (in seconds)
        #time_range = (1 * 60, 2 * 60) # from 1 minutes to 2 minutes (in seconds) (debug)
        predict_time = None
        run_rng = random.randint(1, 100)
        if run_rng != 100:
            predict_time = ((time_range[1] - time_range[0]) * (run_rng / 100)) + time_range[0]
            time_str = str(timedelta(seconds=predict_time))[2:]
        
        title = "Will this run finish?"
        if predict_time is not None:
            title = "Will this run make it to " + time_str + "?"
        
        return [title, [ { "title": "Yes" }, { "title": "No" }, ],  predict_time]


run_example = False

if run_example:

    import settings
    
    app_settings = settings.Settings()
    
    channel = app_settings.get("twitch_channel")
    client_id = app_settings.get("twitch_client_id")
    client_secret = app_settings.get("twitch_client_secret")

    api = TwitchAPI(channel, client_id, client_secret)

    api.createPrediction( "What level will I reach?", \
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

    api.endPrediction(result)