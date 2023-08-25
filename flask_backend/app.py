import numpy as np 
from flask import Flask, request, jsonify 
import joblib 
from transformers import pipeline 
from flask import Flask, request, redirect, session
import requests
from flask_cors import CORS
import base64
import urllib.parse
import http.client
import json

global top_artists
top_artists = ""
global top_tracks
top_tracks = ""
global access_token 

CLIENT_ID = '61f86c15e6b34a75a0ff6d4ed85abcc3'
CLIENT_SECRET = '5a1c80f5c3f74e10b1fa8330150e4665'
REDIRECT_URI = 'http://127.0.0.1:5000/callback'

credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")

headers = {
  "Authorization": f"Basic {base64_credentials}"
}

app = Flask(__name__)
CORS(app)

app.secret_key = 'kldfsjh2jkl34h52l3h4kldjf23430956dndsfoewrhn'

    

@app.route('/login')
def login():
    auth_url = f"https://accounts.spotify.com/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={REDIRECT_URI}&scope=user-top-read user-read-playback-state user-modify-playback-state streaming"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    data = {
        'grant_type': "authorization_code",
        "code" : code,
        "redirect_uri" : REDIRECT_URI
    }
    search_url = "https://accounts.spotify.com/api/token"
    response = requests.post(search_url, data=data, headers=headers)
    response = response.json()
    token = response.get('access_token')
    if token:
        global access_token
        access_token = token

    search_url = "https://api.spotify.com/v1/me/top/artists"
    params2 = {
        "time_range" : "short_term",
        "limit": 3
    }
    headers_2 = {
    'Authorization': f'Bearer {access_token}'
    }
    top_artists_req = requests.get(search_url, params=params2, headers=headers_2)
    top_json = top_artists_req.json()
    global top_artists
    top_artists += top_json["items"][0]["id"] + ","
    top_artists += top_json["items"][1]["id"] + ","
    top_artists += top_json["items"][2]["id"] 
    search_url2 =  "https://api.spotify.com/v1/me/top/tracks"
    params3 = {
        "time_range" : "short_term",
        "limit": 2
    }
    top_tracks_req = requests.get(search_url2, params=params3, headers=headers_2)
    top_json2 = top_tracks_req.json()
    global top_tracks
    top_tracks += top_json2["items"][0]["id"] + ","
    top_tracks += top_json2["items"][1]["id"]

    return redirect("http://localhost:3000/")


emotion_detection = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base", return_all_scores=True)

prediction_model = joblib.load('./models/linear_reg_model.pkl')

@app.route('/predict', methods=["POST"])
def get_acoustic():
    data = request.get_json()
    text = data.get("text")

    if not text:
        return

    emotions = ["joy", "anger", "fear", "sadness"]
    
    weights = []

    #Uses emotion detection model to get weights for my prediction model
    results = emotion_detection(text)
    for emotion in emotions:
        for dict in results[0]:
            if dict["label"] == emotion:
                if dict["score"] > .5:
                    weights.append(1)
                else:
                    weights.append(0)
    
    if 1 not in weights:
        print("no strong emotions")
        params = {
            "limit":1,
            "seed_artists":top_artists,
            "seed_tracks":top_tracks
        }

    else:
        predicted_parameters = prediction_model.predict([weights])
        predicted_parameters = predicted_parameters[0]

        params = {
            "limit": 1,
            "seed_artists": top_artists,
            "seed_tracks": top_tracks,
            "target_acousticness": predicted_parameters[4],
            "target_danceability":predicted_parameters[0],
            "target_energy":predicted_parameters[1],
            "target_valence":predicted_parameters[5],
            "target_speechiness":predicted_parameters[3],
        }

    global access_token
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    search_url = "https://api.spotify.com/v1/recommendations"

    try:
        temp = requests.get(search_url, headers=headers, params=params)
        temp.raise_for_status()
        temp = temp.json()
        recc_uri = temp["tracks"][0]["uri"]
        print(f"SONGGGG {recc_uri}")
        uri = urllib.parse.quote(recc_uri)
        queue_url = f"https://api.spotify.com/v1/me/player/queue?uri={recc_uri}"
        payload = {
            "uri": uri
        }
        result = requests.post(queue_url, headers=headers)
        result.raise_for_status()
        return "Song queued!"
    except requests.exceptions.RequestException as e:
        return(str(e.response))


if __name__ == "__main__":
    app.run(debug=True)   
