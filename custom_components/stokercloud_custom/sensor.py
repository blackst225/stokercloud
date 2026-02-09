"""Sensor platform for StokerCloud Custom integration."""
import logging

from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up StokerCloud Custom sensors."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        StokerCloudSensor(
            coordinator,
            "Kesseltemperatur",
            "boiler_temp",
            "°C",
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][1]["2"][0]["0"],
        ),
        StokerCloudSensor(
            coordinator,
            "Puffertemperatur",
            "buffer_temp",
            "°C",
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][1]["2"][5]["5"],
        ),
        StokerCloudSensor(
            coordinator,
            "Abgastemperatur",
            "exhaust_temp",
            "°C",
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][1]["2"][2]["2"],
        ),
        StokerCloudSensor(
            coordinator,
            "Schafttemperatur",
            "shaft_temp",
            "°C",
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][1]["2"][1]["1"],
        ),
        StokerCloudSensor(
            coordinator,
            "Externe Puffertemperatur",
            "ext_buffer_temp",
            "°C",
            SensorDeviceClass.TEMPERATURE,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][1]["2"][6]["6"],
        ),
        StokerCloudSensor(
            coordinator,
            "Leistung",
            "power_kw",
            "kW",
            SensorDeviceClass.POWER,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][2]["4"][1]["1"],
        ),
        StokerCloudSensor(
            coordinator,
            "Leistung %",
            "power_pct",
            "%",
            SensorDeviceClass.POWER_FACTOR,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][2]["4"][0]["0"],
        ),
        StokerCloudSensor(
            coordinator,
            "Lambda Ist",
            "lambda_actual",
            "λ",
            None,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][2]["4"][2]["2"],
        ),
        StokerCloudSensor(
            coordinator,
            "Lambda Soll",
            "lambda_target",
            "λ",
            None,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][2]["4"][6]["6"],
        ),
        StokerCloudSensor(
            coordinator,
            "Lichtsensor",
            "light_sensor",
            "lx",
            SensorDeviceClass.ILLUMINANCE,
            SensorStateClass.MEASUREMENT,
            lambda data: data["jsondata"][2]["4"][3]["3"],
        ),
        StokerCloudSensor(
            coordinator,
            "Datum",
            "date",
            None,
            None,
            None,
            lambda data: data["jsondata"][3]["6"],
        ),
        StokerCloudModusSensor(coordinator),
        StokerCloudPumpSensor(coordinator),
    ]
    
    async_add_entities(sensors)


class StokerCloudSensor(CoordinatorEntity, SensorEntity):
    """Representation of a StokerCloud sensor."""

    def __init__(
        self,
        coordinator,
        name,
        unique_id_suffix,
        unit,
        device_class,
        state_class,
        value_func,
    ):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = f"StokerCloud {name}"
        self._attr_unique_id = f"{coordinator.username}_{unique_id_suffix}"
        self._attr_native_unit_of_measurement = unit
        self._attr_device_class = device_class
        self._attr_state_class = state_class
        self._value_func = value_func

    @property
    def native_value(self):
        """Return the state of the sensor."""
        try:
            return self._value_func(self.coordinator.data)
        except (KeyError, IndexError, TypeError):
            return None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.username)},
            "name": f"StokerCloud {self.coordinator.username}",
            "manufacturer": "NBE",
            "model": "StokerCloud Heizung",
        }


class StokerCloudModusSensor(CoordinatorEntity, SensorEntity):
    """Sensor for heating mode with Danish to German translation."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "StokerCloud Modus"
        self._attr_unique_id = f"{coordinator.username}_mode"

    @property
    def native_value(self):
        """Return the translated state."""
        try:
            value = self.coordinator.data["jsondata"][2]["4"][7]["11"]
            
            translations = {
                "Slukket": "AUS",
                "Slukket ekstern kontakt": "AUS",
                "Stoppet ekstern temperatur": "AUS über EXT Kontakt",
                "Drift": "EIN",
                "Optænding 1": "Zündung",
                "Fejl optænding": "Zündungsfehler",
                "Alarm ingen brændsel": "FEHLER KEINE FLAMME",
                "Stoppet - temperatur opnået": "Aus - Temperatur erreicht",
            }
            
            return translations.get(value, value)
        except (KeyError, IndexError, TypeError):
            return None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.username)},
            "name": f"StokerCloud {self.coordinator.username}",
            "manufacturer": "NBE",
            "model": "StokerCloud Heizung",
        }


class StokerCloudPumpSensor(CoordinatorEntity, SensorEntity):
    """Binary sensor for pump status."""

    def __init__(self, coordinator):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "StokerCloud Pumpe"
        self._attr_unique_id = f"{coordinator.username}_pump"

    @property
    def native_value(self):
        """Return pump state."""
        try:
            value = self.coordinator.data["jsondata"][2]["4"][14]["23"]
            return "EIN" if value == "1" else "AUS"
        except (KeyError, IndexError, TypeError):
            return None

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.coordinator.username)},
            "name": f"StokerCloud {self.coordinator.username}",
            "manufacturer": "NBE",
            "model": "StokerCloud Heizung",
        }
