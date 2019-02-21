""" Aggregate external data keyed by domain
"""

import os
import pandas as pd

# In
DIR_DATA = os.path.join('data')
FP_BIAS = os.path.join(DIR_DATA, 'bias_scores', 'bias_scores.csv')
FP_FAKE_NEWS = os.path.join(DIR_DATA, 'fake_news.tsv')

# Out
FP_DOMAINS = os.path.join(DIR_DATA, 'domains.tsv')

bias = pd.read_csv(FP_BIAS)
fakenews = pd.read_csv(FP_FAKE_NEWS, sep='\t')

bias.columns = ['domain'] + [f'bias_{c}' for c in bias.columns if c != 'domain']
fakenews.columns = ['domain'] + [f'fn_{c}' for c in fakenews.columns if c != 'domain']

# Unique domains
domain_set = set()
for df in [bias, fakenews]:
    domain_set |= set(df.domain)
print(f'Unique domains: {len(domain_set):,}')

# Merge all domain data
domains = bias.merge(fakenews, how='outer', on='domain')

# Save
domains.to_csv(FP_DOMAINS, index=False, sep='\t')

print(domains.head())
