"""Platform for sensor integration."""
import logging
from datetime import datetime, timedelta

from homeassistant.util import Throttle
from homeassistant.const import TEMP_CELSIUS
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.entity import Entity

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)

from .const import *

_LOGGER = logging.getLogger(__name__)


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the sensor platform."""
    domain_data = hass.data[DOMAIN]
    api = domain_data["api"]
    settings = domain_data["settings"]
    

    if settings[CONF_MAIN_SENSORS] == True:
        sensor_list = []
        for sensor in settings["connected_sensors"]:
            sensor_list.append(GSsensor(sensor, api, settings))
        add_entities(sensor_list, True)

    subsensor_list = []
    for sensor in settings["connected_sensors"]:
        for con in settings[CONF_MON_CON]:
            subsensor_list.append(GSsubsensor(sensor, api, con, settings))
    add_entities(subsensor_list, True)

class GSsensor(Entity):
    """Representation of a Sensor."""

    def __init__(self, s_id, api, settings):
        """Initialize the sensor."""
        self._id = s_id
        self._unique_id = f"gs{s_id}"
        self._name = f"gs_{s_id}"
        self._api = api
        self._icon = "mdi:flower"
        self._settings = settings

        self._data = None
        self._state = None

        self._attr = {}
        self.update()

    def update_self(self):
        self._state = self._data["state"]
        for key, value in MAIN_SENSOR_ATTR.items():
            self._attr[value] = self._data[key]


    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def icon(self):
        return self._icon

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sun."""
        return self._attr

    @property
    def should_poll(self):
        return True

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("Updating %s", self._unique_id)
        update_data = self._api.return_data()[self._id]
        self._data = update_data
        self.update_self()


class GSsubsensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, s_id, api, s_type, settings):
        """Initialize the sensor."""
        self._id = s_id
        self._unique_id = f"gs{s_id}_{s_type}"
        self._name = f"gs_{s_id}_{s_type}"
        self._api = api
        self._type = s_type
        self._unit = SENSOR_TYPES[s_type][1]
        self._icon = "mdi:flower"
        self._settings = settings
        self._lang = self._settings[CONF_LANG]

        self._data = None
        self._state = None
        self._attr = {}


        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    def update_self(self):
        self._state = self._data[self._type]
        self._attr[SENS_ATTR_PLANT_NAME] = self._data[f"plantName{self._lang}"]
        for key, value in SENSOR_ATTR[self._type].items():
            self._attr[value] = self._data[key]
        for key, value in self._attr.items():
            if key in INT_LIST:
                self._attr[key] = int(value)
        
    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def icon(self):
        return self._icon

    @property
    def extra_state_attributes(self):
        """Return the state attributes of the sun."""
        return self._attr

    @property
    def should_poll(self):
        return True

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug("Updating %s", self._unique_id)
        update_data = self._api.return_data()[self._id]
        self._data = update_data
        self.update_self()
