from Parler import Parler, models
from dotenv import load_dotenv
from pathlib import Path
import os
import sys

load_dotenv(dotenv_path='.parler.env')

parler = Parler(jst=os.getenv("JST"), mst=os.getenv("MST"), debug=False)

if sys.flags.interactive:
    print("`parler` method at your disposal.")
else:
    print("Run in interactive mode! python -i shell.py")
    sys.exit(0)