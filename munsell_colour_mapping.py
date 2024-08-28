
import pandas as pd

def get_munsell_dictionary(file_path_list:list,required_columns:list):
    """
    Return a python dictionary mapping munsell rock colour codes to RGB and L*A*B* data.

    Parameters:
    file_path_list(list): The relative file paths for csv files containing munsell colour data.
    required_columns(list): A list of column names. Each element can be a subset of the data's actual column name. 

    Returns:
    munsell_dict(dict): A dictionary mapping munsell rock colour codes to RGB and L*A*B* data.
    """
    munsell_df = create_munsell_dataframe(file_path_list,required_columns)
    munsell_dict = create_munsell_dictionary(munsell_df)
    return munsell_dict

def create_munsell_dataframe(file_path_list:list,required_columns:list):
    """
    Return a pandas dataframe where every row contains a munsell rock colour code and it's associated RGB and L*A*B* data.

    Parameters:
    file_path_list(list): The relative file paths for csv files containing munsell colour data.
    required_columns(list): A list of column names. Each element can be a subset of the data's actual column name. 

    Returns:
    munsell_df(pd.Dataframe): A dataframe where every row contains munsell codes, RGB and L*A*B* values. 
    """
    munsell_df = pd.DataFrame()
    for file_path in file_path_list:
        df = read_munsell_csv_data(file_path)
        df = df_column_filtering(df,required_columns)
        df = create_munsell_value_column(df)
        munsell_df = join_dataframes(munsell_df,df)
    return munsell_df

def create_munsell_dictionary(munsell_df:pd.DataFrame):
    """
    Return a dictionary mapping munsell rock colour codes to RGB and L*A*B* values from data in a pandas Dataframe.

    Parameters:
    munsell_df(pd.Dataframe): dataframe where every row contains a munsell rock colour code and it's associated RGB and L*A*B* data.

    Returns:
    munsell_dict(dict): A dictionary mapping munsell rock colour codes to RGB and L*A*B* data.
    """
    munsell_dict = {}
    for key,group in munsell_df.groupby('munsell'):
        lab  = group[['l*','a*','b*']].values.tolist()[0]
        rgb = group[['r','g','b']].values.tolist()[0]
        munsell_dict[key] = {'rgb':rgb,'lab':lab}
    return munsell_dict

def read_munsell_csv_data(file_path:str):
    """
    Read csv files containing munsell rock colour data.

    Parameters:
    file_path(str): The relative file path to the munsell rock colour csv data.

    Returns:
    df(pd.Dataframe): Raw munsell rock colour data stored in a pandas dataframe.

    Raises:
    FileNotFoundError: If the specified file paths don't lead to the csv data.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print('File Not Found Error: check file path')
        return None
    
def df_column_filtering(df:pd.DataFrame,required_columns:list):
    """
    Returns a subset of an origianl dataframe through filtering out unnecessary columns.

    Parameters:
    df(pd.Dataframe): Raw munsell rock colour data stored in a pandas dataframe.
    required_columns(list): A list of column names. Each element can be a subset of the data's actual column name.

    Returns:
    df(pd.Dataframe): Raw munsell rock colour data stored in a pandas dataframe with unnecessary columns dropped. 
    """
    df.columns = [column.strip().lower() for column in df.columns]
    column_subset = [column for column in df.columns if column in required_columns]
    return df[column_subset]

def create_munsell_value_column(df:pd.DataFrame):
    """
    Merges 3 columns of data into 1. The new column contains munsell rock colour codes as strings. 

    Parameters:
    df(pd.Dataframe): Raw munsell rock colour data stored in a pandas dataframe.

    Returns:
    df(pd.Dataframe): Raw munsell rock colour data stored in a pandas dataframe with new munsell colour code column.  
    """
    df['munsell'] = df['h'].astype(str) + ' ' + df['v'].astype(str) + ' ' + df['c'].astype(str)
    df = df.drop(columns = ['h','v','c'])
    return df

def join_dataframes(munsell_df:pd.DataFrame,df:pd.DataFrame):
    """
    Joins two panda datframes, each contain munsell rock colour data, on every unique munsell colour code.
    The function adds boolean conditions to ensure the join only occurs between correctly structured pandas dataframes. 
    Note that munsell_df is previous defined as a empty dataframe in a previous function and then passed into this function. 

    Parameters:
    munsell_df(pd.Dataframe): dataframe where every row contains a munsell rock colour code and it's associated RGB and L*A*B* data.
    df(pd.Dataframe): Raw munsell rock colour data stored in a pandas dataframe.

    Returns: 
    munsell_df(pd.Dataframe): dataframe where every row contains a munsell rock colour code and it's associated RGB and L*A*B* data.
    """
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
