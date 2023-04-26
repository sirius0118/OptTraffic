import os
import sys
import time

from Scheduler.strategy import baseline, our, Random


def main(argv):
    argv[4] = int((int(argv[2]) + int(argv[3])) / int(argv[5])) * 2
    if argv[1] == 'baseline':
        strategy = baseline(int(argv[4]), int(argv[5]), int(argv[2]), int(argv[3]))
        strategy.Localize()
    elif argv[1] == 'our':
        strategy = our(int(argv[4]), int(argv[5]), int(argv[2]), int(argv[3]))
        strategy.Localize()
        time.sleep(30)
        strategy.TrafficAllocation()
    elif argv[1] == 'random':
        strategy = Random(int(argv[4]), int(argv[5]), int(argv[2]), int(argv[3]))
        strategy.Localize()
    elif argv[1] == 'TA':
        strategy = Random(int(argv[4]), int(argv[5]), int(argv[2]), int(argv[3]))
        # strategy.Localize()
        strategy.TrafficAllocation()


if __name__ == '__main__':
    main(sys.argv)






