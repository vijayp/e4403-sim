import constants
import income
import state


class Rules(object):
  def __init__(self):
    pass

  def NewState(self, state_obj, strat_obj, day_num):
    result = state.State()
    result.CopyFrom(state_obj)


    result.comps_cum_rd += constants.COMPS_DAILY_RD
    result.cum_rd+= strat_obj.DailyRD()
    result.cash_on_hand -= strat_obj.DailyRD()
    if strat_obj.DailyRD() > state_obj.last_days_rd:
      diff = strat_obj.DailyRD() - state_obj.last_days_rd
      result.cash_on_hand -=  (30.0 * diff) * .05
    result.last_days_rd = strat_obj.DailyRD()
    rd = strat_obj.DailyRD()

    result.comps_cum_mktg += constants.COMPS_DAILY_MKTG
    result.cum_mktg+= strat_obj.DailyMktg()
    result.cash_on_hand -= strat_obj.DailyMktg()
    if strat_obj.DailyMktg() > state_obj.last_days_mktg:
      diff = strat_obj.DailyMktg() - state_obj.last_days_mktg
      result.cash_on_hand -=  (30.0 * diff) * .05
    result.last_days_mktg = strat_obj.DailyMktg()
    mktg = strat_obj.DailyMktg()

    # Raise stock
    if strat_obj.InvestorStock() > result.investor_stock:
      diff = strat_obj.InvestorStock() - result.investor_stock
      result.cash_on_hand += diff
      result.investor_stock = strat_obj.InvestorStock()

    if strat_obj.EmployeeStock() > result.employee_stock:
      result.employee_stock = strat_obj.EmployeeStock()

    ss_market_share = (
      (result.cum_rd / (result.cum_rd + result.comps_cum_rd)) +
      (result.cum_mktg) / (result.cum_mktg + result.comps_cum_mktg) +
      (result.employee_stock / (result.employee_stock + result.investor_stock + constants.FOUNDER_STOCK))
      ) / 3.0



    diff = ss_market_share - result.last_days_market_share

    # TOOD(dbentley): explain this code; it accounts for lag in market share
    new_diff = diff * .95
    new_diff_pct = new_diff* 2/(result.last_days_market_share + ss_market_share)
    if new_diff_pct < 0.05 and new_diff_pct > -0.05:
      market_share = ss_market_share
    else:
      market_share = ss_market_share - new_diff

    result.last_days_market_share = market_share
    sales = market_share * constants.MARKET_SIZE

    # Buy PP&E
    if strat_obj.PPAndE() > result.ppande:
      diff = strat_obj.PPAndE() - result.ppande
      result.cash_on_hand -= diff
      result.ppande = strat_obj.PPAndE()

    dep = result.ppande / (365.0 * 5)

    if sales > (result.ppande / 30.0):
      result.messages.append(
        'On day %d, wanted to make %d, but capacity was %d' %
        (day_num, sales, result.ppande / 30.0)
        )
      sales = (result.ppande / 30.0)

    cogs = sales * constants.COGS_PERCENT
    result.cash_on_hand -= cogs

    result.cash_queue = (result.cash_queue[1:] +
                         [sales])
    result.cash_on_hand += state_obj.cash_queue[0]

    result.cash_on_hand -= strat_obj.MonthlyBurnRate() / 30.0
    ops = strat_obj.MonthlyBurnRate() / 30.0

    if result.cash_on_hand <= 0.0:
      result.messages.append(
        'On day %d, cash_on_hand was negative: %d' %
        (day_num, result.cash_on_hand)
        )

    interest = result.cash_on_hand * constants.DAILY_INTEREST_RATE
    result.cash_on_hand += interest

    income_obj = income.IncomeStatement(
      sales, cogs, rd, mktg, ops, dep, interest)
    result.income_statement_queue.append(income_obj)
    if len(result.income_statement_queue) > constants.DAYS_PER_QUARTER:
      result.income_statement_queue = result.income_statement_queue[-constants.DAYS_PER_QUARTER:]

    # update optima

    result.cash_on_days.append(result.cash_on_hand)

    # max sales (on a monthly basis)
    if sales * 30 > result.max_sales_per_month:
      result.max_sales_per_month = sales * 30

    return result
