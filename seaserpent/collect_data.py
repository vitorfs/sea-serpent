from sea_serpent import SeaSerpent
import time

serpent = SeaSerpent()
while True:
    serpent.collect_products()
    time.sleep(7200)