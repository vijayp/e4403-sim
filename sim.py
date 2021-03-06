#! /usr/bin/python


import sys


import constants
import rules
import state
import strategy
import strategies

def EvaluateStrategy(strat_obj):
  initial_state = state.State()
  rules_obj = rules.Rules()
  current_state = initial_state
  for day in range(constants.NUM_DAYS):
    day_strat = strat_obj.StrategyForDay(day, current_state)
    new_state = rules_obj.NewState(current_state, day_strat, day)
    current_state = new_state

  print '\t', current_state.DebugInfo()
  print strat_obj.Description(), current_state.FinalPrint()

def main(args):
  for s in strategies.STRATEGIES:
    EvaluateStrategy(s)


if __name__ == '__main__':
  main(sys.argv)
