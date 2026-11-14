from pathlib import Path
from src.utils import get_current_time

class Report:
    def __init__(self, path_report: Path): 
        if path_report.exists():
            self.path_report = path_report
        else:
            print(path_report)
            raise FileExistsError(f"scripts cant find {path_report}, or u enter wrong path")
        self.current_report_file_path = None

    async def create_report_name(self):
        report_name = "report_" + get_current_time()
        self.current_report_file_path = report_name
        return report_name

    async def get_report_file_path(self):
        return self.current_report_file_path

    async def write_report(self, id: str, name: str, stdout: str):
        separator = "-"*10 + name + "-"*10 + f"  [id-{id}]"
        path = f"{self.path_report}/" + await self.create_report_name()
        with open(path, "a", encoding="utf-8") as file:
            file.write(separator)
            file.write(stdout)
            file.write(separator)

        