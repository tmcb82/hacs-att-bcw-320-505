import aiohttp
from bs4 import BeautifulSoup

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
            "pon_link_status": self._extract_value(stats_html, "PON Link Status"),
            "broadband_connection": self._extract_value(stats_html, "Broadband Connection"),
            "ethernet_connection": self._extract_value(stats_html, "Line State"),
            "ethernet_link_speed": self._extract_value(stats_html, "Current Speed (Mbps)")
        }
        return data

    async def _get_html(self, url: str) -> str:
        async with self.session.get(url, timeout=10) as response:
            response.raise_for_status()
            return await response.text()

    def _extract_value(self, html: str, label: str) -> str | None:
        soup = BeautifulSoup(html, "html.parser")
        
        for tag in soup.find_all(["th", "td", "div", "span"]):
            text = tag.get_text(strip=True).strip(":")
            if text.lower() == label.lower():
                next_td = tag.find_next_sibling("td")
                
                if not next_td:
                    parent = tag.parent
                    if parent:
                        next_td = parent.find_next_sibling("td") or parent.find_next("td")
                        
                if next_td:
                    return next_td.get_text(strip=True)
                    
        return None

    async def test_connection(self) -> bool:
        try:
            await self._get_html(f"{self.base_url}/sysinfo.ha")
            return True
        except Exception:
            return False
