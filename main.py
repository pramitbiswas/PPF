import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta as rd
import calendar


interest_rates = pd.read_csv('Interest_rates.csv')
trans = pd.read_csv('transactions.csv')
last_date = dt.datetime.now().date()

interest_rates['date'] = pd.to_datetime(interest_rates['date'], format='%d-%m-%Y')
trans['date'] = pd.to_datetime(trans['date'], format='%d-%m-%Y')
trans['amount'] = trans['amount'].multiply(-1)


start_date = trans['date'].dt.date[0].replace(day=1)

current_balance = 0
interests = []
tot_Int = 0


current_date = start_date
while (current_date <= last_date):
    current_interest_rate \
        = float(interest_rates[interest_rates['date'].dt.date
                               <= current_date].tail(1)['rate'])
    days_in_current_month = calendar.monthrange(current_date.year,
                                                current_date.month)[1]
    days_in_current_year = 366 if calendar.isleap(current_date.year) else 365

    trans_till_5th = trans[(trans['date'].dt.date >= current_date) &
                           (trans['date'].dt.date <= current_date.replace(day=5))
                           ]['amount'].sum()
    trans_till_end_4m_5th = trans[(trans['date'].dt.date >= current_date.replace(day=6)) &
                                  (trans['date'].dt.date <= current_date.replace(day=days_in_current_month))
                                  ]['amount'].sum()

    bal_on_5th = current_balance + trans_till_5th
    bal_on_end = bal_on_5th + trans_till_end_4m_5th
    current_balance = bal_on_end

    # minimum balance in PPF account between 5th and the end of each month.
    interests.append(
        # min(bal_on_5th, bal_on_end)
        # * days_in_current_month
        # * current_interest_rate/(100*days_in_current_year)
        min(bal_on_5th, bal_on_end)
        * current_interest_rate/(100*12)
    )

    current_date = current_date + rd(months=1)

    if current_date.month == 4:
        if last_date >= current_date.replace(month=3, day=31):
            Int = round(round(round(sum(interests), 2), 1))
            print(f"FY: {current_date.year}, interest: {Int}")
            current_balance += Int
            tot_Int += Int
        interests = []


print(f"Total balance: {current_balance}")
print(f"Invested: {trans['amount'].sum()}, Interest: {tot_Int}")
print(f"ratio: {round(trans['amount'].sum()*100/current_balance)}:{100-(round(trans['amount'].sum()*100/current_balance))}")