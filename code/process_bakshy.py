""" News Classifications from Bakshy et al. 2015

https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/AAI7VA

"""

import os
import re
import utils
import pandas as pd

# Filepaths
DIR_DATA = os.path.join('data', 'domains')
FP_IN = os.path.join(DIR_DATA, 'bakshy2015_top500.txt')
FP_OUT = os.path.join('data', 'domains', 'bakshy2015.csv')

# Load data
bakshy = pd.read_csv(FP_IN)

# Standardize domains
bakshy['domain'] = bakshy['domain'].apply(utils.web.get_domain)

# Drop duplicates by taking mean score (Bakshy has 5 cases of www + non-www)
# E.g. www.washingtonexaminer.com, 0.8124 and washingtonexaminer.com, 0.8285
cols = [c for c in bakshy if c != 'domain']
bakshy = bakshy.groupby("domain")[cols].mean()

# As in Guess 2021, we exclude platforms in this dataset, and also remove satire
bakshy['is_news'] = 1
exclude_domains = [
    'en.wikipedia.org', # wikipedia explicitly says they're not news
    'youtube.com', 'm.youtube.com', # platforms
    'amazon.com', 'twitter.com', 'vimeo.com',
    'theonion.com', # satire
    ]
mask = bakshy.index.isin(exclude_domains)
bakshy.loc[mask, 'is_news'] = 0

# Add column prefix
bakshy = bakshy.add_prefix('bakshy_')

# Save
bakshy.to_csv(FP_OUT)
print(f'saved: {FP_OUT} - {bakshy.shape[0]:,}')
