from flask import Flask, render_template, request, logging, Response, redirect, flash
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import os
from dotenv import load_dotenv
from collections import OrderedDict
import json
import keras
import tensorflow as tf
from keras import backend as K
from keras.models import model_from_json
import MySQLdb

# 環境変数を読み込む
load_dotenv('.env')
env = os.environ
CLIENT_ID = env['CLIENT_ID']
CLIENT_SECRET = env['CLIENT_SECRET']

# Flask の起動
app = Flask(__name__)
with open("model.json", "r") as fm:
    jsonf = fm.read()
model = model_from_json(jsonf)
graph = tf.get_default_graph()

class SpotifyAPI:
    def __init__(self):
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials(self.client_id, self.client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
        self.market = 'JP'
        self.max_duration_ms = 3724438.0
        self.min_duration_ms = 4500.0
        self.max_loudness = 1.893
        self.min_loudness = -60.0
        self.max_tempo = 231.988
        self.min_tempo = 0.0
        with open('label2track.json', 'r') as f:
            self.label2track = json.load(f)

    def search_track(self, search_track, search_artist):
        search_kw = 'track:{0}% artist:{1}'.format(search_track, search_artist)
        result = self.sp.search(q=search_kw, type='track', limit=1)
        item = result['tracks']['items'][0]

        spotify_track_url =item['external_urls']['spotify']  # spotify url of the track
        artist_name = item['artists'][0]['name']  # artist name
        track_id = item['id']  # track id
        track_name = item['name']  # track name
        # preview_url = item['preview_url']  # preview url
        album_image_url = item['album']['images'][0]  # album image url
        # album_name = item['album']['name']  # album name

        return  track_id, track_name, artist_name, album_image_url, spotify_track_url


    def search_track_features(self, track_id):
        result = self.sp.audio_features(track_id)
        result = result[0]
        features_dict = OrderedDict()

        if result == None:
            features_dict['acousticness'] = 0
            features_dict['danceability'] = 0
            features_dict['duration_ms'] = 0
            features_dict['energy'] = 0
            features_dict['instrumentalness'] = 0
            features_dict['liveness'] = 0
            features_dict['loudness'] = 0
            features_dict['speechiness'] = 0
            features_dict['tempo'] = 0
            features_dict['valence'] = 0
            return features_dict

        features_dict['acousticness'] = result['acousticness']
        features_dict['danceability'] =  result['danceability']
        features_dict['duration_ms'] = result['duration_ms']
        features_dict['energy'] = result['energy']
        features_dict['instrumentalness'] = result['instrumentalness']
        features_dict['liveness'] =  result['liveness']
        features_dict['loudness'] =  result['loudness']
        features_dict['speechiness'] = result['speechiness']
        features_dict['tempo'] =  result['tempo']
        features_dict['valence'] =  result['valence']
        return features_dict

    def predict(self, search_track, search_artist):
        track_id, track_name, artist_name, album_image_url, spotify_track_url = \
            self.search_track(search_track=search_track, search_artist=search_artist)

        features_dict = self.search_track_features(track_id)
        track_feature = np.array(np.array([list(features_dict.values())]))
        '''MinMaxScale'''
        track_feature[0][2] = (track_feature[0][2] - self.min_duration_ms) / (self.max_duration_ms - self.min_duration_ms)
        track_feature[0][6] = (track_feature[0][6] - self.min_loudness) / (self.max_loudness - self.min_loudness)
        track_feature[0][8] = (track_feature[0][8] - self.min_tempo) / (self.max_tempo - self.min_tempo)

        global graph
        with graph.as_default():
            model.load_weights('trained_weights.h5')
            inference = model.predict(track_feature)[0]

        ranking = np.argsort(inference)[::-1][:10]
        ranking = [self.label2track[str(r)] for r in ranking]

        results = self.sp.tracks(ranking)
        recommend_tracks = [{'track_name': track_name, 'artist_name': artist_name,\
                             'track_url': spotify_track_url, 'image_url': album_image_url['url']}]


        for result in results['tracks']:
            d = {}
            d['track_name'] = result['name']
            d['artist_name'] = result['artists'][0]['name']
            d['track_url'] = result['external_urls']['spotify']
            d['image_url'] = result['album']['images'][0]['url']
            recommend_tracks.append(d)

        return recommend_tracks



@app.route('/', methods = ["GET" , "POST"])
def index():
    if request.method == 'POST':
        track_name = request.form['track_name']
        artist_name = request.form['artist_name']

        spotifyapi = SpotifyAPI()
        try:
            recommend_tracks = spotifyapi.predict(search_track=track_name, search_artist=artist_name)
        except IndexError:
            return render_template('search.html')


        return render_template('result.html',
                               searched_track=recommend_tracks[0],
                               recommend_tracks=recommend_tracks[1:]
                              )

    else:
        return render_template('search.html')


@app.route("/library")
def walk():

    return render_template("library.php")

@app.route("/profile")
def run():
    return render_template("profile.php")

@app.route("/sign_in", methods = ["GET" , "POST"])
def attack():
    if request.method == 'POST':
        mail_address = request.form['mail_address']
        nick_name = request.form['nick_name']

        conn = MySQLdb.connect(
             user='root',
             passwd='root',
             host='localhost',
             port = 8888,
             unix_socket='/Applications/MAMP/tmp/mysql/mysql.sock',
             db='kadai')
        cur = conn.cursor()
        sql = 'INSERT INTO users (mail_address, nick_name) VALUES ("{0}", "{1}")'.format(mail_address, nick_name)

        cur.execute(sql)
        rows = cur.fetchall()
        print(rows)

        cur.close()
        conn.commit()
        conn.close()

        return render_template('profile.php',
                               mail_address=mail_address,
                               nick_name=nick_name
                              )
    else:
        return render_template("sign_in.html")


if __name__ == '__main__':
    app.run(debug=True, host="localhost", port=9999)
