import importlib

Decorators = importlib.import_module(name="Decorators", package=".Decorators.py")

CountMainFuncs = importlib.import_module(name="CountMainFuncs", package=".CountMainFuncs.pyd")

def CountToNumber(numToStopAt, Interval = 1, numToStartAt = 1, PrintOutput = True):
    CountMainFuncs.CountToNumber(numToStopAt=numToStopAt, Interval=Interval, numToStartAt=numToStartAt, PrintOutput=PrintOutput)
def CountToNumberTimed(numToStopAt, Interval = 1, numToStartAt = 1, PrintOutput = True):
    @TimeFunc
    def ThrowawayFunc(): CountMainFuncs.CountToNumber(numToStopAt=numToStopAt, Interval=Interval, numToStartAt=numToStartAt, PrintOutput=PrintOutput)
    ThrowawayFunc()