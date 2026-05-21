from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.const import UnitOfInformation
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from .const import DOMAIN

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        SoftwareVersionSensor(coordinator),
        UptimeSensor(coordinator),
        FiberLinkStatusSensor(coordinator),
        BroadbandConnectionSensor(coordinator),
        GBTransmittedSensor(coordinator),
        GBReceivedSensor(coordinator),
    ]
    async_add_entities(sensors)

class BGW320SensorBase(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator):
        super().__init__(coordinator)
        self._device_id = coordinator.client.host
        self._attr_device_info = {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": "AT&T BGW320 Router",
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

class FiberLinkStatusSensor(BGW320SensorBase):
    _attr_name = "Fiber Link Status"
    _attr_icon = "mdi:lan-connect"

    @property
    def unique_id(self):
        return f"{self._device_id}_fiber_link_status"

    @property
    def native_value(self):
        return self.coordinator.data.get("fiber_link_status")

class BroadbandConnectionSensor(BGW320SensorBase):
    _attr_name = "Broadband Connection"
    _attr_icon = "mdi:wan"

    @property
    def unique_id(self):
        return f"{self._device_id}_broadband_connection"

    @property
    def native_value(self):
        return self.coordinator.data.get("broadband_connection")

class GBTransmittedSensor(BGW320SensorBase):
    _attr_name = "GB Transmitted"
    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
    _attr_icon = "mdi:upload-network"

    @property
    def unique_id(self):
        return f"{self._device_id}_gb_transmitted"

    @property
    def native_value(self):
        val = self.coordinator.data.get("bytes_transmitted")
        if val and isinstance(val, str):
            try:
                bytes_int = int(val.replace(',', ''))
                return round(bytes_int / 1073741824, 2)
            except ValueError:
                return None
        return None

class GBReceivedSensor(BGW320SensorBase):
    _attr_name = "GB Received"
    _attr_device_class = SensorDeviceClass.DATA_SIZE
    _attr_native_unit_of_measurement = UnitOfInformation.GIGABYTES
    _attr_icon = "mdi:download-network"

    @property
    def unique_id(self):
        return f"{self._device_id}_gb_received"

    @property
    def native_value(self):
        val = self.coordinator.data.get("bytes_received")
        if val and isinstance(val, str):
            try:
                bytes_int = int(val.replace(',', ''))
                return round(bytes_int / 1073741824, 2)
            except ValueError:
                return None
        return None
