import argparse, csv, datetime

def loadRanges(rangeFile):
    ranges = []
    with open(rangeFile) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            r = (row['st'], row['end'])
            ranges.append(r)
    return ranges

def findBatch(ranges, row, rangeCounter, batchCounter):
    t = row['time']
    st,end = ranges[rangeCounter]
    if t < st:
        return -1, rangeCounter
    if t > end:
        if batchCounter == -1:
            batchCounter = 0
        return batchCounter+1, rangeCounter+1
    return batchCounter, rangeCounter

# 2016-02-05 06:45:00
fmt = '%Y-%m-%d %H:%M:%S'

def convertTemp(temp):
    z = (float(temp) * 9) / 5.0 + 32
    return str(z)

def annBatches(day, station, ranges,
               initDataFile, outFile):
    rangeCounter = 0
    batchCounter = -1
    initTime = -1
    with open(initDataFile) as f, open(outFile, 'w') as fout:
        print('day\tstation\trawTime\trelTime\tbatch\ttempF', file=fout)
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            #print(ranges[rangeCounter], row)
            newBatchCounter, newRangeCounter = findBatch(ranges, row, rangeCounter, batchCounter)
            if batchCounter != newBatchCounter:
                initTime = datetime.datetime.strptime(row['time'], fmt)
            if newBatchCounter != -1:
                # fix this w/ datetime
                thisTime = datetime.datetime.strptime(row['time'], fmt)
                relTime = (thisTime - initTime).total_seconds()
                printLs = ( day, station, str(row['time']).split()[1],
                            str(relTime), str(newBatchCounter),
                            convertTemp(row['thermo_temp']))
                print('\t'.join(printLs), file=fout)
            batchCounter = newBatchCounter
            rangeCounter = newRangeCounter
            if rangeCounter == len(ranges)+1:
                break

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

