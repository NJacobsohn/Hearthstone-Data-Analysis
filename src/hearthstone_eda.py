import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import scipy.stats as stats

plt.style.use('ggplot')

def read_data():
    '''Initializes the two, uncleaned dataframes'''
    unclean_df = pd.read_csv("data/hearthstone_decks.csv")
    json_df = pd.read_json("data/refs.json")
    return unclean_df, json_df

def deck_list_create(unclean_df):
    '''takes the deck dataframe and combines all the single card columns into a single columns with a list of dbfIds'''
    card_col_ls = ['card_{}'.format(i) for i in range(30)] #creates list of column names for cards
    big_card_df = pd.DataFrame(unclean_df[card_col_ls], columns=card_col_ls) #creates a new dataframe with JUST the card columns
    big_card_list = big_card_df.values.tolist() #makes list of lists of deck lists
    unclean_df['card_list'] = tuple(map(tuple, big_card_list)) #makes new column where each value in big_card_list is mapped from a list to a tuple
    unclean_df.drop(card_col_ls, axis=1, inplace=True) #drops single card lists in favor of the new listed one
    return unclean_df

def deck_dataframe_creation(unclean_df):
    '''creates dataframes for different important deck types, none needs to be cleaned'''
    ranked_deck_df = unique_column_split(unclean_df, 'deck_type', 'Ranked Deck')
    none_df = unique_column_split(unclean_df, 'deck_type', 'None')
    tournament_df = unique_column_split(unclean_df, 'deck_type', 'Tournament')
    return ranked_deck_df, none_df, tournament_df

def unique_column_split(df, col_str, value):
    '''Returns a new dataframe from a given column in the dataframe where each row contains the inputted value at inputted column'''
    return pd.DataFrame(df[df[col_str] == value])

def fill_with_na(data_frame, fill_dict):
    '''Fills NaN values in given dataframe according to dictionary input'''
    data_frame.fillna(value=fill_dict, inplace=True)
    return data_frame


def drop_rows(data_frame, removal_dict):
    '''Drops all rows from a given data frame where the col = key in removal dict and the value@col = value in removal_dict'''
    drop_set = set()
    for key, value in removal_dict.items():
        drop_set.update(set(data_frame[data_frame[key] == value].index))
    data_frame.drop(drop_set, inplace=True)
    return data_frame
    

def drop_cols(data_frame, cols_to_drop):
    '''Drops columns from given dataframe. cols are inputted as a list in cols_to_drop'''
    data_frame.drop(cols_to_drop, axis=1, inplace=True)
    return data_frame


def weapon_durability_fixing(json_data):
    '''Fixes weapons having "SPELL" as health rather than their durability value'''
    weapon_index = json_data[json_data['type'] == 'WEAPON'].index
    for i in weapon_index:
        json_data['health'][i] = json_data['durability'][i]
    return json_data['health']


