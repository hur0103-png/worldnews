import re

with open("database.py", "r", encoding="utf-8") as f:
    code = f.read()

new_imports = """import sqlite3
import os
from datetime import datetime

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
"""

code = re.sub(r'import sqlite3\nimport os\nimport psycopg2\nfrom psycopg2.extras import RealDictCursor\nfrom datetime import datetime', new_imports, code)

with open("database.py", "w", encoding="utf-8") as f:
    f.write(code)
