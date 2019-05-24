import numpy as numpy
import matplotlib.pyplot as plt
import pandas as pd
import json


def unique_column_split(df, col_str, value):
    '''Returns a new dataframe from a given column in the dataframe where each row contains the inputted value at inputted column'''
    return pd.DataFrame(df[df[col_str] == value])


if __name__ == '__main__':
    unclean_df = pd.read_csv("data/hearthstone_decks.csv")
    card_col_ls = ['card_{}'.format(i) for i in range(30)] #creates list of column names for cards
    big_card_df = pd.DataFrame(unclean_df[card_col_ls], columns=card_col_ls) #creates a new dataframe with JUST the card columns
    clean_df = unclean_df.copy() #creates copy of unclean_df as backup/new work space
    clean_df['card_list'] = big_card_df.values.tolist() #makes new column where each value in big_card_df is compressed into a list for reach row
    clean_df.drop(card_col_ls, axis=1, inplace=True) #drops single card lists in favor of the new listed one

    #deck_type column has 7 types, going to put each type in its own df to properly separate them and make things easier to work through

    type_ls = list(clean_df['deck_type'].unique()) #makes list of unique values

    #tavern brawl decks don't need to be conisdered most likely
    #tavern_brawl_df = unique_column_split(clean_df, 'deck_type', type_ls[0]) #SIZE= 6360

    #this is the main and most important df
    ranked_deck_df = unique_column_split(clean_df, 'deck_type', type_ls[1]) #SIZE= 202375

    #not sure if this is important, might just drop it since it's so small
    theorycraft_df = unique_column_split(clean_df, 'deck_type', type_ls[2]) #SIZE= 19688

    #what even is this HUGE dataframe, needs cleaning and sorting
    none_df = unique_column_split(clean_df, 'deck_type', type_ls[3]) #SIZE= 91058

    #probably not a useful dataset given the EDA I'm trying to do
    #arena_df = unique_column_split(clean_df, 'deck_type', type_ls[4]) #SIZE= 14095

    #pve decks are NOT important
    #pve_adventure_df = unique_column_split(clean_df, 'deck_type', type_ls[5]) #SIZE= 9059

    #tournament decks are maybe important? (tournament meta versus popular meta?)
    tournament_df = unique_column_split(clean_df, 'deck_type', type_ls[6]) #SIZE= 3597


    df_list = [ranked_deck_df, theorycraft_df, none_df, tournament_df] #creates list of dfs to easily iterate cleaning methods through them

    json_df = pd.read_json("data/refs.json") #creates df of cards to index. DF is size=(3116 rows X 32 columns)
    #this needs a LOT of column cleaning + card cleaning. No rows can be removed (I think) due to creating issues with deck lists

    #column dropping
    cols_to_drop = [
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
        'flavor'
    ]
    json_df.drop(cols_to_drop, axis=1, inplace=True) #useless or redundant info
     

    #value cleaning
    json_df.fillna(value={'collectible' : 0, 'hideStats' : 0, 'race' : 'None'}, inplace=True) #replaces NaN with 0 to make it easier to index

    #row dropping test
    #this drops the rows but maintains the original index values of the rows!
    collectible0_index = json_df[json_df['collectible'] == 0].index 
    json_df.drop(collectible0_index, inplace=True) #this *SHOULD* remove all non-playable cards in the game
    #1206 rows now
    heroSkin_index = json_df[json_df['set'] == 'HERO_SKINS'].index
    json_df.drop(heroSkin_index, inplace=True) #removes alt heros from the list
    #1198 rows now

    '''
    set_id_ls = json_df['set'].unique().tolist()
    for id in set_id_ls:
        collect_sum = json_df[json_df['set'] == id]['collectible'].sum()
        collect_count = json_df[json_df['set'] == id]['collectible'].count()
        print("# of collectible cards in {} out of total = {} / {}".format(id, collect_sum, collect_count))
        ''' #code used to check proportion of collectible cards in each set

    # SET IDs
    #['TGT', 'GANGS', 'CORE', 'UNGORO', 'EXPERT1', 'HOF', 'OG', 'BRM',
    #   'GVG', 'KARA', 'LOE', 'NAXX']
    '''
    These columns need to be certain values for a card to actually exist
        collectible = 1

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
    ['attack', 'cardClass', 'collectible',
    'cost', 'dbfId', 'durability',
    'faction', 'flavor', 'health', 'id', 'mechanics',
    'name', 'overload', 'playerClass', 'race', 
    'rarity', 'referencedTags', 'set', 'spellDamage', 'text', 'type'] 
    '''

    

        