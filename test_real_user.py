# -*- coding: utf-8 -*-
"""Simulate real user: zashed -> podpisalsya -> vybral den. Run: python3 test_real_user.py"""

import os

_script_dir = os.path.dirname(os.path.abspath(__file__))
_env_path = os.path.join(_script_dir, ".env")


def _load_env():
    if os.getenv("SHEETS_WEBAPP_URL"):
        return
    if os.path.isfile(_env_path):
        for enc in ("utf-8", "latin-1", "cp1251"):
            try:
                with open(_env_path, "r", encoding=enc) as f:
                    for line in f:
                        s = line.strip()
                        if s.startswith("SHEETS_WEBAPP_URL=") and "=" in s:
                            val = s.split("=", 1)[1].strip().strip('"\'')
                            if val and not val.startswith("#"):
                                os.environ["SHEETS_WEBAPP_URL"] = val
                                return
            except Exception:
                continue


_load_env()

import sheets

# Use ASCII status - will show in sheet as: zashed, podpisalsya, vybral_den
USER_ID = 123456789
USERNAME = "test_real_user"
FIRST_NAME = "Test User"
DAY_LABEL = "Day 1 (5 feb)"

def main():
    if not os.getenv("SHEETS_WEBAPP_URL"):
        print("ERROR: SHEETS_WEBAPP_URL not set")
        return
    print("Simulating real user flow...")
    ok1 = sheets.append_status(USER_ID, "zashed")
    ok2 = sheets.append_status(USER_ID, "podpisalsya")
    ok3 = sheets.append_subscription(user_id=USER_ID, username=USERNAME, first_name=FIRST_NAME)
    ok4 = sheets.append_status(USER_ID, "vybral_den", DAY_LABEL)
    if ok1 and ok2 and ok3 and ok4:
        print("OK! Check Google Sheet - user_id=%s, username=%s" % (USER_ID, USERNAME))
    else:
        print("ERROR: some writes failed: zashed=%s podpisalsya=%s sub=%s den=%s" % (ok1, ok2, ok3, ok4))

if __name__ == "__main__":
    main()
