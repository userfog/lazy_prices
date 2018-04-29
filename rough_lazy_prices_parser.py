import re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from numpy import linalg as LA

def find_dates(s):
    dateRegex  = r'(((january|february|march|april|may|june|july|august|september|october|november|december) ([0-9][0-9]|[0-9]), [0-9][0-9][0-9][0-9]))'
    allDates = re.findall(dateRegex, s, re.I)
    dateString = set(map(lambda x: x[1], allDates))
    return dateString

def find_comma_numbers(s):
    number_regex = r'(([0-9][0-9][0-9],[0-9][0-9][0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]|[0-9][0-9][0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]|[0-9][0-9],[0-9][0-9][0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]|[0-9],[0-9][0-9][0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]|[0-9][0-9][0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]|[0-9][0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]|[0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]|[0-9][0-9][0-9],[0-9][0-9][0-9]|[0-9][0-9],[0-9][0-9][0-9]|[0-9],[0-9][0-9][0-9]))'
    allNumbers = re.findall(number_regex, s, re.I)
    numberString = set(map(lambda x: x[1], allNumbers))
    return numberString

def clean_dates(s):
    allDates = find_dates(s)
    for dString in allDates:
        s = s.replace(dString, '')
    return s

def clean_comma_numbers(s):
    allNumbers = find_comma_numbers(s)
    for nString in allNumbers:
        s = s.replace(nString, '')
    return s

def process_section(fName):
    with open(fName) as f:
        s = f.read()
    s = s.replace('\n', '')
    clean = clean_dates(s)
    print(find_dates(clean))
    clean = clean_comma_numbers(clean)
    print(find_comma_numbers(clean))
    soup = BeautifulSoup(clean, 'html.parser')
    pTag = soup.findAll('p')
    d = {}
    for para in pTag:
        words = para.text.split(' ')
        keys = set(words)
        for k in keys:
            if k in d:
                d[k] = d[k] + 1
            else: 
                d[k] = 1
    return d

def compare_docs():
    d1 = process_section('10Q YR2015Q2 Item2.htm')
    d2 = process_section('10Q YR2016Q2 Item2.htm')
    df1 = pd.DataFrame(d1, index = [0]).T.reindex()
    df1.columns = ['count']
    df1['word'] = df1.index.values
    df2 = pd.DataFrame(d2, index = [0]).T.reindex()
    df2.columns = ['count']
    df2['word'] = df2.index.values
    combined = pd.merge(df1, df2, on = 'word', how = 'outer', suffixes = ['_2015Q2', '_2016Q2'])
    combined['count_2015Q2'] = np.where(pd.isnull(combined['count_2015Q2']), 0, combined['count_2015Q2'])
    combined['count_2016Q2'] = np.where(pd.isnull(combined['count_2016Q2']), 0, combined['count_2016Q2'])
    u = combined['count_2015Q2']
    v = combined['count_2016Q2']
    norm = np.dot(u,v) / (LA.norm(u, ord = 2) * LA.norm(v, ord = 2))
    return(norm)












