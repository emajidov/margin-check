from db.connection import init_db, engine
from check.check import check_account_margin
import logging
import schedule

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    logging.info("Application started")
    # this method is needed to generate the tables in the first run
    init_db()
    # to connect database we need to have a db session object
    session = engine.connect()

    # since margin checks happens in every 10 minutes the application will run checks for all account in every 10 minutes
    schedule.every(10).seconds.do(check_account_margin, session)

    while True:
        schedule.run_pending()
