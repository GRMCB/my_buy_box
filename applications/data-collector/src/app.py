from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import atexit
import time

logging.basicConfig(level=logging.DEBUG,
                      format='%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger(__name__)

def print_date_time():
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))


app = Flask(__name__)

scheduler = BackgroundScheduler()
scheduler.add_job(func=print_date_time, trigger="interval", seconds=10)
scheduler.start()

atexit.register(scheduler.shutdown)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')