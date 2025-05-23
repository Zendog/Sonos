#! /usr/bin/env python
# -*- coding: utf-8 -*-
#

import crypt
import json
import time
import urllib.parse
import urllib.request
import indigo

class AuthenticationError(Exception):
    """Raised when an operation encountered authentication issues."""
    pass


class PandoraConnection(object):

    partner_id = None
    partner_auth_token = None

    user_id = None
    user_auth_token = None

    time_offset = None

    PROTOCOL_VERSION = '5'
    RPC_URL = "https://tuner.pandora.com/services/json/?"
    RPC_URL = "://tuner.pandora.com/services/json/?"
    DEVICE_MODEL = 'android-generic'
    PARTNER_USERNAME = 'android'
    PARTNER_PASSWORD = 'AC7IBG09A3DTSYM4R41UJWL07VLN8JI7'
    AUDIO_FORMAT_MAP = {'aac': 'HTTP_64_AACPLUS_ADTS',
                        'mp3': 'HTTP_128_MP3'}
    stations = []


    def __init__(self):
        self.rid = "%07i" % (time.time() % 1e7)
        self.timedelta = 0




    def authenticate(self, username, password):
        import indigo
        import time
        try:
            indigo.server.log(f"🔐 BEGIN PandoraConnection.authenticate() for {username}")

            # Step 1: Partner Login
            partner_response = self.do_request(
                method='auth.partnerLogin',
                secure=True,
                crypted=False,
                deviceModel=self.DEVICE_MODEL,
                username=self.PARTNER_USERNAME,
                password=self.PARTNER_PASSWORD,
                version=self.PROTOCOL_VERSION
            )
            indigo.server.log("✅ Partner login response received")

            self.partner_id = partner_response.get('partnerId')
            self.partner_auth_token = partner_response.get('partnerAuthToken')

            if not self.partner_id or not self.partner_auth_token:
                indigo.server.log("❌ Partner login failed: Missing partnerId or partnerAuthToken")
                return False

            # Step 2: Time Sync
            encrypted_sync_time = partner_response.get('syncTime')
            if not encrypted_sync_time:
                indigo.server.log("❌ Partner login failed: syncTime missing")
                return False

            decrypted_time = crypt.pandora_decrypt(encrypted_sync_time)
            pandora_time = int(decrypted_time[4:14])
            self.time_offset = pandora_time - time.time()
            indigo.server.log(f"⏱ Time sync calculated. Offset: {self.time_offset:.2f} seconds")

            # Step 3: User Login
            indigo.server.log(f"🔐 Attempting user login for {username}")
            user_response = self.do_request(
                method='auth.userLogin',
                secure=True,
                crypted=True,
                username=username,
                password=password,
                loginType="user",
                returnStationList=True
            )
            indigo.server.log("✅ User login response received")

            self.user_id = user_response.get('userId')
            self.user_auth_token = user_response.get('userAuthToken')

            if not self.user_id or not self.user_auth_token:
                indigo.server.log("❌ User login failed: Missing userId or userAuthToken")
                return False

            # Step 4: Load Stations
            self.stations = user_response.get('stationListResult', {}).get('stations', [])
            indigo.server.log(f"✅ User authenticated. Loaded {len(self.stations)} Pandora stations.")
            return True

        except Exception as e:
            indigo.server.log(f"❌ EXCEPTION in authenticate(): {e}")
            return False








    def search(self, text):
        return self.do_request("music.search", False, True, searchText=text)

    def get_stations(self):
        try:
            return self.do_request('user.getStationList', False, True)['stations']
        except ValueError:
            return self.stations

    def get_genre_stations(self):
        return self.do_request("station.getGenreStations", False, True)

    def get_fragment(self, station_token=None, additional_format="mp3"):
        songlist = self.do_request('station.getPlaylist', True, True, stationToken=station_token, additionalAudioUrl=self.AUDIO_FORMAT_MAP[additional_format])['items']

        self.curStation = station_token
        self.curFormat = format

        return songlist

    def get_station(self, station_token):
        return self.do_request('station.getStation', False, True, stationToken=station_token, includeExtendedAttributes=True)

    def delete_station(self, station_token):
        self.do_request('station.deleteStation', False, True, stationToken=station_token)

    def add_seed(self, station_token, music_token):
        return self.do_request('station.addMusic', False, True, stationToken=station_token, musicToken=music_token)

    def delete_seed(self, station_token, seed_token):
        self.do_request("station.deleteMusic", False, True, seedId=seed_token)

    def add_feedback(self, station_token, track_token, is_positive_feedback=True):
        return self.do_request("station.addFeedback", False, True, stationToken=station_token, trackToken=track_token, isPositive=is_positive_feedback)

    def delete_feedback(self, station_token, feedback_token):
        self.do_request("station.deleteFeedback", False, True, feedbackId=feedback_token)


    def do_request(self, method, secure, crypted, **kwargs):
        import indigo
        import urllib.request
        import urllib.parse
        import json
        import time

        try:
            # Construct query string parameters
            url_arg_strings = []
            if self.partner_id:
                url_arg_strings.append('partner_id=%s' % self.partner_id)
            if self.user_id:
                url_arg_strings.append('user_id=%s' % self.user_id)
            if self.user_auth_token:
                url_arg_strings.append('auth_token=%s' % urllib.parse.quote(self.user_auth_token))
            elif self.partner_auth_token:
                url_arg_strings.append('auth_token=%s' % urllib.parse.quote(self.partner_auth_token))

            url_arg_strings.append('method=%s' % method)
            url = ('https' if secure else 'http') + self.RPC_URL + '&'.join(url_arg_strings)

            # Add time sync and tokens
            if self.time_offset:
                kwargs['syncTime'] = int(time.time() + self.time_offset)
            if self.user_auth_token:
                kwargs['userAuthToken'] = self.user_auth_token
            elif self.partner_auth_token:
                kwargs['partnerAuthToken'] = self.partner_auth_token

            # Prepare JSON payload
            payload = json.dumps(kwargs)
            if crypted:
                encrypted_str = crypt.pandora_encrypt(payload)  # still a string
                data = encrypted_str.encode("utf-8")             # encode to bytes
            else:
                data = payload.encode("utf-8")                   # directly encode

            # Build and send the request
            headers = {
                'User-agent': "02strich",
                'Content-type': 'text/plain'
            }
            req = urllib.request.Request(url, data, headers)
            response = urllib.request.urlopen(req)
            text = response.read()

            # Decode and parse response
            tree = json.loads(text)
            if tree.get('stat') == 'fail':
                code = tree.get('code')
                msg = tree.get('message')
                if code == 1002:
                    raise AuthenticationError()
                else:
                    raise ValueError("%d: %s" % (code, msg))
            elif 'result' in tree:
                return tree['result']

        except Exception as e:
            indigo.server.log(f"❌ EXCEPTION in do_request({method}): {e}")
            raise
