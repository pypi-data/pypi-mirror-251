#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ..dependencies import pd, Union, Dict 
from .nova_minute_by_minute import nova_minute_by_minute

def nova_concat(data_dict: Dict) -> pd.DataFrame:
    '''
    Concatenate the minute-by-minute data for each participant into a single DataFrame.

    This function takes a dictionary of minute-by-minute dataframes (`data_dict`) and concatenates them into a single DataFrame. The dictionary should be created using the `read_raw_nova_data` function. The Participant ID column is added at the beginning of the DataFrame to allow for sample-level analysis.

    Parameters
    ----------
    data_dict : Dict
        A dictionary containing Participant ID as keys and minute-by-minute dataframes as values.

    Returns
    -------
    pd.DataFrame
        A concatenated DataFrame containing minute-by-minute data for all participants.

    Example
    -------
    data_dict = {
        'Participant1': df1,
        'Participant2': df2,
        ...
    }
    concatenated_df = nova_concat(data_dict)
    '''

    frames = [] 

    for df_id, df in data_dict.items():
        try:
            df = nova_minute_by_minute(df, df_id)
            frames.append(df)
        except Exception as e:
            print(f'Error processing folder {df_id}: {e}')

    # Find the widest dataframe
    widest = max(frames, key=lambda x: x.shape[1])

    # Add the missing columns to each dataframe
    frames = [df.reindex(widest.columns, axis=1) for df in frames]

    # Concatenate the dataframes on the Participant ID and Time(sec) columns
    df = pd.concat(frames)

    return df