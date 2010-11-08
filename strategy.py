import state


class Strategy(object):
  def __init__(self, rd=0, mktg=0, ppande=0, investor_stock=0,
               employee_stock=0):
    self.rd = rd
    self.mktg = mktg
    self.ppande = ppande
    self.investor_stock = investor_stock
    self.employee_stock = employee_stock

  def NewState(self, state_obj):
    result = state.State()
    result.CopyFrom(state_obj)
    return result

  def DailyRD(self):
    return self.rd * 1.0

  def DailyMktg(self):
    return self.mktg * 1.0

  def MonthlyBurnRate(self):
    return self.ppande * .1

  def PPAndE(self):
    return self.ppande

  def InvestorStock(self):
    return self.investor_stock

  def EmployeeStock(self):
    return self.employee_stock

  def Description(self):
    return '[%d\t%d\t%d\t%d\t%d]' % (
      self.DailyRD(), self.DailyMktg(),
      self.PPAndE(), self.InvestorStock(), self.EmployeeStock())

  def StrategyForDay(self, day_num):
    return self


class TimedStrategy(object):
  def __init__(self, rules):
    self._rules = rules
    self._original_rules = rules
    self._current_strat = Strategy(*rules[0][1])

  def StrategyForDay(self, day_num):
    if len(self._rules) == 1 or day_num < self._rules[1][0]:
      return self._current_strat
    self._rules = self._rules[1:]
    kwargs = self._current_strat.__dict__.copy()
    kwargs.update(self._rules[0][1])
    self._current_strat = Strategy(**kwargs)
    return self._current_strat

  def Description(self):
    return str(self._original_rules)


STRATEGIES = [
  Strategy(1000, 1000, 100 * 1000, 182 * 1000, 0),
  TimedStrategy([
    (0, (1000, 1000, 100 * 1000, 182 * 1000, 0)),
    (638, dict(rd=0.0, mktg=0.0)),
    ]),
  TimedStrategy([
    (0, (700, 700, 100 * 1000, 163 * 1000, 0)),
    (35, dict(rd=900.0, mktg=900.0)),
    (90, dict(rd=1000.0, mktg=1000.0)),
    (120, dict(rd=1100.0, mktg=1100.0, ppande=105 * 1000)),
    (150, dict(rd=1200.0, mktg=1200.0, ppande=110 * 1000)),
    (638, dict(rd=0.0, mktg=0.0)),
    ]),
  TimedStrategy([
    (0, (700, 700, 100 * 1000, 163 * 1000, 0)),
    (35, dict(rd=900.0, mktg=900.0)),
    (90, dict(rd=1100.0, mktg=1100.0)),
    (130, dict(rd=1133.0, mktg=1133.0)),
    (150, dict(rd=1200.0, mktg=1200.0, ppande=110 * 1000)),
    (500, dict(ppande=112 * 1000)),
    (578, dict(rd=2100.0, mktg=2100.0)),
    (638, dict(rd=0.0, mktg=0.0)),
    ]),
  TimedStrategy([
    (0, (700, 700, 70 * 1000, 158 * 1000, 0)),
    (30, dict(ppande=80 * 1000)),
    (35, dict(rd=900.0, mktg=900.0)),
    (55, dict(ppande=90 * 1000)),
    (85, dict(rd=1100.0, mktg=1100.0, ppande = 100 * 1000)),
    (150, dict(rd=1200.0, mktg=1200.0, ppande=110 * 1000)),
    (500, dict(ppande=112 * 1000)),
    (578, dict(rd=2500.0, mktg=2500.0)),
    (638, dict(rd=0.0, mktg=0.0)),
    ]),

  ]
