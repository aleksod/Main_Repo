#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 13:03:52 2017

@author: aleksod
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 13:03:52 2017

@author: aleksod
"""
import requests
from bs4 import BeautifulSoup
import pandas as pd
import gender_guesser.detector as gender
import pickle
import re
import string
import dateutil
import numpy as np
printable = set(string.printable)

url = 'http://www.boxofficemojo.com/yearly/chart/?page={}&view=releasedate&view2=domestic&yr={}&p=.htm'
urls = list()
for year in range(2017, 1979, -1):
    for page in range(1,11):
        urls.append(url.format(page, year))

domain = 'http://www.boxofficemojo.com'

def get_movie_value(soup, field_name):
    '''Grab a value from boxofficemojo HTML

    Takes a string attribute of a movie on the page and
    returns the string in the next sibling object
    (the value for that attribute)
    or None if nothing is found.
    '''
    try:
        obj = soup.find(text=re.compile(field_name))
        if not obj:
            return np.nan
        # this works for most of the values
        next_sibling = obj.findNextSibling()
        if next_sibling:
            return next_sibling.text
        else:
            return np.nan
    except:
        return np.nan

def to_date(datestring):
    try:
        date = dateutil.parser.parse(datestring)
        return date
    except:
        return np.nan

def money_to_int(moneystring):
    try:
        moneystring = moneystring.replace('$', '').replace(',', '')
        return int(moneystring)
    except:
        return np.nan

def runtime_to_minutes(runtimestring):
    try:
        if runtimestring == None:
            return np.nan
        runtime = runtimestring.split()
        try:
            minutes = int(runtime[0])*60 + int(runtime[2])
            return minutes
        except:
            return np.nan
    except:
        return np.nan

def get_movie_value_href(soup, field_name):
    '''Grab a value from boxofficemojo HTML
    
    Takes a string attribute of a movie on the page and
    returns the string in the next sibling object
    (the value for that attribute)
    or None if nothing is found.
    '''
    try:
        obj = soup.find_all('a', href=re.compile(field_name))
        if len(obj) == 0:
            return '| |' # None
        # this works for most of the values
        try:
            next_sibling = obj[1] #obj.findNextSibling()
        except IndexError:
            temp_list = [''.join([s for s in el.text if s in printable]) for el in soup.find_all(['td', 'th']) if el.text]
            indeces = [i for i,val in enumerate(temp_list) if val.startswith(field_name)]
    #         field_name_temp = field_name + ':'
            names_list = temp_list[indeces[0]+1].split()

            if len(names_list) == 1:
                return names_list[0]
            else:
                name_id = 0
                new_names_list = []
                while name_id < len(names_list):
                    split_name = nameSeparator(names_list[name_id])
                    if len(split_name) > 1:
                        if (
                            '.' in split_name[0]
                            ) or (
                            '-' in split_name[0]
                            ) or (
                            split_name[0] == split_name[0].upper() and
                            split_name[1] == split_name[1].upper()
                            ) or (
                            split_name[0] == 'Mc'
                            ) or (
                            split_name[0] == 'O'
                            ) or (
                            split_name[0] == 'Mac'
                            ) or (
                            split_name[0] == "O'"
                            ):
                            new_names_list.append(split_name[0] + split_name[1])
                        else:
                            new_names_list[name_id-1] = new_names_list[name_id-1] + ' ' + split_name[0]
                            new_names_list.append(split_name[1])
                    elif name_id == len(names_list)-1:
                        new_names_list[name_id-1] = new_names_list[name_id-1] + ' ' + split_name[0]
                    else:
                        new_names_list.append(split_name[0])
                    name_id += 1

            return new_names_list[0]

        if next_sibling:
            return next_sibling.text
        else:
            return '| |' # None

    except:
        return np.nan

def get_all_movie_value_href(soup, field_name):
    '''Grab a value from boxofficemojo HTML
    
    Takes a string attribute of a movie on the page and
    returns the string in the next sibling object
    (the value for that attribute)
    or None if nothing is found.
    '''
    try:
        obj = soup.find_all('a', href=re.compile(field_name))
        if len(obj) == 0:
            return [] # None
        # this works for most of the values
        try:
            next_sibling = obj[1] #obj.findNextSibling()
        except IndexError:
            temp_list = [''.join([s for s in el.text if s in printable]) for el in soup.find_all(['td', 'th']) if el.text]
            indeces = [i for i,val in enumerate(temp_list) if val.startswith(field_name)]
    #         field_name_temp = field_name + ':'
            names_list = temp_list[indeces[0]+1].split()

            if len(names_list) == 1:
                return names_list[0]
            else:
                name_id = 0
                new_names_list = []

                while name_id < len(names_list):
                    split_name = nameSeparator(names_list[name_id])
                    if len(split_name) > 1:
                        if (
                            '.' in split_name[0]
                            ) or (
                            '-' in split_name[0]
                            ) or (
                            split_name[0] == split_name[0].upper() and
                            split_name[1] == split_name[1].upper()
                            ) or (
                            split_name[0] == 'Mc'
                            ) or (
                            split_name[0] == 'O'
                            ) or (
                            split_name[0] == 'Mac'
                            ) or (
                            split_name[0] == "O'"
                            ):
                            new_names_list.append(split_name[0] + split_name[1])
                        else:
                            new_names_list[name_id-1] = new_names_list[name_id-1] + ' ' + split_name[0]
                            new_names_list.append(split_name[1])
                    elif name_id == len(names_list)-1:
                        new_names_list[name_id-1] = new_names_list[name_id-1] + ' ' + split_name[0]
                    else:
                        new_names_list.append(split_name[0])
                    name_id += 1

            return new_names_list

        if next_sibling:
            return next_sibling.text
        else:
            return [] # None

    except:
        return []
    
def nameSeparator(name):
    try:
        if re.findall('[A-Z][^A-Z]*', name) == []:
            return name
        else:
            return re.findall('[A-Z][^A-Z]*', name)
    except:
        return np.nan

rank = []
movie_title = []
studio = []
total_gross = []
total_gross_theaters = []
opening = []
opening_theaters = []
date_open = []
date_close = []
movie_page = []
release_year = []
genre = []
runtime = []
mpaa_rating = []
budget = []
director = []
director_gender = []
director_all = []
writer = []
writer_gender = []
writer_all = []
actor = []
actor_gender = []
actor_all = []
producer = []
producer_gender = []
producer_all = []
composer = []
composer_gender = []
composer_all = []

d = gender.Detector()
movie_counter = 1
for url in urls:
    try:
        response = requests.get(url)
        page = response.text
        soup = BeautifulSoup(page,"html5lib")

        if 'error' not in soup.find_all('td')[6].text:
            the_table = soup.find_all('table')[6]
            data = the_table.find_all('tr')[2:(len(the_table.find_all('tr'))-4)]

            for table_row in data:
                try:
                    link = domain + table_row.a['href']
                    response2 = requests.get(link)
                    page2 = response2.text
                    soup2 = BeautifulSoup(page2, "html5lib")

                    print(movie_counter, response.status_code, table_row.find_all('td')[1].text)

                    if response.status_code == 200:

                        try:
                            val_101 = get_movie_value(soup2, 'Genre:')
                            val_102 = runtime_to_minutes(get_movie_value(soup2, 'Runtime:'))
                            val_103 = get_movie_value(soup2, 'MPAA Rating:')
                            val_104 = get_movie_value(soup2, 'Production Budget:')

                            val_201 = get_movie_value_href(soup2, 'Director')
                            val_202 = d.get_gender(get_movie_value_href(soup2, 'Director').split()[0])
                            val_203 = get_all_movie_value_href(soup2, 'Director')

                            val_301 = get_movie_value_href(soup2, 'Writer')
                            val_302 = d.get_gender(get_movie_value_href(soup2, 'Writer').split()[0])
                            val_303 = get_all_movie_value_href(soup2, 'Writer')

                            val_401 = get_movie_value_href(soup2, 'Actor')
                            val_402 = d.get_gender(get_movie_value_href(soup2, 'Actor').split()[0])
                            val_403 = get_all_movie_value_href(soup2, 'Actor')

                            val_501 = get_movie_value_href(soup2, 'Producer')
                            val_502 = d.get_gender(get_movie_value_href(soup2, 'Producer').split()[0])
                            val_503 = get_all_movie_value_href(soup2, 'Producer')

                            val_601 = get_movie_value_href(soup2, 'Composer')
                            val_602 = d.get_gender(get_movie_value_href(soup2, 'Composer').split()[0])
                            val_603 = get_all_movie_value_href(soup2, 'Composer')

                            val_701 = domain + table_row.a['href']
                            val_702 = table_row.find_all('td')[0].text
                            val_703 = table_row.find_all('td')[1].text
                            val_704 = table_row.find_all('td')[2].text
                            val_705 = table_row.find_all('td')[3].text
                            val_706 = table_row.find_all('td')[4].text
                            val_707 = table_row.find_all('td')[5].text
                            val_708 = table_row.find_all('td')[6].text
                            val_709 = table_row.find_all('td')[7].text
                            val_710 = table_row.find_all('td')[8].text
                            val_711 = soup.head.text.split()[0]

                            genre.append(val_101)
                            runtime.append(val_102)
                            mpaa_rating.append(val_103)
                            budget.append(val_104)

                            director.append(val_201)
                            director_gender.append(val_202)
                            director_all.append(val_203)

                            writer.append(val_301)
                            writer_gender.append(val_302)
                            writer_all.append(val_303)

                            actor.append(val_401)
                            actor_gender.append(val_402)
                            actor_all.append(val_403)

                            producer.append(val_501)
                            producer_gender.append(val_502)
                            producer_all.append(val_503)

                            composer.append(val_601)
                            composer_gender.append(val_602)
                            composer_all.append(val_603)

                            movie_page.append(val_701)
                            rank.append(val_702)
                            movie_title.append(val_703)
                            studio.append(val_704)
                            total_gross.append(val_705)
                            total_gross_theaters.append(val_706)
                            opening.append(val_707)
                            opening_theaters.append(val_708)
                            date_open.append(val_709)
                            date_close.append(val_710)
                            release_year.append(val_711)

                        except:
                            pass

                    movie_counter += 1

                except:
                    pass
    except:
        pass

full_release_date = ["{}/{}".format(date_open_, release_year_) for date_open_, release_year_ in zip(date_open, release_year)]

data_list = [
        rank, 
        movie_title, 
        studio, 
        total_gross, 
        total_gross_theaters, 
        opening, 
        opening_theaters, 
        date_open, 
        date_close, 
        movie_page, 
        release_year, 
        genre, 
        runtime, 
        mpaa_rating, 
        budget, 
        director, 
        director_gender, 
        director_all, 
        writer, 
        writer_gender, 
        writer_all, 
        actor, 
        actor_gender, 
        actor_all, 
        producer, 
        producer_gender, 
        producer_all, 
        composer, 
        composer_gender, 
        composer_all
        ]

data_columns = [
        'rank', 
        'movie_title', 
        'studio', 
        'total_gross', 
        'total_gross_theaters', 
        'opening', 
        'opening_theaters', 
        'date_open', 
        'date_close', 
        'movie_page', 
        'release_year', 
        'genre', 
        'runtime', 
        'mpaa_rating', 
        'budget', 
        'director', 
        'director_gender', 
        'director_all', 
        'writer', 
        'writer_gender', 
        'writer_all', 
        'actor', 
        'actor_gender', 
        'actor_all', 
        'producer', 
        'producer_gender', 
        'producer_all', 
        'composer', 
        'composer_gender', 
        'composer_all'
        ]

movie_df = pd.DataFrame(data_list)
movie_df = movie_df.transpose()
movie_df.columns = data_columns

with open('movie_data.pkl', 'wb') as picklefile:
    pickle.dump(movie_df, picklefile)
picklefile.close()