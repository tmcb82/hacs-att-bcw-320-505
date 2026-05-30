import re
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        SoftwareVersionSensor(coordinator),
        UptimeSensor(coordinator),
        PONLinkStatusSensor(coordinator),
        BroadbandConnectionSensor(coordinator),
        EthernetConnectionSensor(coordinator),
        EthernetLinkSpeedSensor(coordinator),
    ]
    async_add_entities(sensors)

class BGW320SensorBase(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._device_id = coordinator.client.host
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": "AT&T BGW320-505",
            "manufacturer": "Nokia",
            "model": "BGW320-505",
            "configuration_url": f"http://{self._device_id}",
        }

class SoftwareVersionSensor(BGW320SensorBase):
    _attr_name = "Software Version"
    _attr_icon = "mdi:cellphone-link"

    @property
    def unique_id(self):
        return f"{self._device_id}_software_version"

    @property
    def native_value(self):
        return self.coordinator.data.get("software_version")

class UptimeSensor(BGW320SensorBase):
    _attr_name = "Time Since Last Reboot"
    _attr_icon = "mdi:clock-outline"

    @property
    def unique_id(self):
        return f"{self._device_id}_uptime"

    @property
    def native_value(self):
        seconds_str = self.coordinator.data.get("uptime_seconds")
        if not seconds_str:
            return None
            
        try:
            total_seconds = int(seconds_str)
            days = round(total_seconds / 86400)
            return f"{days} day{'s' if days != 1 else ''}"
        except ValueError:
            return None

class PONLinkStatusSensor(BGW320SensorBase):
    _attr_name = "PON Link Status"
    _attr_icon = "mdi:lan-connect"

    @property
    def unique_id(self):
        return f"{self._device_id}_pon_link_status"

    @property
    def native_value(self):
        return self.coordinator.data.get("pon_link_status")

class BroadbandConnectionSensor(BGW320SensorBase):
    _attr_name = "Broadband Connection"
    _attr_icon = "mdi:wan"

    @property
    def unique_id(self):
        return f"{self._device_id}_broadband_connection"

    @property
    def native_value(self):
        return self.coordinator.data.get("broadband_connection")

class EthernetConnectionSensor(BGW320SensorBase):
    _attr_name = "Ethernet Connection"
    _attr_icon = "mdi:ethernet-cable"

    @property
    def unique_id(self):
        return f"{self._device_id}_ethernet_connection"

    @property
    def native_value(self):
        return self.coordinator.data.get("ethernet_connection")

class EthernetLinkSpeedSensor(BGW320SensorBase):
    _attr_name = "Ethernet Link Speed"
    _attr_native_unit_of_measurement = "Gbps"
    _attr_icon = "mdi:speedometer"

    @property
    def unique_id(self):
        return f"{self._device_id}_ethernet_link_speed"

    @property
    def native_value(self):
        val = self.coordinator.data.get("ethernet_link_speed")
        if val and isinstance(val, str):
            match = re.search(r"([\d\.]+)", val.replace(',', ''))
            if match:
                try:
                    mbps_float = float(match.group(1))
                    return round(mbps_float / 1000, 2)
                except ValueError:
                    return None
        return None
