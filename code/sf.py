import os

def loadDays():
    ls = [x.split('.')[0] for x in os.listdir('../data/')
          if 'xlsx' in x]
    return ls

rule parseData:
    input:  '../data/{day}.xlsx'
    output: '../data/parsed/{day}'
    shell:  'python parseData.py {input} {output}'

rule hmm:
    input: '../data/parsed/{day}'
    output: '../work/ann/{day}'
    shell:  'python hmm.py {input} {output}'

rule pullHigh:
    input:  '../work/ann/{day}'
    output: '../work/ann_high/{day}'
    shell:  'python printMax.py {input} {output}'

rule all:
    input: expand( '../work/ann_high/{day}', day=loadDays() )
