import argparse, csv, yahmm


def loadRows(datFile):
    ls = []
    with open(datFile) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            ls.append( float(row['thermo_temp']))
    return ls

def main(args):
    model = yahmm.Model(name='peaks')
    sequence = loadRows(args.datFile)
    emissionParams = { 'low':(30,10), 'high':(100,20) }
    low = yahmm.State( yahmm.NormalDistribution(*emissionParams['low']), name='low')
    high = yahmm.State( yahmm.NormalDistribution(*emissionParams['high']), name='high')

    # model.add_state(low)
    # model.add_state(high)

    model.add_transition(model.start, low, .8)
    model.add_transition(model.start, high, .2)

    model.add_transition(high, low, .2)
    model.add_transition(high, high, .8)

    model.add_transition(low, high, .2)
    model.add_transition(low, low, .7)

    model.add_transition(low, model.end, .1)

    model.bake()
    model.train([sequence])

    viterbi_prob, viterbi_path = model.viterbi(sequence)
    path = [ state[1].name for state in viterbi_path ]
    with open(args.outFile, 'w') as fout, open(args.datFile) as f:
        reader = csv.DictReader(f, delimiter='\t')
        i = 0
        for row in reader:
            print( i, path[i],  len(viterbi_path) )
            ls = (row['time'], row['thermo_temp'], path[i])
            print( '\t'.join(ls), file=fout )
            i += 1

if __name__ == "__main__":
    desc = 'Pull significant read IDs.'
    parser = argparse.ArgumentParser(description=desc)
    argLs = ('datFile', 'outFile',)
    for param in argLs:
        parser.add_argument(param)
    args = parser.parse_args()
    main(args)
