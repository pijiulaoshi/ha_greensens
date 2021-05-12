import requests
import urllib3

urllib3.disable_warnings()
import json
from datetime import date


class GreensensApi:
    def __init__(self, username: str, password: str):
        self._user = username
        self._pass = password
        self._host = "https://api.greensens.de/api"
        self.s = requests.Session()
        self._at = None
        self._atd = None
        self.authenticate()

        self._bearer = f"Bearer {self._at}"
        self._headers = {"Content-Type": "application/json"}
        self._data = None
        # self._hubs = None
        self._sensors = None

        self.update()
        self.update_sensors()

    def return_data(self):
        """Return sensor data"""
        self.update()
        return self._data

    def return_sensors(self):
        """Return sensor data"""
        # self.update()
        self.update_sensors()
        return self._sensors

    def update_sensors(self):
        """Return sensor list"""
        list = []
        for key, value in self._data.items():
            list.append(key)
        self._sensors = list

    def update(self):
        """Update sensor data"""
        self._data = self.get_sensordata()

    ## HTTP REQUEST ##
    def get_sensordata(self):
        """Make a request."""
        self.update_access_token()
        headers = self._headers
        headers["authorization"] = self._bearer
        data = self.s.get(
            f"{self._host}/plants", headers=headers, verify=False, timeout=10
        )
        if data.status_code == 200:
            hubs = data.json()["data"]["registeredHubs"]
            new_data = {}
            for hub in hubs:
                for sensor in hub["plants"]:
                    new_data[sensor["sensorID"]] = sensor
            return new_data
        else:
            return self._data

    ## AUTH ##
    def authenticate(self):
        url = f"{self._host}/users/authenticate"
        payload = json.dumps({"login": self._user, "password": self._pass})
        r = self.s.post(
            url, headers={"Content-Type": "application/json"}, data=payload, timeout=10
        )
        token = r.json()["data"]["token"]
        auth_date = date.today()
        self._at = token
        self._atd = auth_date

    def update_access_token(self):
        if self._at == None:
            self.authenticate()
        tokenage = date.today() - self._atd
        if tokenage.days > 4:
            self.authenticate()


##===============================##
