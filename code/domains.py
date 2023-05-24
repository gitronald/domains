""" Aggregate external data keyed by domain
"""

import os
import pandas as pd

# In
DATA_DIR = os.path.join('data', 'domain_coding')
FP_NEWS = os.path.join(DATA_DIR, 'news.tsv')
FP_BIAS = os.path.join(DATA_DIR, 'robertson2018.csv')
FP_FAKE_NEWS = os.path.join(DATA_DIR, 'grinberg2019.tsv')

# Out
FP_DOMAINS = os.path.join(DATA_DIR, 'domains.tsv')

# Load data
bias = pd.read_csv(FP_BIAS)
news = pd.read_csv(FP_NEWS, sep='\t')
fakenews = pd.read_csv(FP_FAKE_NEWS, sep='\t')

# Unique domains
domain_set = set()
for df in [bias, news, fakenews]:
    domain_set |= set(df.domain)

# Merge all domain data
domains = news.merge(bias, how='outer', on='domain')
domains = domains.merge(fakenews, how='outer', on='domain')

# # Combine unreliable news columns - no NewsGuard in public release
# domains['fake_either'] = (
#     (domains['fn_is_fake'] == 1) | 
#     (domains['newsguard_is_fake'] == 1)
# ).astype(float)

# Save -------------------------------------------------------------------------

domains.to_csv(FP_DOMAINS, sep='\t', index=False)
print(f'saved: {FP_DOMAINS} - {domains.shape[0]:,}')
