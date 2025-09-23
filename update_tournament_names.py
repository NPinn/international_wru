print('Initialise')
import json
import pandas as pd
import numpy as np
from difflib import SequenceMatcher
from copy import deepcopy

import re
from wikipedia_scraper import fetch_wikipedia_page, search_wikipedia

print('Load Data')
wru_data_json = json.load(open("data/cleaned_data/wru_yearly_breakdown_cleaned.json"))

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

print('Search for Wikipedia Pages Names with Highest Similarities')
for year, details in wru_data_json.items():
    if details['tournaments'] != None:
        for i, tournament in details['tournaments'].items():
            search_name = year+' womens rugby '+tournament['tournament_name']
            search_results = search_wikipedia(search_name)
            
            sorted_list = deepcopy(search_results)
            sorted_list.sort()
            similarity_dict = {}
            
            similarity_dict['result'] = ''
            similarity_dict['similarity'] = 0
            for i in range(len(sorted_list)):
                result = sorted_list[i]
                
                if year in result:
                    similarity_1 = similar(result, tournament['tournament_name'])
                    if similarity_1 > similarity_dict['similarity']:
                        similarity_dict['result'] = result
                        similarity_dict['similarity'] = similarity_1
                        
                    similarity_2 = similar(result, year+' '+tournament['tournament_name'])
                    if similarity_1 > similarity_dict['similarity']:
                        similarity_dict['result'] = result
                        similarity_dict['similarity'] = similarity_2
                else:
                    if result == year+" Women's Rugby "+tournament['tournament_name']:
                        similarity = similar(result, year+" Women's Rugby "+tournament['tournament_name'])
                        if similarity > similarity_dict['similarity']:
                            similarity_dict['result'] = result
                            similarity_dict['similarity'] = similarity
                    elif result == year+' '+tournament['tournament_name']:
                        similarity = similar(result, year+' '+tournament['tournament_name'])
                        if similarity > similarity_dict['similarity']:
                            similarity_dict['result'] = result
                            similarity_dict['similarity'] = similarity
                    elif result == tournament['tournament_name']+' '+year:
                        similarity = similar(result, tournament['tournament_name']+' '+year)
                        if similarity > similarity_dict['similarity']:
                            similarity_dict['result'] = result
                            similarity_dict['similarity'] = similarity
                    elif result == year+" Women's "+tournament['tournament_name']:
                        similarity = similar(result, year+" Women's "+tournament['tournament_name'])
                        if similarity > similarity_dict['similarity']:
                            similarity_dict['result'] = result
                            similarity_dict['similarity'] = similarity
            
            tournament['wikipedia_page_name'] = similarity_dict['result']

print('Populate with additional specifics')
for year, details in wru_data_json.items():
    if details['tournaments'] != None:
        for i, tournament in details['tournaments'].items():
            if tournament['wikipedia_page_name'] == '':
                search_name = year+' womens rugby '+tournament['tournament_name']
                search_results = search_wikipedia(search_name)
                
                for result in search_results:
                    if tournament['tournament_name']+" (women's)"==result:
                        tournament['wikipedia_page_name'] = result
                    elif tournament['tournament_name']==result:
                        tournament['wikipedia_page_name'] = result

