import asyncio
from src.logger import configure_logging
from service.manager import Manager

async def main():
    configure_logging()

    manager = Manager(domain="sushinadom-75.ru")
    await manager.runtime()
    
if __name__ == "__main__":
    asyncio.run(main())
