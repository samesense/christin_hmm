"""Find limits of batch ranges in absolute time."""
import argparse, csv, xlrd
from datetime import datetime

def main(args):
    book = xlrd.open_workbook(args.xlsxFile)
    name = 'Untitled Report - Data'
    first_sheet = book.sheet_by_index(0)
    with open(args.outFile, 'w') as fout:
        print('time\tthermo_temp', file=fout)
        for row in range(0, first_sheet.nrows):
            temp = first_sheet.row_values(row)[3]
            if isinstance(temp, float):
                excelTime = xlrd.xldate_as_tuple(first_sheet.row(row)[1].value, book.datemode)
                myTime = datetime(*excelTime)
                print(str(myTime) + '\t' + str(temp), file=fout)

if __name__ == "__main__":
    desc = 'Find ranges for batches in each file.'
    parser = argparse.ArgumentParser(description=desc)
    argLs = ('xlsxFile', 'outFile',)
    for param in argLs:
        parser.add_argument(param)
    args = parser.parse_args()
    main(args)

