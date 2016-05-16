import os, csv, datetime

STATIONS = ('Banbury', 'Cal#1_in', 'mill', 'scratcher_out', 'scratcher_in', 'sheeter_in', 'sheeter_out')
STATIONS_NO_CALL = ('Banbury', 'mill', 'scratcher_out', 'scratcher_in', 'sheeter_in', 'sheeter_out')
STATIONS_NO_MILL = ('Banbury', 'Cal#1_in', 'scratcher_out', 'scratcher_in', 'sheeter_in', 'sheeter_out')
STATIONS_NO_SH = ('Banbury', 'Cal#1_in', 'mill', 'scratcher_out', 'scratcher_in', 'sheeter_in',)

DAYS = {'011316':STATIONS,
        '011916':STATIONS,
        '012016':STATIONS,
        '012116':STATIONS,
        '012216':STATIONS,
        '020116':STATIONS,
        '020216':STATIONS,
        '020416':STATIONS,
        '020516':STATIONS,
        '042716':STATIONS_NO_SH,
        '042816':STATIONS,
        '042916':STATIONS,
        '050616':STATIONS_NO_CALL}

#        '121415':STATIONS_NO_MILL,}

def loadDays():
    ls = [x.split('.')[0] for x in os.listdir('../data/')
          if 'xlsx' in x]
    return ls

rule parseData:
    input:  '../data/raw/{day}.xlsx'
    output: '../data/parsed/{day}'
    shell:  'python parseData.py {input} {output}'

rule hmm:
    input: '../data/parsed/{day}'
    output: '../work/ann/{day}'
    shell:  'python hmm.py {input} {output}'

rule findStarts:
    """Take start of batch as highest temp for new high region"""
    input:  '../work/ann/Banbury_{day}'
    output: '../work/ann_high/{Banbury}_{day}'
    shell:  'python printMax.py {input} {output}'

rule calcShift:
    """Using start from banbury files, find diff between initial starts"""
    input:  '../work/ann_high/Banbury_{day}',
            '../work/ann_high/{station}_{day}',
            '../work/ann/{station}_{day}'
    output: '../work/batchRanges/{station}_{day}',
            '../work/starts/{station}_{day}.txt'
    shell:  'python calcBatchRanges.py {wildcards.station} {input} {output}'

rule formatData:
    """Annotate batches using ranges."""
    input:  '../work/batchRanges/{station}_{day}',
            '../data/parsed/{station}_{day}',
    output: '../work/formatted/{station}_{day}'
    shell:  'python formatData.py {wildcards.day} {wildcards.station} {input} {output}'

def getStations(wc):
    return [ '../work/formatted/%s_%s' % (station, wc.day)
             for station in DAYS[wc.day] ]

rule collapseData:
    input: getStations
    output: '../out/{day}.tab'
    run:
        files = list(input)
        shell('head -1 %s > {output}' % (files[0],))
        for afile in files:
            shell('tail -n +2 {afile} >> {output}')

rule tmp:
    input: '../work/formatted/sheeter_in_042716'

rule all:
    input: expand( '../out/{day}.tab', day=DAYS )
