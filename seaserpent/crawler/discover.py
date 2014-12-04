from unipath import Path
import sys
import os

PROJECT_DIR = Path(os.path.abspath(__file__)).parent.parent.parent
sys.path.append(PROJECT_DIR)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seaserpent.settings')

import django
django.setup()

import threading
from crawler import SubmarinoSerpent, AmericanasSerpent, ShoptimeSerpent

class Discover(threading.Thread):
    
    serpent = None

    def __init__(self, serpent):
        super(Discover, self).__init__()
        self.serpent = serpent

    def run(self):
        self.serpent.discover_products()

submarino = Discover(SubmarinoSerpent())
americanas = Discover(AmericanasSerpent())
shoptime = Discover(ShoptimeSerpent())

submarino.start()
americanas.start()
shoptime.start()
