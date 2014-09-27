 # -*- coding: utf-8 -*-

# get a list of all professors teaching at Swiss institutions
# (from 'http://www.proff.ch')
# and save them in a .csv file
"""
Created on Wed May 28 16:35:12 2014

@author: stefan
"""

from bs4 import BeautifulSoup
from bs4.dammit import EntitySubstitution
import urllib2
import csv




def is_leaf(soup):
    """"
    Make us of the fact that class=formSubject 
    only shows up in the professor (leaf) pages
    """
    leaf_flags = soup.findAll('td', {'class' :'formSubject'}) #only shows up in leafs
    if not leaf_flags:
        #print('list is empty -> is not a leaf')
        return 0
    else:
        #print('list not empty -> is leaf')
        return 1
    
def read_data(soup,data):
    """
    If a professor belongs to multiple universities, only use the first one listed
    --> consider all data up to (& including) the first 'Homepage' field, then stop
    """
    n_entries_first_uni = 16
    #t = soup.findAll('td', {'class' :'formSubject'})
    interesting_tr = soup.findAll('tr',{'class' :'formBg'})
    #locate the table...
    row = []
    for tr in interesting_tr:
        interesting_td = tr.findAll('td',{'class' :'formSubject'});
        for td in interesting_td:
            #print td.string.strip().encode('utf8') #column name
            value = td.find_next_sibling('td').text.strip().encode('utf8')
            #print value
            if  (value== None):
                value = 'NA'
            row = row + [value]
            if (td.string.strip() == 'Homepage'):
                we_should_stop = 1
            else:
                we_should_stop = 0
        if (we_should_stop):
            break
    return row
    
    


def find_data (url,data):
    """
    follows the links in the website given by url to find all the faculty data
    writes the result into data
    """
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page);
    cur_dir = soup.find('td',{'class' : 'history'})
    if (cur_dir):
        print cur_dir.text.strip()
    if (not(is_leaf(soup))):
        links = soup.findAll('a',{'class':'list'})
        #follow the links
        for link in links:
            url = GLOBAL_URL + link.get('href')
            find_data(url,data)
    else:
        data.append(read_data(soup,data))
    return data
    
    
def write_to_csv(filename,data):
    with open(filename, 'w') as fp:
        a = csv.writer(fp, delimiter=';')
        a.writerows(data)
        

GLOBAL_URL = 'http://www.proff.ch'
start_URL = GLOBAL_URL + '/search.hierarchy.school.do'

data = [['Name','First Name','Sex','University','Information','Faculty','Institute',
            'Category of Professors','Title','Subjects','Address','Phone','Zip Code / Location',
            'E-Mail','Retired','Homepage']]

url = start_URL
data = find_data(url,data)
write_to_csv('faculty.csv',data)