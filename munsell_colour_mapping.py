
import pandas as pd

def get_munsell_dictionary(file_path_list:list,required_columns:list):
    munsell_df = create_munsell_dataframe(file_path_list,required_columns)
    munsell_dict = create_munsell_dictionary(munsell_df)
    return munsell_dict

def create_munsell_dataframe(file_path_list:list,required_columns:list):
    munsell_df = pd.DataFrame()
    for file_path in file_path_list:
        df = read_munsell_csv_data(file_path)
        df = df_column_filtering(df,required_columns)
        df = create_munsell_value_column(df)
        munsell_df = join_dataframes(munsell_df,df)
    return munsell_df

def create_munsell_dictionary(munsell_df:pd.DataFrame):
    munsell_dict = {}
    for key,group in munsell_df.groupby('munsell'):
        lab  = group[['l*','a*','b*']].values.tolist()[0]
        rgb = group[['r','g','b']].values.tolist()[0]
        munsell_dict[key] = {'rgb':rgb,'lab':lab}
    return munsell_dict

def read_munsell_csv_data(file_path:str):
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print('File Not Found Error: check file path')
        return None
    
def df_column_filtering(df:pd.DataFrame,required_columns:list):
    df.columns = [column.strip().lower() for column in df.columns]
    column_subset = [column for column in df.columns if column in required_columns]
    return df[column_subset]

def create_munsell_value_column(df:pd.DataFrame):
    df['munsell'] = df['h'].astype(str) + ' ' + df['v'].astype(str) + ' ' + df['c'].astype(str)
    df = df.drop(columns = ['h','v','c'])
    return df

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

munsell_dict = get_munsell_dictionary(['munsell_data/real_CIELAB.csv','munsell_data/real_sRGB.csv'],['l*','a*','b*','h','v','c','r','g','b'])
print(munsell_dict['10RP 1 2'])