print('Manually Populate Remaining Details')
for year, details in wru_data_json.items():
    if details["tournaments"] != None:
        for i, tournament in details["tournaments"].items():
            if tournament["wikipedia_page_name"] == "":
                if year == "2000" and tournament["tournament_name"] == "Asian World Cup qualifier":
                    # Need to Extract #Qualifier Section
                    tournament["wikipedia_page_name"] = "2002 Women's Rugby World Cup"
                
                if year == "2002" and tournament["tournament_name"] == "FIRA ENC XV-a-side Tournament":
                    tournament["wikipedia_page_name"] = "2002 FIRA Women's European Nations Cup"
                
                if year == "2003" and tournament["tournament_name"] == "NAWIRA Caribbean Women's 15-a-side Championship":
                    tournament["wikipedia_page_name"] = "2003 NAWIRA Women's Rugby Championship"
                
                if year == "2005" and tournament["tournament_name"] == "Asian World Cup Qualifiers":
                    # Need to Extract #Qualifier Section
                    tournament["wikipedia_page_name"] = "2006 Women's Rugby World Cup"
                
                if year == "2006" and tournament["tournament_name"] == "Pacific tri-nations":
                    tournament["wikipedia_page_name"] = "Women's Pacific Tri-Nations"
                
                if year == "2009" and tournament["tournament_name"] == "FIRA European Trophy (World Cup Qualifier)":
                    tournament["wikipedia_page_name"] = "2009 FIRA Women's European Trophy"
                
                if year == "2009" and tournament["tournament_name"] == "Asia World Cup Qualifier":
                    # Need to Extract #Asian Qualifier Section
                    tournament["wikipedia_page_name"] = "2010 Women's Rugby World Cup qualifying"
                
                if year == "2010" and tournament["tournament_name"] == "Caribbean Women's Championship":
                    # Need to Extract #Carribian Section
                    tournament["wikipedia_page_name"] = "2010 NACRA Women's Rugby Championship"
                
                if year == "2011" and tournament["tournament_name"] == "Asian Championship (II Division)":
                    tournament["wikipedia_page_name"] = "2011 ARFU Development Cup"
                
                if year == "2012" and tournament["tournament_name"] == "Asian Championship (II Division)":
                    tournament["wikipedia_page_name"] = "2012 ARFU Development Cup"
                
                if year == "2013" and tournament["tournament_name"] == "ARFU Women's Rugby Championship":
                    tournament["wikipedia_page_name"] = "2013 Asia Women's Four Nations"
                
                if year == "2013" and tournament["tournament_name"] == "Africa World Cup Qualification":
                    # Need to Extract #African Qualifier Section
                    tournament["wikipedia_page_name"] = "2014 Women's Rugby World Cup qualifying"
                
                if year == "2016" and tournament["tournament_name"] == "2016 Oceania Rugby Women's Championship, World Cup qualifier (Oceania)":
                    tournament["wikipedia_page_name"] = "2016 Oceania Rugby Women's Championship"
                
                if year == "2016" and tournament["tournament_name"] == "World Cup qualifier (Europe)":
                    tournament["wikipedia_page_name"] = "2016 Oceania Rugby Women's Championship"
                
                if year == "2016" and tournament["tournament_name"] == "Asia Pacific Championship World Cup qualifier (Repechage)":
                    # Need to Extract Reperchage Section
                    tournament["wikipedia_page_name"] = "2017 Women's Rugby World Cup qualifying"
                
                if year == "2019" and tournament["tournament_name"] == "Asian Championship qualifiers":
                    tournament["wikipedia_page_name"] = "2019 Asia Rugby Women's Championship Div 1"
                
                if year == "2020" and tournament["tournament_name"] == "2019 Oceania Championship World Cup qualifier (Oceania)":
                    tournament["wikipedia_page_name"] = "2019 Oceania Rugby Women's Championship"
                
                if year == "2020" and tournament["tournament_name"] == "World Cup qualifier (Americas)":
                    # Need to Extrect #Americas Section
                    tournament["wikipedia_page_name"] = "2021 Rugby World Cup qualifying"
                
                if year == "2021" and tournament["tournament_name"] == "RE World Cup Qualification Tournament World Cup qualifier (Europe)":
                    # Need to Extrect #Europe Section
                    tournament["wikipedia_page_name"] = "2021 Rugby World Cup qualifying"
                
                if year == "2024" and tournament["tournament_name"] == "2025 World Cup South America Qualifier":
                    # Need to Extrect #Americas Section
                    tournament["wikipedia_page_name"] = "2025 Women's Rugby World Cup qualifying"
                
                if year == "2025" and tournament["tournament_name"] == "Rugby Europe Conference":
                    tournament["wikipedia_page_name"] = "2025 Rugby Europe Women's Championship"


print('Save Data')
with open("data/cleaned_data/wru_yearly_breakdown_added_tournament_page_names.json", "w") as jfile:
    json.dump(wru_data_json, jfile)