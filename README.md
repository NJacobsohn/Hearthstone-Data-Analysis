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

While this might be interesting to look as for someone who's played the game before, I want to also show how each of these events affected uploads throughout the overall timeline of the game.
## **Conclusion**