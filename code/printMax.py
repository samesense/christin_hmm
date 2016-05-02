"""Limit high blocks to len 3.
   Report highest temp and time for it.
"""
import argparse, csv, copy

def main(args):
    currentState = '-1'
    batch = 1
    acc = []
    with open(args.hmmFile) as f, open(args.outFile, 'w') as fout:
        print('time\tthermo_temp\thighest\tbatch', file=fout)
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            state = row['state']
            if currentState != state:
                if state == 'high':
                    acc.append( (float(row['thermo_temp']), row['time'], batch ) )
                elif state == 'low':
                    if currentState == 'high' and len(acc) > 10 and max( [a[0] for a in acc] ) > 100:
                        highest = max( [a[0] for a in acc] )
                        for t,ts,batch in acc:
                            isHighest = t==highest
                            printLs = ( ts, str(t), str(isHighest), str(batch) )
                            print('\t'.join(printLs), file=fout)
                            batch += 1
                    acc = []
                currentState = state
            elif state == 'high':
                acc.append( (float(row['thermo_temp']), row['time'], batch ) )

if __name__ == "__main__":
    desc = 'Pull high intervals.'
    parser = argparse.ArgumentParser(description=desc)
    argLs = ('hmmFile', 'outFile',)
    for param in argLs:
        parser.add_argument(param)
    args = parser.parse_args()
    main(args)
