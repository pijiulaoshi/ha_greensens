"""GreenSens Constants"""
# from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import TEMP_CELSIUS, PERCENTAGE

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from datetime import datetime, timedelta

DOMAIN = "greensens"
PLATFORMS = ["sensor"]
SCAN_INTERVAL = timedelta(seconds=600)

NOTIFICATION_TITLE = "GreenSens Setup"
NOTIFICATION_ID = "greensens_notify"


SENS_ATTR_PLANT_NAME = "plant_name"


SENSOR_FNAMES = {
    "moisture": "Moisture",
    "minMoisture": "Min Mosture",
    "maxMoisture": "Max Mosture",
    "illumination": "Light",
    "minIllumination": "Min Light",
    "maxIllumination": "Max Light",
    "temperature": "Temperature",
    "minTemperature": "Min Temperature",
    "maxTemperature": "Max Temperature",
    "sensorID": "Sensor ID",
    "status": "Status",
    "plantNameEN": "Plant Name English",
    "plantNameDE": "Plant Name German",
    "plantNameLA": "Plant Name Latin",
    "lastConnection": "Last Update",
    "calibration": "Temperature Offset",
    "state": "Plant State",
}

MAIN_SENSOR_ATTR = {
    "sensorID": "sensor_id",
    "state": "plant_state",
    "moisture": "moisture",
    "illumination": "light",
    "temperature": "temperature",
    "minMoisture": "min_moisture",
    "maxMoisture": "max_moisture",
    "minIllumination": "min_light",
    "maxIllumination": "max_ight",
    "minTemperature": "min_temperature",
    "maxTemperature": "max_temperature",
    "status": "status",
    "plantNameEN": "plant_name_english",
    "plantNameDE": "plant_name_german",
    "plantNameLA": "plant_name_latin",
    "lastConnection": "last_update",
    "calibration": "temperature_offset",
}

INT_LIST = ["min_moisture", "max_moisture", "min_light", "max_light"]

SENSOR_ATTR = {
    "temperature": {
        "minTemperature": "min_temperature",
        "maxTemperature": "max_temperature",
        "state": "plant_state",
    },
    "moisture": {
        "minMoisture": "min_moisture",
        "maxMoisture": "max_moisture",
        "state": "plant_state",
        
    },
    "illumination":{
        "minIllumination": "min_light",
        "maxIllumination": "max_light",
        "state": "plant_state",
    }
}

SENSOR_ATTR2 = {
    "state": "plant_state",
    "moisture": "moisture",
    "illumination": "light",
    "temperature": "temperature",
    "minMoisture": "min_moisture",
    "maxMoisture": "max_moisture",
    "minIllumination": "min_light",
    "maxIllumination": "max_ight",
    "minTemperature": "min_temperature",
    "maxTemperature": "max_temperature",
    "status": "status",
}

SENSOR_TYPES2 = [
    "id",
    "moisture",
    "minMoisture",
    "maxMoisture",
    "illumination",
    "minIllumination",
    "maxIllumination",
    "temperature",
    "minTemperature",
    "maxTemperature",
    "temperaturePercent",
    "moisturePercent",
    "illuminationPercent",
    "sensorID",
    "status",
    "isReset",
    "plantId",
    "plantNameEN",
    "plantNameDE",
    "plantNameLA",
    "link",
    "lastConnection",
    "packageCount",
    "calibration",
    "chargeLevel",
    "state",
    "stateColor",
]

SENSOR_DEVICE_DATA = [
    "sensorID",
    "status",
    "isReset",
    "plantNameEN",
    "plantNameDE",
    "plantNameLA",
    "link",
    "lastConnection",
    "packageCount",
    "calibration",
    "chargeLevel",
    "state",
    "stateColor",
]


SENSOR_TYPES = {
    "temperature": ["Temperature", TEMP_CELSIUS],
    "moisture": ["Moisture", PERCENTAGE],
    "illumination": ["Light", "lux"],
}

NAME_LANG = ["EN", "DE", "LA"]

CONF_USER = "username"
CONF_PASS = "password"
CONF_MON_CON = "monitored_conditions"
CONF_LANG = "name_language"
CONF_MAIN_SENSORS = "add_main_sensor"


DEFAULT_MON_CON = [
    "moisture",
    "illumination",
    "temperature",
]


### COMPONENT_CONFIG_SCHEMA ###
CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.Schema(
            {
                vol.Required(CONF_USER): cv.string,
                vol.Required(CONF_PASS): cv.string,
                vol.Optional(CONF_LANG, default="LA"): vol.In(NAME_LANG),
                vol.Optional(CONF_MAIN_SENSORS, default=True): cv.boolean,
                vol.Optional(CONF_MON_CON, default=list(DEFAULT_MON_CON)): [
                    vol.In(SENSOR_TYPES)
                ],
            }
        )
    },
    extra=vol.ALLOW_EXTRA,
)