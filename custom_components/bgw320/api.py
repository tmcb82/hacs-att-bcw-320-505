async def fetch_data(self) -> dict:
        sysinfo_html = await self._get_html(f"{self.base_url}/sysinfo.ha")
        stats_html = await self._get_html(f"{self.base_url}/broadbandstatistics.ha")

        data = {
            "software_version": self._extract_value(sysinfo_html, "Software Version"),
            "uptime_seconds": self._extract_value(sysinfo_html, "Time Since Last Reboot"),
            "fiber_link_status": self._extract_value(stats_html, "Link Status"),
            "broadband_connection": self._extract_value(stats_html, "Broadband Connection"),
            "bytes_transmitted": self._extract_value(stats_html, "Transmit Bytes"),
            "bytes_received": self._extract_value(stats_html, "Receive Bytes")
        }
        return data