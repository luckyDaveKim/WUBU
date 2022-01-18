from datetime import date

from dateutil.relativedelta import relativedelta

from investar.DualMomentum import DualMomentum

target_time = date(2020, 7, 1)
term_month = 3
stock_count = 100

dm = DualMomentum()
rm_start_date = target_time.strftime("%Y-%m-%d")
rm_end_date = (target_time + relativedelta(months=term_month)).strftime("%Y-%m-%d")
rm = dm.get_rltv_momentum(rm_start_date, rm_end_date, stock_count)

am_start_date = (target_time + relativedelta(months=term_month, days=1)).strftime("%Y-%m-%d")
am_end_date = (target_time + relativedelta(months=term_month * 2)).strftime("%Y-%m-%d")
am = dm.get_abs_momentum(rm, am_start_date, am_end_date)
