import argparse, csv

def loadRanges(rangeFile):
    ranges = []
    with open(rangeFile) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            r = (row['st'], row['end'])
            ranges.append(r)
    return ranges

def findBatch(ranges, row, rangeCounter):
    t = row['time']
    st,end = ranges[rangeCounter]
    if t < st:
        return -1, rangeCounter
    if t > end:
        if batchCounter == -1:
            batchCounter = 0
        return batchCounter+1, rangeCounter+1
    return batchCounter, rangeCounter

def annBatches(day, station, ranges,
               initDataFile, outFile):
    rangeCounter = 0
    batchCounter = 0
    initTime = -1
    with open(initDataFile) as f, open(outFile, 'w') as fout:
        print('day\tstation\trawTime\trelTime\tbatch')
        reader = csv.DictReader(initDataFile, delimiter='\t')
        for row in reader:
            batchCounter, rangeCounter = findBatch(ranges, row, rangeCounter, batchCounter)
            if batchCounter != -1:
                initTime = row[time]
            if batch != -1:
                # fix this w/ datetime
                relTime = initTime - row['time']
                printLs = ( day, station, row['time'],
                            relTime, str(batchCounter) )
                print('\t'.join(printLs), file=fout)

def main(args):
    ranges = loadRanges(args.rangeFile)
    annBatches(args.day, args.station, ranges,
               args.initData, args.outFile)

if __name__ == "__main__":
    desc = 'Apply range file to annotate time points with batches'
    parser = argparse.ArgumentParser(description=desc)
    argLs = ('day', 'station', 'rangeFile', 'initData', 'outFile',)
    for param in argLs:
        parser.add_argument(param)
    args = parser.parse_args()
    main(args)

