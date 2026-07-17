import importlib
import os
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class AppStartupTest(unittest.TestCase):
    def test_import_app_without_postgres(self):
        for key in [
            "DATABASE_URL",
            "USE_POSTGRES",
            "DB_USER",
            "DB_PASSWORD",
            "DB_HOST",
            "DB_PORT",
            "DB_NAME",
        ]:
            os.environ.pop(key, None)

        for module_name in ["main", "database", "models", "schemas"]:
            sys.modules.pop(module_name, None)

        main = importlib.import_module("main")

        self.assertTrue(hasattr(main, "app"))


if __name__ == "__main__":
    unittest.main()
