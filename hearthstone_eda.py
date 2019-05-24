import numpy as numpy
import matplotlib.pyplot as plt
import pandas as pd
import json

def read_data():
    '''Initializes the two, uncleaned dataframes'''
    unclean_df = pd.read_csv("data/hearthstone_decks.csv")
    json_df = pd.read_json("data/refs.json")
    return unclean_df, json_df

def deck_list_create(unclean_df):
    '''takes the deck dataframe and combines all the single card columns into a single columns with a list of dbfIds'''
    card_col_ls = ['card_{}'.format(i) for i in range(30)] #creates list of column names for cards
    big_card_df = pd.DataFrame(unclean_df[card_col_ls], columns=card_col_ls) #creates a new dataframe with JUST the card columns
    unclean_df['card_list'] = big_card_df.values.tolist() #makes new column where each value in big_card_df is compressed into a list for reach row
    unclean_df.drop(card_col_ls, axis=1, inplace=True) #drops single card lists in favor of the new listed one
    return unclean_df

def deck_dataframe_creation(unclean_df):
    '''creates dataframes for different important deck types, none needs to be cleaned'''
    ranked_deck_df = unique_column_split(unclean_df, 'deck_type', 'Ranked Deck')
    theorycraft_df = unique_column_split(unclean_df, 'deck_type', 'Theorycraft')
    none_df = unique_column_split(unclean_df, 'deck_type', 'None')
    tournament_df = unique_column_split(unclean_df, 'deck_type', 'Tournament')

    return ranked_deck_df, theorycraft_df, none_df, tournament_df

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
    '''drops columns from given dataframe. cols are inputted as a list in cols_to_drop'''
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

    ranked_decks, theorycraft, none_type, tournament = deck_dataframe_creation(unclean_df)

    df_list = [ranked_decks, theorycraft, none_type, tournament] #creates list of dfs to easily iterate future cleaning methods through them


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
        'collectible', # shouldn't need this column assuming all cards in the df are correct
        'id' #this seems like an internal blizzard id, not the id we'll be using to create deck lists
        ]

    #ORDER IS IMPORTANT HERE, MUST DO THIS ORDER
    json_df = drop_cols(drop_rows(fill_with_na(json_df, card_fill_dict), card_row_drop_dict), card_cols_to_drop)
    print(json_df.shape)
    json_df['health'] = weapon_durability_fixing(json_df)
    print(json_df.shape)



    #deck_type column has 7 types, going to put each type in its own df to properly separate them and make things easier to work through
    #type_ls = list(unclean_df['deck_type'].unique()) #makes list of unique values
    #tavern brawl decks don't need to be conisdered most likely
        #tavern_brawl_df = unique_column_split(unclean_df, 'deck_type', type_ls[0]) #SIZE= 6360
    #this is the main and most important df
        #ranked_deck_df = unique_column_split(unclean_df, 'deck_type', 'Ranked Deck') #SIZE= 202375
    #not sure if this is important, might just drop it since it's so small
        #theorycraft_df = unique_column_split(unclean_df, 'deck_type', 'Theorycraft') #SIZE= 19688
    #what even is this HUGE dataframe, needs cleaning and sorting
        #none_df = unique_column_split(unclean_df, 'deck_type', 'None') #SIZE= 91058
    #probably not a useful dataset given the EDA I'm trying to do
        #arena_df = unique_column_split(unclean_df, 'deck_type', type_ls[4]) #SIZE= 14095
    #pve decks are NOT important
        #pve_adventure_df = unique_column_split(unclean_df, 'deck_type', type_ls[5]) #SIZE= 9059
    #tournament decks are maybe important? (tournament meta versus popular meta?)
        #tournament_df = unique_column_split(unclean_df, 'deck_type', 'Tournament') #SIZE= 3597
    


    #code used to check proportion of collectible cards in each set
    '''
    set_id_ls = json_df['set'].unique().tolist()
    for id in set_id_ls:
        collect_sum = json_df[json_df['set'] == id]['collectible'].sum()
        collect_count = json_df[json_df['set'] == id]['collectible'].count()
        print("# of collectible cards in {} out of total = {} / {}".format(id, collect_sum, collect_count))
    ''' 
    

    # SET IDs
    '''
    ['TGT', 'GANGS', 'CORE', 'UNGORO', 'EXPERT1', 'HOF', 
    'OG', 'BRM', 'GVG', 'KARA', 'LOE', 'NAXX']
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

    

        