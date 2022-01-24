import asyncio
import json

from cock import build_entrypoint
from loguru import logger

from alco_map import VERSION
from alco_map.injector import register


async def amain():
    pass


def main(config):
    register(lambda: config, singleton=True, name="config")
    register(lambda: VERSION, singleton=True, name="version")
    logger.level("INFO")
    logger.info("alco-map service config: \n{}", json.dumps(config, indent=4, default=repr))
    asyncio.run(amain())


options = [
]

entrypoint = build_entrypoint(main, options, auto_envvar_prefix="ALCO_MAP", show_default=True)
if __name__ == "__main__":
    entrypoint(prog_name="alco-map")
