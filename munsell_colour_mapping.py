
import pandas as pd

def create_munsell_dataframe(file_path_list:list):
    munsell_df = pd.DataFrame()
    for file_path in file_path_list:
        df = read_munsell_csv_data(file_path)
        df = create_munsell_value_column(df)
        munsell_df = join_dataframes(munsell_df,df)
    
    return munsell_df

def join_dataframes(munsell_df:pd.DataFrame,df:pd.DataFrame):
    if munsell_df.empty:
        munsell_df = df
        return munsell_df
    elif 'munsell' in munsell_df.columns and 'munsell' in df.columns:
        munsell_df = pd.merge(munsell_df,df, on = 'munsell', how = 'inner')
        return munsell_df
    else:
        print("Error: join cannot occur as dataframe doesn't have munsell column")

def create_munsell_value_column(df:pd.DataFrame):
    df['munsell'] = df['h'].astype(str) + ' ' + df['v'].astype(str) + ' ' + df['c'].astype(str)
    df = df.drop(columns = ['h','v','c'])
    return df

def read_munsell_csv_data(file_path:str):
    try:
        df = pd.read_csv(file_path)
        df.columns = [column.strip().lower() for column in df]
        df = df.drop(columns=redundant_columns(df,['l*','a*','b*','h','v','c','r','g','b']))
        return df
    except FileNotFoundError:
        print('File Not Found Error: check file path')
        return None
    

def redundant_columns(df:pd.DataFrame,required_columns:list):
    current_columns = df.columns
    return [column for column in current_columns if column not in required_columns]

create_munsell_dataframe(['munsell_data/real_CIELAB.csv','munsell_data/real_sRGB.csv'])
