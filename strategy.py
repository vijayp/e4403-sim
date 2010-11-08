import state


class Strategy(object):
  def __init__(self, rd=0, mktg=0, ppande=0, investor_stock=0,
               employee_stock=0):
    self.rd = rd
    self.mktg = mktg
    self.ppande = ppande
    self.investor_stock = investor_stock
    self.employee_stock = employee_stock

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

  def StrategyForDay(self, day_num, state_obj):
    return self


class AdaptiveStrategy(object):
  def __init__(self, rd=0, mktg=0, ppande=0, investor_stock=0,
               employee_stock=0):
    self.rd = rd
    self.mktg = mktg
    self.ppande = ppande
    self.investor_stock = investor_stock
    self.employee_stock = employee_stock
    self.cycles_since_mod = 10

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

  def StrategyForDay(self, day_num, state_obj):
    if day_num % 4 == 0:
      # look at capacity; do we need to increase it?
      cash_on_hand = state_obj.cash_on_hand

      capacity = state_obj.ppande / 30.0
      output = state_obj.income_statement_queue[-1].rev
      if capacity - output < 66:
        self.ppande += 4 * 1000
        cash_on_hand -= 4000

      # look at cash
      if cash_on_hand > 30000:
        self.rd += 100
        self.mktg += 100
        self.cycles_since_mod = 0
      elif cash_on_hand > 20000 and self.cycles_since_mod > 1:
        self.rd += 50
        self.mktg += 50
        self.cycles_since_mod = 0
      elif cash_on_hand < 10000:
        self.rd -= 100
        self.mktg -= 100
        self.cycles_since_mod = 0
      if day_num % 28 == 0:
        state_obj.messages.append(
          '[day %d: %d\t%d\t%d\t%d\t%d]' %
          (day_num,
           state_obj.cash_on_hand,
           state_obj.ppande/ 30.0,
           state_obj.income_statement_queue[-1].rev,
           state_obj.cash_on_days[0],
           self.rd))
      self.cycles_since_mod += 1
    return self


class TimedStrategy(object):
  def __init__(self, rules):
    self._rules = rules
    self._original_rules = rules
    self._current_strat = Strategy(*rules[0][1])

  def StrategyForDay(self, day_num, state_obj):
    if len(self._rules) == 1 or day_num < self._rules[1][0]:
      return self._current_strat.StrategyForDay(day_num, state_obj)
    state_obj.messages.append(
      '[day %d: %d\t%d\t%d\t%d]' %
      (day_num,
       state_obj.cash_on_hand,
       state_obj.ppande/ 30.0,
       state_obj.income_statement_queue[-1].rev,
       state_obj.cash_on_days[0]))
    self._rules = self._rules[1:]
    kwargs = self._current_strat.__dict__.copy()
    if 'cycles_since_mod' in kwargs:
      del kwargs['cycles_since_mod']
    kwargs.update(self._rules[0][1])
    if len(self._rules[0]) == 3:
      cls = self._rules[0][2]
    else:
      cls = Strategy
    self._current_strat = cls(**kwargs)
    return self._current_strat.StrategyForDay(day_num, state_obj)

  def Description(self):
    return str(self._original_rules)


