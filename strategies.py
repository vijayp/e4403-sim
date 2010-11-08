from strategy import *

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
