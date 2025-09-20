print('Initialising')
import json
import pandas as pd
import numpy as np

import re
from wikipedia_scraper import fetch_wikipedia_page, search_wikipedia

data_path = 'data/'
raw_data_path = data_path+'raw_data/'

print('Importing Messy Data')
wru_yearly_breakdown_json = json.load(open(raw_data_path+'wru_yearly_breakdown_messy.json'))

print('Cleaning Data')
cleaned_dict = {}
for year, details in wru_yearly_breakdown_json.items():
    tournaments_dict = {}
    tournaments = details['tournaments']
    if tournaments == None:
        tournaments_dict = None
    else:
        matches = re.findall(r"\n(.*?)\n\n", tournaments, flags=re.DOTALL)
        for i, match in enumerate(matches):
            if match == '' or 'dates' in match.lower() or 'location' in match.lower():
                pass
            else:
                details_dict = {}
                if len(match.split('\n')) == 4:
                    details_dict['test_match_numbers'] = match.split('\n')[0]
                    details_dict['tournament_dates'] = match.split('\n')[1]
                    details_dict['tournament_name'] = match.split('\n')[2]
                    details_dict['tournament_location'] = match.split('\n')[3]
                elif len(match.split('\n')) == 3:
                    details_dict['tournament_dates'] = match.split('\n')[0]
                    details_dict['tournament_name'] = match.split('\n')[1]
                    details_dict['tournament_location'] = match.split('\n')[2]
                else:
                    for detail in match.split('\n'):
                        if str(year) in detail:
                            details_dict['tournament_dates'] = detail
                        elif detail.lower() != 'various':
                            if len(detail) > 0:
                                details_dict['tournament_name'] = detail
                            
                
                tournaments_dict[i] = details_dict

    other_matches_dict = {}
    other_matches = details['other_matches']
    for i, test in enumerate(re.findall(r"(.*)", other_matches)):
        test = test.replace('[a]', '')
        test = test.replace('[b]', '')
        test = test.replace(' [1]', '')
        test = test.replace(' [2]', '')
        test = test.replace(' [3]', '')
        if test != ''and 'main article' not in test.lower():
            match_dict = {}
            try:
                match_dict['match_date'] = re.findall(r"(\d{1,2}\s[a-zA-Z]*\s\d{4})", test)[0]
            except:
                match_dict['match_date'] = re.findall(r"(\?{1,2}\s\?{1,2}\s\d{4})", test)[0]
            try:
                match_dict['team_a'] = re.findall(fr"(?<={other_matches_dict['match_date']})(?:\[N 1\])?\s*?((?:[A-Z][a-z]*\s)?[a-zA-Z]*)", test)[0]
            except:
                match_dict['team_a'] = re.findall(r"(?<=\d{4})(?:\[N 1\])?\s*?((?:[A-Z][a-z]*\s)?[a-zA-Z]*)", test)[0]
                
            match_dict['score'] = re.findall(r"(\d{1,}–\d{1,})", test)[0]
            team_b =  re.findall(fr"(?<={match_dict['score']}\s).*?((?:[A-Z][a-z]*\s)?[A-Z][a-z]*)", test)[0]
            
            if team_b == 'World X':
                match_dict['team_b'] = 'World XV'
            else:
                match_dict['team_b'] = team_b

            if re.findall(r",\s?(.*)", test):
                match_dict['location'] = re.findall(r",\s?(\w*)[A-Z]?", test)[0]
            else:
                match_dict['location'] = re.findall(fr"(?<={match_dict['team_b']})\s?(.*)", test)[0]
            other_matches_dict[i] = match_dict
    
    cleaned_dict[year] = {'tournaments': tournaments_dict, 'other_matches' : other_matches_dict}

print('Saving Cleaned Data')
with open("data/cleaned_data/wru_yearly_breakdown_cleaned.json", "w") as jfile:
    json.dump(cleaned_dict, jfile)