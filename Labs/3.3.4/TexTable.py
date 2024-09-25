import pandas as pd
from sys import argv


def main():
    if len(argv) < 2:
        print("Give .csv file")
        return
    table = pd.read_csv(argv[1])

    print(table.to_latex(column_format='|r|r|r|r|r|r|r|', float_format='%.2f'))


if __name__ == '__main__':
    main()
