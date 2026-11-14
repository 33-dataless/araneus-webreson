from src.json_parser import JsonParser
from src.report import Report
from pathlib import Path

import subprocess
import logging 
log = logging.getLogger(__name__)

class Runner:
    def __init__(self, domain, ip):
        self.domain = domain
        self.ip = ip
        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.path_tools = self.BASE_DIR / "tools" / "tools.json"
        self.path_report = self.BASE_DIR / "report"
        self.report = Report(self.path_report)
        self.jparser = JsonParser(self.path_tools)

    def create_query(self, tool):
        query = f"{tool['executable']} {' '.join(tool['args'])}"
        query = query.replace("{domain}", self.domain)
        query = query.replace("{ip}", self.ip)    
        return query.split(" ")   

    async def runner(self):
        self.tools = await self.jparser.load_json()

        for tool in self.tools.values():
            query = self.create_query(tool)

            try:
                result = subprocess.run(query, capture_output=True, text=True, timeout=120)

                if result.stderr:
                    print(result.stderr)
                    raise RuntimeError(F"tool {tool['name']} return error")

            except Exception as error:
                log.error("exception run tool: %s", error)
                raise Exception('tool ' + tool['name'] + ' return error')
            
            try:
                await self.report.write_report(id=tool['id'], name=tool['name'], stdout=result.stdout)
                log.info("~ TOOL { %s } COMPLETED", str(tool["name"]))
            except Exception as error:
                log.error("exception write report: %s", error)
        else:
            log.info("all commands were successful, the final report is in %s", await self.report.get_report_file_path())    
        