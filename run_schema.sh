#!/bin/bash
set -e
export DATABASE_URL="postgresql+asyncpg://omnibot:omnibot@localhost:5432/omnibot"
python3 -c "
import asyncio
from omnibot.db import create_schema
asyncio.run(create_schema())
print('Schema created')
"