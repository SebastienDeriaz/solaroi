import pandas as pd
import numpy as np

def main():

    df = pd.DataFrame()
    for file in ['./Fiez_Deriaz_01012021-31122021.xlsx', './Fiez_Deriaz_01012022-31122022.xlsx', './Fiez_Deriaz_01012023-27112023.xlsx']:
        df = pd.concat([df, pd.read_excel(file, index_col='Date et heure')])
    df.columns = [f"{c} {u}" for c, u in zip(df.columns, df.iloc[0, :])]
    df.drop('[dd.MM.yyyy HH:mm]', axis=0, inplace=True)
    df.index = pd.to_datetime(df.index)

    df.to_excel('Fiez_Deriaz_01012021-27112023.xlsx')

if __name__ == '__main__':
    main()