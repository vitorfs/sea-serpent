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

class CollectData(threading.Thread):
    
    serpent = None
    number = 0
    total = 1

    def __init__(self, serpent, number = 0, total = 1):
        super(CollectData, self).__init__()
        self.serpent = serpent
        self.number = number
        self.total = total

    def run(self):
        self.serpent.collect_data(self.number, self.total)

CollectData(AmericanasSerpent(), 0, 3).start()
CollectData(AmericanasSerpent(), 1, 3).start()
CollectData(AmericanasSerpent(), 2, 3).start()

CollectData(SubmarinoSerpent(), 0, 3).start()
CollectData(SubmarinoSerpent(), 1, 3).start()
CollectData(SubmarinoSerpent(), 2, 3).start()

CollectData(ShoptimeSerpent(), 0, 3).start()
CollectData(ShoptimeSerpent(), 1, 3).start()
CollectData(ShoptimeSerpent(), 2, 3).start()