import aiohttp
from bs4 import BeautifulSoup
import re

class BGW320Client:
    def __init__(self, host: str, session: aiohttp.ClientSession):
        self.host = host
        self.session = session
        self.base_url = f"http://{self.host}/cgi-bin"

    async def fetch_data(self) -> dict:
        sysinfo_html = await self._get_html(f"{self.base_url}/sysinfo.ha")
        stats_html = await self._get_html(f"{self.base_url}/broadbandstatistics.ha")

        data = {
            "software_version": self._extract_value(sysinfo_html, "Software Version"),
            "uptime_seconds": self._extract_value(sysinfo_html, "Time Since Last Reboot"),
            "fiber_link_status": self._extract_value(stats_html, "Link Status"),
            "bytes_transmitted": self._extract_value(stats_html, "Transmit Bytes"),
            "bytes_received": self._extract_value(stats_html, "Receive Bytes")
        }
        return data

    async def _get_html(self, url: str) -> str:
        async with self.session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.text()

    def _extract_value(self, html: str, label: str) -> str | None:
        soup = BeautifulSoup(html, "html.parser")
        label_tag = soup.find(string=re.compile(label, re.IGNORECASE))
        if label_tag:
            parent = label_tag.parent
            next_td = parent.find_next_sibling("td")
            if next_td:
                return next_td.get_text(strip=True)
        return None

    async def test_connection(self) -> bool:
        try:
            await self._get_html(f"{self.base_url}/sysinfo.ha")
            return True
        except Exception:
            return False