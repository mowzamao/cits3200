
import pandas as pd

def create_munsell_dictionary(file_path_list:list):
    munsell_dict = {}
    munsell_df = create_munsell_dataframe(file_path_list)
    for key,group in munsell_df.groupby('munsell'):
        lab  = group[['l*','a*','b*']].values.tolist()[0]
        rgb = group[['r','g','b']].values.tolist()[0]
        munsell_dict[key] = {'rgb':rgb,'lab':lab}
    return munsell_dict

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
        print("Error: join cannot occur,column names don't match")
        return None

def create_munsell_value_column(df:pd.DataFrame):
    df['munsell'] = df['h'].astype(str) + ' ' + df['v'].astype(str) + ' ' + df['c'].astype(str)
    df = df.drop(columns = ['h','v','c'])
    return df

def read_munsell_csv_data(file_path:str):
    try:
        df = pd.read_csv(file_path)
        df.columns = [column.strip().lower() for column in df.columns]
        column_subset= required_columns(df.columns,['l*','a*','b*','h','v','c','r','g','b'])
        df = df[column_subset]
        return df
    except FileNotFoundError:
        print('File Not Found Error: check file path')
        return None

def required_columns(current_columns,required_columns):
    return [column for column in current_columns if column in required_columns]

munsell_dict = create_munsell_dictionary(['munsell_data/real_CIELAB.csv','munsell_data/real_sRGB.csv'])
print(munsell_dict['10RP 1 2'])
