import numpy as numpy
import matplotlib.pyplot as plt
import pandas as pd


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


    df_list = [ranked_deck_df, theorycraft_df, none_df, tournament_df]

    

        