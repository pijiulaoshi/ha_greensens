"""custom component for GreenSens Api"""
import logging
from homeassistant.helpers.discovery import load_platform

from .const import *
#from .api import GreensensApi as gs

from pygreensens import GreensensApi as gs

_LOGGER = logging.getLogger(__name__)


def setup(hass, config):
    """Setup the GreenSens component."""
    entity_id = DOMAIN + ".status"
    try:
        _LOGGER.debug("GreenSens setting up!")
        conf = config[DOMAIN]
        username = conf.get(CONF_USER)
        password = conf.get(CONF_PASS)
        lang = conf.get(CONF_LANG)
        main_sensors = conf.get(CONF_MAIN_SENSORS)
        mon_con = conf.get(CONF_MON_CON, DEFAULT_MON_CON)
        
        api = gs(username, password)

        # data_coordinator = GreenSensData(hass, settings)
        sensors = api.return_sensors()

        domain_data = {}
        domain_data["sensors"] = sensors
        settings = {CONF_LANG: lang, CONF_MAIN_SENSORS: main_sensors, "connected_sensors": sensors ,CONF_MON_CON: mon_con}
        domain_data["settings"] = settings

        domain_data["mon_con"] = mon_con
        domain_data["api"] = api
        hass.data[DOMAIN] = domain_data

        hass.helpers.discovery.load_platform("sensor", DOMAIN, {}, config)
        hass.states.set(entity_id, "Active", settings)
        #### NOTHING BELOW THIS LINE ####
        # If Success:
        _LOGGER.info("GreenSens has been set up!")
        return True
        #################################
        # If Fail:
    except Exception as ex:
        hass.states.set(entity_id, "Error")
        _LOGGER.error(
            "Error while initializing GreenSens, exception: {}".format(str(ex))
        )
        hass.components.persistent_notification.create(
            f"Error: {str(ex)}<br />Fix issue and restart",
            title=NOTIFICATION_TITLE,
            notification_id=NOTIFICATION_ID,
        )
        return False
