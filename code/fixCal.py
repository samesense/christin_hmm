"""Rename lower-case call files to upper case."""
import os

for afile in os.listdir('../data/raw/'):
    print(afile[0])
    if afile[0] == 'c':
        print('here', afile)
        newFile = 'C' + afile[1:]
        cmd = 'mv "../data/raw/%s" "../data/raw/%s"' % (afile, newFile)
        os.system(cmd)
