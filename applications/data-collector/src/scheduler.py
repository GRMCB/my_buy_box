from apscheduler.schedulers.background import BackgroundScheduler

class Scheduler:

    def schedule(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(func=myJob, trigger="interval", seconds=10)
        scheduler.start()

    def myJob(self):
        print('I finally started')