rule parseData:
    input:  '../data/Banbury_042916.xlsx'
    output: '../data/parsed/Banbury_042916'
    shell:  'python parseData.py {input} {output}'

rule hmm:
    input: '../data/parsed/Banbury_042916'
    output: '../work/Banbury_042916'
    shell:  'python hmm.py {input} {output}'
