# Hearthstone Data Analysis

## **Overview**
Hearthstone is a digital card game release by Blizzard Entertainment in 2014. It's a free to play game featuring many prominent characters from World of Warcraft. Hearthstone quickly became extremely popular due to having similar gameplay to Magic: The Gathering while also having a much lower barrier to entry. It has many facets that make it unique due to its electronic nature, such as:
- Creating random cards from a class and shuffling them into your deck
- Cards that replace your deck with a different one mid-match 
- A card that shuffles a copy of your opponents deck into your deck
It has many built in gamemodes, but the main mode, and the mode I'm looking at with regards to the data, is ranked play. The other modes are not as interesting to look at as many of them change weekly or involve playing solo. 

The basics of a game Hearthstone are as follows:
- Each player has a 30-card deck
- The deck type is chosen from 1 of 9 classes
- Each deck fundamentally contains a mix of two card types, minions and spells
- Minions are played on the board, and can be used to attack your opponent or their minions
- Spells are single use effects that can be used on a variety of targets, such as minions, your deck, your opponent, etc.

![Hearthstone Board][hs_board]

[hs_board]:https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/hearthstone_gameplay.png

The dataset was pulled from a popular deck sharing website called [hearthpwn](https://www.hearthpwn.com), and contains over 340,000 decks uploaded from the game's release until February of 2017. The dataset also contains a .json file with every card in the game and their attributes.

## **Questions**
- How did the popularity of Hearthstone change from its initial release as they released more content?
- What classes were popular/unpopular for each content change? Do they correspond at all with what the highest rated decks were?

## **Cleaning**
It's immediately obvious that there's a lot of bad data in here. The deck csv was a bit of a challenge. It started with 346,232 decks, with each card in the deck in it's own column. My first task was to take all 30 card columns, combine their values into a tuple, put that tuple in its own column, then drop the 30 individual columns. From there, I realized that the data also included decks from many of Hearthstone's special gamemodes, so I just wanted the decks that were made for ranked play. Now I've got a 202,375 row data frame of just decks in the ranked play mode, it's done right? Wrong. Keeping duplicate deck lists didn't seem very important as there were many copies of popular deck lists that were uploaded with little to no ratings. I sorted the data by ratings and dropped all duplicate decks with lower ratings, bringing the final data size to 184,903 decks.

With the card json, there was also a lot of dirty data, but it was easy to decide what to keep. Since any single player specific cards or even joke cards that you only see when you watch the credits of the game were also in this file, it had a lot of cards that literally would never show up in a ranked deck. While I didn't need to trim this data, I wanted to make the frame as small as possible to increase processing time. The most important thing I wanted to do was reduce the columns, as each card contained 31 columns of data. I was able to cut this down to 16 important columns,which was after dropping all columns with irrelevant or redundant data.

## **Visualization**
What I really wanted to know about this data (as a former player) is how balance updates to certain cards or new releases affect what is played or popular. As a starting point, this is the total amount of deck uploads per content update.
![Uploads per Patch][patch_uploads]

[patch_uploads]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/deck_uploads_per_patch.png

One could gather that the Explorers and Old Gods content releases were the most popular. While this might be interesting to look as for someone who's played the game before, I want to also show how each of these compared to uploads throughout the overall timeline of the game.

![Patch versus Month][patch_versus_month]

[patch_versus_month]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/month_versus_patch.png

This shows the total amount of uploads per content release compared to the overall monthly uploads. As the popularity of the game rises, the avg yearly uploads trends upwards despite certain changes or expansions being less popular than previous ones. This is most visible on the Explorers set, the most popular set as far as uploads are concerned, yet the largest upload months were the months around the Old Gods and Gagdetzan expansion releases.


Another thing I wanted to visualize was the most popular class and deck for each content update. While this might be the most interesting to people who play the game, it can give a cool insight on how the meta adjusts when things are changed.

Taking a look at the most popular class per patch (based on total number of deck uploads) actually tells us a lot.

![Class pop per Patch][class_pop_per_patch]

[class_pop_per_patch]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/most_popular_class_per_patch.png

While this may not look interesting, the two patches where priest was the most uploaded deck could actually be a farce. While yes, the most user-made decks during that time were Priest decks, it's very likey the most played class was not priest. The Karazhan content release could theoretically have created a large skew in the deck uploads due to a certain card called Purify.

<p align="center">
  <img width="200" height="250" src="img/purify.png">
</p>


It was by miles the worst card that had been added to the game, which means everyone wanted to make a deck where it was good to try and prove... something? I strongly believe this card single handedly skewed the priest data. If we take a look at the highest rated deck per patch, it supports this data as well.

![best_deck_per_patch][deck_per_patch]

[deck_per_patch]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/most_popular_deck_per_patch.png

All of these decks but 1 were actually good decks. The outlier here is purify priest, which at the time boasted (if you were lucky) around a 10% winrate. The highest rated decks afterwards are actual good decks again, but I do believe that the desire to make what was deemed a "meme card" good in a competitive setting skewed the data.

## **Conclusion**
It's pretty plain to see that whenever new content is released, the deck uploads spike briefly and slowly decline until new content comes out again. What makes the data most interesting to me is how easily it can be skewed. Just a single bad card made a bad deck "good" purely because people were making fun of it. 

## **Photo and Data Credits**
- I did not create nor do I own any images/data from the game of Hearthstone
- This data was collected from https://www.hearthpwn.com using their API by a Kaggle user named romainvincent. The data can be accessed [by clicking here.](https://www.kaggle.com/romainvincent/history-of-hearthstone/metadata)
- Hearthstone, World of Warcraft, and all related properties are owned by Blizzard Entertainment
- The gameplay image was pulled from an article on https://www.windowscentral.com, the article can be found [here.](https://www.windowscentral.com/hearthstone-rise-mech-event-starts-june)
- The image of the Purify card was pulled from the [Hearthstone Wiki](https://hearthstone.gamepedia.com), the page about the card Purify [can be found here.](https://hearthstone.gamepedia.com/Purify)
- All graphs and charts were made by myself in matplotlob using the data from Kaggle