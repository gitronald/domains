# Replication script for generating web domains table

# Download and unzip external data sources
cd data
URL_BIAS='http://personalization.ccs.neu.edu/static/archive/bias_scores.tar.gz'
curl -o bias_scores.tar.gz $URL_BIAS
tar -xzvf bias_scores.tar.gz
rm bias_scores.tar.gz

URL_FAKE='https://github.com/LazerLab/twitter-fake-news-replication/trunk/domains/domain_coding'
svn export $URL_FAKE
cd -

# Install virtual environment and pkgs for csv and excel data
virtualenv venv --python=python3.6
source venv/bin/activate
pip install pandas xlrd

python3.6 code/fake_news.py
# Extract fake news data
# in:
#   data/domain_coding/data/black_sites.txt
#   data/domain_coding/data/Domain Codings.xlsx
# out:
#   data/fake_news.tsv

python3.6 code/aggregate_domains.py
# Merge all, keyed by domain
# in:
#   data/fake_news.tsv
#   data/bias_scores/bias_scores.csv
# out:
#   data/domains/domains.tsv

# deactivate