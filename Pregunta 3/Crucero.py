import pandas as pd
import re
import string
import numpy as np


def standardise_column_names(df, remove_punct=True):
    """ Converts all DataFrame column names to lower case replacing
    whitespace of any length with a single underscore. Can also strip
    all punctuation from column names.

    Parameters
    ----------
    df: pandas.DataFrame
        DataFrame with non-standardised column names.
    remove_punct: bool (default True)
        If True will remove all punctuation from column names.

    Returns
    -------
    df: pandas.DataFrame
        DataFrame with standardised column names.
    Example
    -------
    >>> df = pd.DataFrame({'Column With Spaces': [1,2,3,4,5],
                           'Column-With-Hyphens&Others/': [6,7,8,9,10],
                           'Too    Many Spaces': [11,12,13,14,15],
                           })
    >>> df = standardise_column_names(df)
    >>> print(df.columns)
    Index(['column_with_spaces',
           'column_with_hyphens_others',
           'too_many_spaces'], dtype='object')
    """

    translator = str.maketrans(string.punctuation, ' ' * len(string.punctuation))

    for c in df.columns:
        c_mod = c.lower()
        if remove_punct:
            c_mod = c_mod.translate(translator)
        c_mod = '_'.join(c_mod.split(' '))
        if c_mod[-1] == '_':
            c_mod = c_mod[:-1]
        c_mod = re.sub(r'\_+', '_', c_mod)
        df.rename({c: c_mod}, inplace=True, axis=1)
    return df


df = pd.read_csv('crucero_1.csv', header=1)
df = df.dropna(axis=0, how='all')
df = df.dropna(axis=1, how='all')
df['yyyy-mm-ddThh:mm:ss.sss'] = df['yyyy-mm-ddThh:mm:ss.sss'].apply(pd.to_datetime)
df = df.fillna(method='ffill')


df = standardise_column_names(df)

df["id"] = df.groupby(df[['cruise', 'ship', 'station', 'yyyy_mm_ddthh_mm_ss_sss',
                          'longitude_degrees_east', 'latitude_degrees_north', 'bot_depth_m']]
                      .apply(frozenset, axis=1)).ngroup()

df2 = df.drop(['depth_m', 'fluorescence_wet_labs_eco_afl_fl_mg_m_3',
               'dissolved_oxygen_ml_l', 'temperature_deg_c', 'salinity_practical_psu'],
              axis=1)


df3 = df.drop(['cruise', 'ship', 'station', 'type', 'yyyy_mm_ddthh_mm_ss_sss',
              'longitude_degrees_east', 'latitude_degrees_north', 'bot_depth_m'], axis=1)


df4 = df3.set_index(['id', 'depth_m'])
df4 = df4.stack().rename_axis(['id', 'depth_m', 'variable']).rename('value').reset_index()


print(df)
print(df2)
print(df3)
print(df4)
print(df['cruise'].value_counts())

f = df
f['time'] = df['yyyy_mm_ddthh_mm_ss_sss'].dt.strftime('%H:%M:%S')
print(f['time'].value_counts())

X = df.groupby(df['cruise']).mean()
print(' La hora con mayor cantidad de datos es 14:51:00 ')
print('El crusero de 2018 tiene mas datos')
print('El promedio de las variables por profundidad es: ')
print(df3.groupby(pd.cut(df3["depth_m"], np.arange(0, 500, 10))).mean().drop('id', axis=1))
print('El promedio de las variables por años es: ')
print(X[['fluorescence_wet_labs_eco_afl_fl_mg_m_3', 'dissolved_oxygen_ml_l',
         'temperature_deg_c', 'salinity_practical_psu']])
