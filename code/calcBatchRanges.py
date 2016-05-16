import xlrd, argparse, datetime, csv
from collections import defaultdict

def loadHighs(highFile):
    highs = {}
    with open(highFile) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            highs[row['time']] = True
    return highs

def printBanburyRanges(highFile, initFile, outFile, outStartFile):
    """These ranges are easy b/c there's no shift."""
    highs = loadHighs(highFile)
    st, lastTime, lastState = '-1','-1','-1'
    with open(outFile, 'w') as fout, open(initFile) as f, open(outStartFile, 'w') as foutSt:
        print('st\tend', file=fout)
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            t = row['time']
            if t in highs:
                if lastState == '-1':
                    # first high seen
                    st = t
                    print(str(st), file=foutSt)
                elif lastState == 'low':
                    # new batch
                    end = lastTime
                    print(st + '\t' + end, file=fout)
                    st = t
                lastState = 'high'
            else:
                lastState = 'low'
            lastTime = t
        end = lastTime
        print(st + '\t' + end, file=fout)

# 2016-02-05 06:45:00
fmt = '%Y-%m-%d %H:%M:%S'

def loadStarts(highFile):
    batch2start = defaultdict(list)
    starts = []
    with open(highFile) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            if row['highest'] == 'True':
                st = datetime.datetime.strptime(row['time'], fmt)
                batch2start[row['batch']].append(st)

    batchKeys = [ int(x) for x in batch2start.keys() ]
    batchKeys.sort()
    for batch in batchKeys:
        starts.append( batch2start[ str(batch) ][0] )
    return starts

def findFirstHigh(thisStFile):
    """Get first high time from file."""
    with open(thisStFile) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            return datetime.datetime.strptime(row['time'], fmt)

def printRanges(banburyStFile, thisStFile, initFile, outFile, outStartFile):
    """Must apply shift"""
    banburyStarts = loadStarts(banburyStFile)
    firstHigh = findFirstHigh(thisStFile)
    with open(outStartFile, 'w') as fout:
        print(str(firstHigh), file=fout)
    shift = banburyStarts[0] - firstHigh
    shiftedStarts = [ st+shift for st in banburyStarts ]
    st, lastTime, batch = '-1','-1',-1
    with open(initFile) as f, open(outFile, 'w') as fout:
        print('st\tend', file=fout)
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            thisTime = datetime.datetime.strptime(row['time'], fmt)
            if batch == -1:
                #print('here', shiftedStarts[0] - thisTime, thisTime >= shiftedStarts[0])
                if thisTime >= shiftedStarts[0]:
                    batch = 0
                    st = thisTime
            elif batch+1 < len(shiftedStarts):
                if thisTime >= shiftedStarts[batch+1]:
                    # move to new batch
                    print(str(st) + '\t' + str(lastTime), file=fout)
                    st = thisTime
                    batch += 1
                # if batch+1 == len(shiftedStarts):
                #     break
            lastTime = thisTime
        if st != '-1':
            print(str(st) + '\t' + str(thisTime), file=fout)

def main(args):
    if args.station == 'Banbury':
        printBanburyRanges(args.banburyStFile, args.initFile, args.outFile,
                           args.outStartFile)
    else:
        printRanges(args.banburyStFile, args.thisStFile,
                    args.initFile, args.outFile, args.outStartFile)
#    i = 1/0

if __name__ == "__main__":
    desc = 'Pull significant read IDs.'
    parser = argparse.ArgumentParser(description=desc)
    argLs = ('station', 'banburyStFile', 'thisStFile',
             'initFile', 'outFile', 'outStartFile')
    for param in argLs:
        parser.add_argument(param)
    args = parser.parse_args()
    main(args)


