import constants
import income

class State(object):
  def __init__(self):
    self.cash_on_hand = constants.STARTING_CASH
    self.cum_rd = 0
    self.comps_cum_rd = 0
    self.last_days_rd = 0

    self.cum_mktg = 0
    self.comps_cum_mktg = 0
    self.last_days_mktg = 0

    self.ppande = 0

    self.investor_stock = 0
    self.employee_stock = 0

    self.cash_queue = [0] * constants.RECEIVABLE_DAYS
    self.income_statement_queue = []
    self.last_days_market_share = 0

    self.cash_on_days = []
    self.max_sales_per_month = 0

    self.messages = []

  def CopyFrom(self, other):
    self.cash_on_hand = other.cash_on_hand * 1.0
    self.cum_rd = other.cum_rd * 1.0
    self.comps_cum_rd = other.comps_cum_rd * 1.0
    self.last_days_rd = other.last_days_rd * 1.0

    self.cum_mktg = other.cum_mktg * 1.0
    self.comps_cum_mktg = other.comps_cum_mktg * 1.0
    self.last_days_mktg = other.last_days_mktg * 1.0

    self.ppande = other.ppande * 1.0

    self.investor_stock = other.investor_stock * 1.0
    self.employee_stock = other.employee_stock * 1.0

    self.cash_queue = other.cash_queue
    self.income_statement_queue = other.income_statement_queue
    self.last_days_market_share = other.last_days_market_share

    self.cash_on_days = other.cash_on_days
    self.max_sales_per_month = other.max_sales_per_month
    self.messages = other.messages

  def Print(self):
    return '$: %d' % (self.cash_on_hand)

  def DebugInfo(self):
    min_cash_amount = 1000 * 1000 * 1000
    min_cash_day = 0
    for (day, amount) in enumerate(self.cash_on_days):
      if amount < min_cash_amount:
        min_cash_amount = amount
        min_cash_day = day

    return '[min_cash=%d (day=%d), max_sales=%d]\n' % (
      min_cash_amount, min_cash_day,
      self.max_sales_per_month) + ('\n'.join(self.messages))


  def FinalPrint(self):
    lqi = income.Aggregate(self.income_statement_queue).Income()
    valuation = self.cash_on_hand + 40 * lqi
    own_pct = constants.FOUNDER_STOCK / (self.investor_stock + self.employee_stock + constants.FOUNDER_STOCK)
    founders_money = valuation * own_pct
    return '[$%d + 40 * %d = %d * %f = %d]' % (
      self.cash_on_hand,
      lqi,
      valuation,
      own_pct,
      founders_money)
