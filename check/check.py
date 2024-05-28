from sqlalchemy.orm import Session
from db.models import CI050, CC050, Account, Member, Issue
from datetime import date, timedelta
from sqlalchemy import select, insert
import logging


def check_last_day_transaction(db: Session, account: Account):
    """
    This function checks the transaction of the member account with the first intraday transaction and closing
    transaction from yesterday. If the margin of the closing transaction and the first intraday transaction
     of the day are not equal then it will create an issue in the database.
    :param db: connection object
    :param account: account ID
    :return: None
    """
    logging.info("Checking for yesterday's closed transactions")
    yesterday = str(date.today() - timedelta(days=1))
    yesterday = "2020-05-11"  # replacing yesterday value to test data
    today = str(date.today())
    today = "2020-05-12"  # replacing today value to test data
    last_day_transactions: CC050 = db.execute(select(CC050).where(CC050.date == yesterday,
                                                                  CC050.account == account.id)).all()
    last_day_transaction = last_day_transactions[-1] if last_day_transactions else None
    if last_day_transaction:

        logging.debug("yesterday", last_day_transaction)

        today_first_transaction: CI050 = db.execute(select(CI050).filter(
            CI050.date == today,
            CI050.account == account.id,
            CI050.clearing_member == last_day_transaction.clearing_member,
            last_day_transaction.margin_type == CI050.margin_type).order_by(
            CI050.time_of_day)).all()
        today_first_transaction = today_first_transaction[0] if today_first_transaction else None

        logging.debug("today", today_first_transaction)
        if last_day_transaction.margin == today_first_transaction.margin:
            logging.info("Transactions match")
        else:

            issue = db.execute(select(Issue).where(Issue.cc050_id == last_day_transaction.id,
                                                   Issue.ci050_id == today_first_transaction.id)).all()

            if not issue:
                stmt = insert(Issue).values(
                    description="Yesterday's closed margin and today's first intraday margin does not match",
                    bank_id=account.bank_id,
                    account_id=account.id,
                    previous_margin=last_day_transaction.margin,
                    current_margin=today_first_transaction.margin,
                    cc050_id=last_day_transaction.id,
                    ci050_id=today_first_transaction.id)
                db.execute(stmt)
                db.commit()
            logging.info("Issue found in yesterday's closed margin and today's first intraday margin")

    else:
        logging.debug("No transaction found")


def check_closed_transaction(db: Session, account: Account):
    """
    This method is used to check closed transaction and last intraday transaction margin value.
    :param db: database connection object
    :param account: account to check
    :return: None
    """
    logging.info("Checking for today's closed transactions")
    current_day = str(date.today())
    current_day = "2020-05-11"  # replacing yesterday value to test data
    last_day_transactions: CC050 = db.execute(select(CC050).where(CC050.date == current_day,
                                                                  CC050.account == account.id)).all()
    last_day_transaction = last_day_transactions[-1] if last_day_transactions else None
    if last_day_transaction:

        logging.debug("yesterday", last_day_transaction)

        today_first_transaction: CI050 = db.execute(select(CI050).filter(
            CI050.date == current_day,
            CI050.account == account.id,
            CI050.clearing_member == last_day_transaction.clearing_member,
            last_day_transaction.margin_type == CI050.margin_type).order_by(
            CI050.time_of_day)).all()
        today_first_transaction = today_first_transaction[-1] if today_first_transaction else None

        logging.debug("today", today_first_transaction)
        if last_day_transaction.margin == today_first_transaction.margin:
            logging.info("Transactions match")
        else:

            issue = db.execute(select(Issue).where(Issue.cc050_id == last_day_transaction.id,
                                                   Issue.ci050_id == today_first_transaction.id)).all()

            if not issue:
                stmt = insert(Issue).values(
                    description="Current days last margin and closed account transaction does not match",
                    bank_id=account.bank_id,
                    account_id=account.id,
                    previous_margin=last_day_transaction.margin,
                    current_margin=today_first_transaction.margin,
                    cc050_id=last_day_transaction.id,
                    ci050_id=today_first_transaction.id)
                db.execute(stmt)
                db.commit()
            logging.info("Issue found in current days last margin and closed account transaction")

    else:
        logging.debug("No transaction found")


def check_account_margin(db: Session):
    """
    This method gets all the accounts for each member in db and checks transactions for each account.
    :param db: db connection object
    :return: None
    """
    logging.info("Starting margin check for each accounts...")
    members = db.execute(select(Member)).all()
    for member in members:
        accounts = db.execute(select(Account).where(Account.bank_id == member.id)).all()
        for account in accounts:
            check_last_day_transaction(db, account)
            check_closed_transaction(db, account)

    logging.info("Margin check completed for all accounts")
