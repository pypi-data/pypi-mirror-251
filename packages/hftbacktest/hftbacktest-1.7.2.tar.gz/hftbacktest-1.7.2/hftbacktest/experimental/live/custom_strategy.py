import logging
import sys

import pandas as pd

from .livebroker import LiveBroker
from .ordermanager import OrderManager


def algo(hbt):
    while hbt.elapse(100_000):
        pass



def run():
    broker = LiveBroker('btcusdt')
    broker.connect()

    # Try/except just keeps ctrl-c from printing an ugly stacktrace
    try:
        algo(broker)
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

run()
