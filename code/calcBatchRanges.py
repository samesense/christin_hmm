import xlrd, argparse

def loadHighs(highFile):
    highs = {}
    with open(highFile) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            highs[row['time']] = True
    return highs

def printBanburyRanges(highFile, initFile, outFile):
    highs = loadHighs(highFile)
    st, lastTime, lastState = -1,-1,-1
    with open(outFile, 'w') as fout, open(initFile) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            t = row['time']
            if t in highs:
                if lastState == 'low':
                    # new batch range
            else:
                if lastTime == 'high':


def 

def main(args):
    if args.station == 'Banbury':
        printBanburyRanges(args.banburyStFile, args.initFile, args.outFile)
    else:
        printRanges(args.banburyStFile, args.initFile, args.outFile)

if __name__ == "__main__":
    desc = 'Pull significant read IDs.'
    parser = argparse.ArgumentParser(description=desc)
    argLs = ('station', 'banburyStFile', 'initFile', 'outFile',)
    for param in argLs:
        parser.add_argument(param)
    args = parser.parse_args()
    main(args)


