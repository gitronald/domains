""" News classifications

The following values are smaller than those listed in the paper because
it only considers unique domains, and some domains were repeated in each
dataset.

joseph2019.csv was provided by Kenny Joseph, and contains news classifications from Grinberg et al. (2019).

"""

import os
import numpy as np
import pandas as pd

def get_news_class(row):
    if row.isnull().all():
        return None
    elif (row == True).any():
        return True
    else:
        return False

DATA_DIR = os.path.join('data', 'domains')
FP_JOSEPH = os.path.join(DATA_DIR, 'joseph2019.csv') 
FP_BAKSHY = os.path.join(DATA_DIR, 'bakshy2015.csv')
FP_YIN = os.path.join(DATA_DIR, 'yin2018.csv')
FP_NEWS_OUT = os.path.join(DATA_DIR, 'news.tsv')

# Load data --------------------------------------------------------------------

joseph2019 = pd.read_csv(FP_JOSEPH)
newsguard = pd.read_csv(FP_NEWSGUARD)
bakshy2015 = pd.read_csv(FP_BAKSHY)
yin2018 = pd.read_csv(FP_YIN)

# Reshape and merge ------------------------------------------------------------

# Use joseph2019 aggregated datasets as base news
news = joseph2019.copy()

# Add Bakshy classifications
keep_cols = ['domain', 'bakshy_is_news']
news = news.merge(bakshy2015[keep_cols], how='outer', on='domain')
news.rename(columns={'bakshy_is_news':'bakshy'}, inplace=True)

# Add Yin classifications
keep_cols = ['domain', 'yin_is_news']
news = news.merge(yin2018[keep_cols], how='outer', on='domain')
news.rename(columns={'yin_is_news':'yin'}, inplace=True)

# Format
news.set_index('domain', inplace=True)
news = news.astype(float)

# Overall news classification based on a subset of data sources
use_cols = ['fakenews_proj', 'yin', 'bakshy']
news['n'] = news[use_cols].sum(axis=1)
news['is_news'] = (news.n > 0).astype(float)

prefix_cols = [f'news_{c}' for c in news]
news.columns = prefix_cols

# Save
news.to_csv(FP_NEWS_OUT, sep='\t')
print(f"saved: {FP_NEWS_OUT} - {news.shape[0]:,}")
