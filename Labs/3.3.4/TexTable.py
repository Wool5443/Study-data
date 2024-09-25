import pandas as pd


def main():
    files = [
        "U(I)14.csv",
        "U(I)31.csv",
        "U(I)48.csv",
        "U(I)65.csv",
        "U(I)82.csv",
        "U(I)99.csv",
        "U(I)100Reversed.csv",
        "K(Isc).csv",
    ]

    tablesFile = open("Tables.txt", "w")

    for file in files:
        get_table(file, tablesFile)

    tablesFile.close()


def get_table(file: str, outFile):
    table = pd.read_csv(file)
    column_fomrat = '|' + '|'.join('r' * len(table)) + '|'
    print(
        table.to_latex(column_format=column_fomrat,
                       float_format='%.2e',
                       index=False),
        file=outFile
    )



if __name__ == '__main__':
    main()
