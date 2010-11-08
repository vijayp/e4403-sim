class IncomeStatement(object):
  def __init__(self, revenues, cogs, rd, mktg, ops, depreciation, interest):
    self.rev = revenues
    self.cogs = cogs
    self.rd = rd
    self.mktg = mktg
    self.ops = ops
    self.dep = depreciation
    self.interest = interest

  def Income(self):
    return (
      self.rev
      - self.cogs
      - self.rd
      - self.mktg
      - self.ops
      - self.dep
      + self.interest)


def Aggregate(stmts):
  rev = 0
  cogs = 0
  rd = 0
  mktg = 0
  ops = 0
  dep = 0
  interest = 0
  for s in stmts:
    rev += s.rev
    cogs += s.cogs
    rd += s.rd
    mktg += s.mktg
    ops += s.ops
    dep += s.dep
    interest += s.interest

  result = IncomeStatement(rev, cogs, rd, mktg, ops, dep, interest)
  return result
