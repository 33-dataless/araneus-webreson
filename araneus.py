
import asyncio
import logging

from src.logger import configure_logging
from cli.cli import Cli


async def main():
    configure_logging()

    cli = Cli()
    await cli.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Interrupted")
    except Exception:
        logging.exception("Araneus execution failed")