if __name__ == '__main__':

    unclean_df, json_df = read_data()
    unclean_df = deck_list_create(unclean_df)
    ranked_decks, none_type, tournament = deck_dataframe_creation(unclean_df)
    df_list = [ranked_decks, none_type, tournament] #creates list of dfs to easily iterate future cleaning methods through them

    #defines dictionary for proper card.json NaN filling
    card_fill_dict = {
        'collectible' : 0, 
        'hideStats' : 0, 
        'race' : 'None', 
        'attack' : 'Spell',
        'health' : 'Spell',
        'durability' : 'None',
        'spellDamage' : 0,
        'overload' : 0,
        'text' : 'None',
        'referencedTags' : 'None',
        'mechanics' : 'None'
        } 

    #tells what rows to drop. Where col(key) == value
    card_row_drop_dict = {
        'collectible' : 0,
        'set' : 'HERO_SKINS',
        'type' : 'HERO'
    }

    #defines card.json cols to drop
    card_cols_to_drop = [
        'howToEarn',
        'howToEarnGolden',
        'playRequirements',
        'artist',
        'collectionText',
        'classes',
        'multiClassGroup',
        'hideStats',
        'targetingArrowText',
        'entourage',
        'elite',
        'faction',
        'flavor',
        'playerClass',
        'collectible', #shouldn't need this column assuming all cards in the df are correct
        'id' #this seems like an internal blizzard id, not the id we'll be using to create deck lists
        ]

    '''
    ORDER IS IMPORTANT HERE, MUST DO 
        1)FILL
        2)ROW DROP
        3)COL DROP
    '''
    #json_df = drop_cols(drop_rows(fill_with_na(json_df, card_fill_dict), card_row_drop_dict), card_cols_to_drop)

    #json_df['health'] = weapon_durability_fixing(json_df)


    


    #with the above code, the card DF should be as clean as it needs to be!

    #this code just makes a smaller dataframe with just the card ids and names, might be useful but also might be pointless
    card_id_df = pd.DataFrame()
    card_id_df['dbfId'], card_id_df['name'] = json_df['dbfId'], json_df['name']
    card_id_df.sort_values('dbfId', ascending=True, inplace=True)



    #starting below is code to clean the deck df

    #drops the deck_type column in important dfs as it's redundant info in the df
    #this sorts the data frame by deck rating in order to keep the highest rated copy of each deck
    for df in df_list: 
        df.drop('deck_type', axis=1, inplace=True)
        df.sort_values('rating', ascending=False, inplace=True) 
    
   
    
    #this drops all rows with duplicate decks, NOT using this for tournaments
    ranked_decks.drop_duplicates('card_list', inplace=True)
    none_type.drop_duplicates('card_list', inplace=True)
    
    for df in df_list:
        df['date'] = pd.to_datetime(df['date'])

    #makes dfs for each year, from here it's easier to work on a month by month standpoint
    ranked_decks_2014 = ranked_decks[ranked_decks['date'].map(lambda x: x.year == 2014)]
    ranked_decks_2014['month'] = ranked_decks_2014['date'].map(lambda x: x.month)
    ranked_decks_2015 = ranked_decks[ranked_decks['date'].map(lambda x: x.year == 2015)]
    ranked_decks_2015['month'] = ranked_decks_2015['date'].map(lambda x: x.month)
    ranked_decks_2016 = ranked_decks[ranked_decks['date'].map(lambda x: x.year == 2016)]
    ranked_decks_2016['month'] = ranked_decks_2016['date'].map(lambda x: x.month)
    ranked_decks_2017 = ranked_decks[ranked_decks['date'].map(lambda x: x.year == 2017)]
    ranked_decks_2017['month'] = ranked_decks_2017['date'].map(lambda x: x.month)

    tournament_2014 = tournament[tournament['date'].map(lambda x: x.year == 2014)]
    tournament_2015 = tournament[tournament['date'].map(lambda x: x.year == 2015)]
    tournament_2016 = tournament[tournament['date'].map(lambda x: x.year == 2016)]
    tournament_2017 = tournament[tournament['date'].map(lambda x: x.year == 2017)]


    #type_ls = list(unclean_df['deck_type'].unique()) #makes list of unique values
    #this is the main and most important df
        #ranked_deck_df = unique_column_split(unclean_df, 'deck_type', 'Ranked Deck') #SIZE= 202375, 184903 after dups 8.6%
    #not sure if this is important, might just drop it since it's so small
        #theorycraft_df = unique_column_split(unclean_df, 'deck_type', 'Theorycraft') #SIZE= 19688, 19438 after removing dups 1.3%
    #what even is this HUGE dataframe, needs cleaning and sorting
        #none_df = unique_column_split(unclean_df, 'deck_type', 'None') #SIZE= 91058, 83309 after removing dups 8.5%
    #tournament decks are maybe important? (tournament meta versus popular meta?)
        #tournament_df = unique_column_split(unclean_df, 'deck_type', 'Tournament') #SIZE= 3597, 2770 after remove 23% 
    

    # SET IDs
    '''
    {
        TGT : The Grand Tournament, 
        GANGS : Mean Streets of Gadgetzan, 
        CORE : Basic, 
        UNGORO : Journey to Un'Goro, 
        EXPERT1 : Classic, 
        HOF : Hall of Fame, 
        OG : Whispers of the Old Gods, 
        BRM : Blackrock Mountain, 
        GVG : Goblins versus Gnomes, 
        KARA : One Night in Karazhan, 
        LOE : League of Explorers, 
        NAXX : Naxxramus
    }
    '''



    #DECK DF MASTER COL LIST
    '''
    ['craft_cost', 'date', 'deck_archetype', 'deck_class', 'deck_format',
    'deck_id', 'deck_set', 'deck_type', 'rating', 'title', 'user', 'card_0',
    'card_1', 'card_2', 'card_3', 'card_4', 'card_5', 'card_6', 'card_7',
    'card_8', 'card_9', 'card_10', 'card_11', 'card_12', 'card_13', 'card_14', 
    'card_15', 'card_16', 'card_17', 'card_18', 'card_19', 'card_20', 'card_21', 
    'card_22', 'card_23', 'card_24', 'card_25', 'card_26', 'card_27', 'card_28', 
    'card_29']
    '''

    #DECK DF CURRENT COL LIST
    '''
    ['craft_cost', 'date', 'deck_archetype', 'deck_class', 'deck_format',
    'deck_id', 'deck_set', 'deck_type', 'rating', 'title', 'user', 'card_list']
    '''

    #JSON_DF MASTER COL LIST
    '''
    ['artist', 'attack', 'cardClass', 'classes', 'collectible',
    'collectionText', 'cost', 'dbfId', 'durability', 'elite', 'entourage',
    'faction', 'flavor', 'health', 'hideStats', 'howToEarn', 'howToEarnGolden', 'id', 'mechanics',
    'multiClassGroup', 'name', 'overload', 'playRequirements',
    'playerClass', 'race', 'rarity', 'referencedTags', 'set', 'spellDamage',
    'text', 'type'] 
    '''
    
    #JSON_DF CURRENT COL LIST
    '''
    ['attack', 'cardClass', 'cost', 'dbfId', 'durability',
    'health', 'mechanics', 'name', 'overload', 'race', 
    'rarity', 'referencedTags', 'set', 'spellDamage', 'text', 'type'] 
    '''

    

        