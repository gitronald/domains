""" Fake news classifications

Color-coded fake news domain classifications from this paper:
Grinberg et al. 2019. Fake news on Twitter during the 2016 U.S. presidential
election. Science, Vol. 363, Issue 6425, pp. 374-378. DOI: 10.1126/science.aau2706 

Classification data obtained from replication materials here:
https://doi.org/10.5281/zenodo.2483311

"""

import os
import re
import pandas as pd

# In data
DIR_DATA = os.path.join('data', 'domain_coding', 'data')
FP_BLACK_LIST = os.path.join(DIR_DATA, 'black_sites.txt')
FP_FAKE_NEWS_IN = os.path.join(DIR_DATA, 'Domain Codings.xlsx')

# Out data
FP_FAKE_NEWS_OUT = os.path.join('data', 'fake_news.tsv')

# Load data
blacklist = pd.read_csv(FP_BLACK_LIST, header=None)
blacklist[1] = 'black'
blacklist.columns = ['domain', 'color']

fakenews = pd.read_excel(FP_FAKE_NEWS_IN)
fakenews.columns = ['_'.join(re.split('\s+', c.lower())) for c in fakenews.columns]
fakenews.rename(columns={'likelihood_rating':'color'}, inplace=True)
fakenews['color'] = fakenews['color'].str.lower()
fakenews = fakenews[['domain', 'color']]

# Append black listed domains
fakenews = fakenews.append(blacklist, sort=False)

# Add an aggregate col
fakenews['is_fake'] = fakenews.color.isin(['black','red','orange'])

# Save
fakenews.to_csv(FP_FAKE_NEWS_OUT, index=False, sep='\t')
