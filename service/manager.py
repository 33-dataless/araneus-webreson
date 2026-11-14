from pathlib import Path

from src.utils import get_current_time
from src.get_ip_by_domain import get_ip_by_domain
from .runner import Runner
from tools.tools import Tools

class Manager:
    def __init__(self, domain):
        self.path_report = Path("report/")
        self.domain = domain

    async def runtime(self):
        self.ip = await get_ip_by_domain(self.domain)
        if self.ip is None:
            raise ValueError("socket cant find ip by domain")
        self.runner = Runner(domain=self.domain, ip=self.ip)
        await self.runner.runner()


        