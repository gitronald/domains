"""Process Robertson 2018 data

Data from my previous project. Contains an aggregation of partisan bias scores from four sources, as well as scores developed in the paper.

"""

import os
import utils # see https:/github.com/gitronald/utils
import pandas as pd

DATA_DIR = os.path.join('data')
FP_BIAS_IN = os.path.join(DATA_DIR, 'bias_scores', 'bias_scores.csv')
FP_BIAS_OUT = os.path.join(DATA_DIR, 'robertson2018.csv')

# Load
bias = pd.read_csv(FP_BIAS_IN)

# Add prefix to partisan bias score column names
bias.set_index('domain', inplace=True)
bias = bias.add_prefix('bias_')

# Fix domains with URL params:
# 1. vyper.io?utm_source=
# 2. home.twibble.io?utm_source=twitter&utm_medium=social&utm_campaign=poweredby
#
# Looking into N shares, these urls were shared by 500 and 1400 unique 
# accounts, repectively, and neither domain exists in the dataset without 
# the parameters. Together this suggests that the score applies to the 
# domain, and not the domain + these specific parameters.
bias = bias.reset_index()
bias['domain'] = bias['domain'].apply(utils.web.get_domain)

# Drop duplicates after standardizing (removes domain:433 sites), keep 
# record/score with more unique accounts sharing it
bias = (bias.sort_values(['domain', 'bias_rounded_n_accts'])
        .drop_duplicates(subset=['domain'], keep='last'))

# Drop 
bias.set_index('domain', inplace=True)

# Save
bias.to_csv(FP_BIAS_OUT)
print(f'saved: {FP_BIAS_OUT} - {bias.shape[0]:,}')