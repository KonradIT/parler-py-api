import fire
import sys, os

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from Parler import Parler

if __name__ == "__main__":

    fire.Fire(Parler)
