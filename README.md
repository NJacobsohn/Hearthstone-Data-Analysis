# Hearthstone Data Analysis

## **Overview**
Hearthstone is a digital card game release by Blizzard Entertainment in 2014. It's a free to play game featuring many prominent characters from World of Warcraft. Hearthstone quickly became extremely popular due to having similar gameplay to Magic: The Gathering but also having a much lower barrier to entry. It also has many facets that make it unique due to its electronic only nature. Creating random cards from a class and shuffling them into your deck, cards that replace your deck with a different one mid-match, or even a card that shuffles a copy of your opponents deck into your deck.

The dataset was pulled from a popular deck sharing website called [hearthpwn](https://www.hearthpwn.com), and contains over 340,000 decks uploaded from the game's release until February of 2017. The dataset also contains a .json file with every card in the game and their attributes.

## **Cleaning**
It's immediately obvious that there's a lot of bad data in here. With the card json, it was easy to decide what to keep. Only cards that are collectible, and that can be put into a deck were kept into consideration. The decks were a bit of a challenge, but ultimately I separated the main dataset into a couple, smaller dataframes with pandas. I ended up with only the decks that were created for use in the ranked gamemode, about 200,000 entries. From there I organized the data by each deck's user rating, and removed all duplicate entries, bringing the total data sample size to 184,903 decks.
## **Visualization**
What really wanted to know about this data (as a former player) is how balance updates to certain cards or new releases affect what is played or popular. As a starting point, this is the total amount of deck uploads per content update.
![Uploads per Patch][patch_uploads]

[patch_uploads]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/deck_uploads_per_patch.png

While this might be interesting to look as for someone who's played the game before, I want to also show how each of these compared to uploads throughout the overall timeline of the game.

![Patch versus Month][patch_versus_month]

[patch_versus_month]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/month_versus_patch.png

This shows the total amount of uploads per content release compared to the overall monthly uploads. As the popularity of the game rises, the avg yearly uploads trends upwards despite certain changes or expansions being less popular than previous ones. This is most visible on the Explorers set, the most popular set as far as uploads are concerned, yet the largest upload months were the months around the Old Gods and Gagdetzan expansion releases.


Another thing I wanted to visualize was the most popular class and deck for each content update. While this might be the most interesting to people who play the game, it can give a cool insight on how the meta adjusts when things are changed.

Taking a look at the most popular class per patch (based on total number of deck uploads) actually tells us a lot.

![Class pop per Patch][class_pop_per_patch]

[class_pop_per_patch]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/most_popular_class_per_patch.png

While this may not look interesting, the three patches where priest was the most uploaded deck could actually be a farce. While yes, the most user-made decks during that time were Priest decks, it's very likey the most played class was not priest. The Karazhan content release could theoretically have created a large skew in the deck uploads due to a certain card called Purify.

![Purify][purify]

[purify]
## **Conclusion**