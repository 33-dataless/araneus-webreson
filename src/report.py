
import asyncio
from pathlib import Path

from src.utils import get_current_time


class Report:
    def __init__(self, path_report: Path):
        self.path_report = path_report
        self.path_report.mkdir(parents=True, exist_ok=True)

        self.current_report_file_path = None
        self.lock = asyncio.Lock()

    async def create_report_name(self):
        report_name = f"report_{get_current_time()}.txt"

        self.current_report_file_path = (
            self.path_report / report_name
        )

        return self.current_report_file_path

    async def get_report_file_path(self):
        return self.current_report_file_path

    async def write_report(
        self,
        id: str,
        name: str,
        stdout: str,
        status: str,
        stderr: str = ""
    ):
        async with self.lock:
            if self.current_report_file_path is None:
                await self.create_report_name()

            separator = f"\n{'=' * 15} {name} [ID: {id}] {'=' * 15}\n"

            content = (
                f"STATUS: {status}\n"
                f"{separator}"
                f"{stdout}\n"
            )

            if stderr:
                content += f"\nSTDERR:\n{stderr}\n"

            content += f"\n{'=' * 60}\n"

            with open(
                self.current_report_file_path,
                "a",
                encoding="utf-8"
            ) as file:
                file.write(content)
