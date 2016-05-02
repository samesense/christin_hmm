import os, csv, datetime

STATIONS = ('Banbury', 'Cal#1_in', 'mill', 'scratcher_out', 'scratcher_in', 'sheeter_in', 'sheeter_out')
DAYS = ('020516', '020216', '042916', '042816', ) #'042716'

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
    output: '../work/batchRanges/{station}_{day}'
    shell:  'python calcBatchRanges.py {wildcards.station} {input} {output}'

rule formatData:
    """Annotate batches using ranges."""
    input:  '../work/batchRanges/{station}_{day}',
            '../data/parsed/{station}_{day}',
    output: '../work/formatted/{station}_{day}'
    shell:  'python formatData.py {wildcards.day} {wildcards.station} {input} {output}'

rule collapseData:
    input: expand('../work/formatted/{station}_{{day}}', \
                  station = STATIONS)
    output: '../out/{day}.xls'
    run:
        files = list(input)
        shell('head -1 %s > {output}' % (files[0],))
        for afile in files:
            shell('tail -n +2 {afile} >> {output}')

rule tmp:
    input: '../work/ann_high/Banbury_020216'

rule all:
    input: expand( '../out/{day}.xls', day=DAYS )
