""" News Classifications from Yin (2018) LocalNewsDataset

Source: https://github.com/yinleon/LocalNewsDataset

"""

import os
import utils # see https:/github.com/gitronald/utils
import pandas as pd

# Filepaths
DIR_DATA = os.path.join('data', 'domain_coding')
FP_IN = os.path.join(DIR_DATA,'local_news_dataset_2018_for_domain_analysis.csv')
FP_OUT = os.path.join('data', 'domain_coding', 'yin2018.csv')

# Load data
yin = pd.read_csv(FP_IN)

# Standardize domains and set all as news
yin['domain'] = yin['domain'].apply(utils.web.get_domain)
yin['is_news'] = 1

# Drop string column
mask = yin.domain == 'alaska broadcast television'
yin = yin[~mask]

# Exclude MySpace as a domain from this dataset
exclude_domains = ['myspace.com']
mask = yin.domain.isin(exclude_domains) 
yin.loc[mask, 'is_news'] = 0 

# Add column prefix
yin.set_index("domain", inplace=True)
yin = yin.add_prefix('yin_')

# Save
yin.to_csv(FP_OUT)
print(f'saved: {FP_OUT} - {yin.shape[0]:,}')
