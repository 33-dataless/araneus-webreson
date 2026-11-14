
import asyncio
import logging
import os
import re
from pathlib import Path

from src.json_parser import JsonParser
from src.report import Report


log = logging.getLogger(__name__)


class Runner:
    def __init__(self, domain: str, ip: str):
        self.domain = domain
        self.ip = ip

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.path_tools = self.BASE_DIR / "tools" / "tools.json"
        self.path_report = self.BASE_DIR / "report"

        self.report = Report(self.path_report)
        self.jparser = JsonParser(self.path_tools)

        self.semaphore = asyncio.Semaphore(3)
        self.timeout = 120

    def has_root_permissions(self) -> bool:
        if os.name != "posix":
            return False

        return os.geteuid() == 0

    def get_target_variables(self) -> dict:
        return {
            "{domain}": self.domain,
            "{ip}": self.ip,
            "{url}": f"https://{self.domain}",
            "{http_url}": f"http://{self.domain}",
            "{https_url}": f"https://{self.domain}",
        }

    def create_query(self, tool: dict) -> list[str]:
        variables = self.get_target_variables()

        executable = tool["executable"]
        args = []

        for argument in tool["args"]:
            placeholders = re.findall(r"\{([^{}]+)\}", argument)

            for placeholder in placeholders:
                key = f"{{{placeholder}}}"

                if key not in variables:
                    raise ValueError(
                        f"Unknown placeholder '{key}' "
                        f"in tool '{tool['name']}'"
                    )

            for placeholder, value in variables.items():
                argument = argument.replace(placeholder, value)

            args.append(argument)

        return [executable, *args]

    async def execute_tool(self, tool: dict):
        tool_name = tool.get("name", "Unknown")
        tool_id = str(tool.get("id", "?"))

        stdout = ""
        stderr = ""
        status = "FAILED"

        async with self.semaphore:
            try:
                if tool.get("requires_root", False):
                    if not self.has_root_permissions():
                        status = "SKIPPED"
                        stderr = (
                            "This tool requires root privileges. "
                            "Run Araneus with --sudo."
                        )

                        log.warning(
                            "Tool %s skipped: root privileges required",
                            tool_name
                        )

                        return await self.report.write_report(
                            id=tool_id,
                            name=tool_name,
                            stdout=stdout,
                            stderr=stderr,
                            status=status
                        )

                query = self.create_query(tool)

                process = await asyncio.create_subprocess_exec(
                    *query,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )

                try:
                    stdout_bytes, stderr_bytes = await asyncio.wait_for(
                        process.communicate(),
                        timeout=self.timeout
                    )

                except asyncio.TimeoutError:
                    process.kill()
                    stdout_bytes, stderr_bytes = await process.communicate()

                    stdout = stdout_bytes.decode(
                        errors="replace"
                    )
                    stderr = stderr_bytes.decode(
                        errors="replace"
                    )

                    status = "TIMEOUT"
                    stderr += (
                        f"\nProcess exceeded timeout "
                        f"of {self.timeout} seconds."
                    )

                else:
                    stdout = stdout_bytes.decode(errors="replace")
                    stderr = stderr_bytes.decode(errors="replace")

                    if process.returncode == 0:
                        status = "SUCCESS"
                    else:
                        status = "FAILED"
                        stderr += (
                            f"\nProcess exited with code "
                            f"{process.returncode}."
                        )

            except FileNotFoundError as error:
                status = "FAILED"
                stderr = f"Executable not found: {error}"

            except PermissionError as error:
                status = "FAILED"
                stderr = f"Permission denied: {error}"

            except Exception as error:
                status = "FAILED"
                stderr = str(error)

            finally:
                log.info(
                    "Tool %s finished with status: %s",
                    tool_name,
                    status
                )

                try:
                    await self.report.write_report(
                        id=tool_id,
                        name=tool_name,
                        stdout=stdout,
                        stderr=stderr,
                        status=status
                    )
                except Exception:
                    log.exception(
                        "Failed to write report for tool %s",
                        tool_name
                    )

    async def runner(self):
        tools = await self.jparser.load_json()

        if not tools:
            log.warning("No tools configured")
            return

        await self.report.create_report_name()

        log.info("Starting scan for %s (%s)", self.domain, self.ip)

        tasks = [
            self.execute_tool(tool)
            for tool in tools.values()
        ]

        await asyncio.gather(*tasks)

        report_path = await self.report.get_report_file_path()

        log.info(
            "Scan completed. Report saved to: %s",
            report_path
        )
