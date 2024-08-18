import flights
import time
from apscheduler.schedulers.background import BackgroundScheduler

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(flights.get_flight_prices, 'interval', minutes=1)
    scheduler.start()

start_scheduler()
try:
    while True:
        time.sleep(35)
except (KeyboardInterrupt, SystemExit):
    pass
    
