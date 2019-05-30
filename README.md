# Purifying Hearthstone Data

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

[hs_board]:https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/hearthstone-gameplay.jpg

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

Starting with the most popular class per patch:

![Class pop per Patch][class_pop_per_patch]

[class_pop_per_patch]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/most_popular_class_per_patch.png

And on to the highest rated decks.

![best_deck_per_patch][deck_per_patch]

[deck_per_patch]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/most_popular_deck_per_patch.png

It's pretty hard to tell at a glance how these line up, so lets mark them based off of if the deck matches the popular class rather than just by class.


![deck_and_class_match][matching]

[matching]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/deck_matching_class_pop.png

So there really doesn't seem to be any sort of tie-in between what decks were highly rated versus what classes people like playing. But there it something interesting about the highest rated decks. Every deck on it is a deck with a high winrate, except for one. This beautiful little outlier is Purify Priest. Purify Priest (at the time) boasted, if you were lucky, around a 10% winrate.

## **What's a Purify???**

<p align="center">
  <img width="225" height="300" src="img/purify.png">
</p>

While this may not seem either bad or good, this card was by miles the worst card that had been added to the game. It was so bad it became a challenge to try and make a deck that could actually win centered around purify's effect. Fortunately (maybe), that challenge took off and consquently created a whole cult of Hearthstone fans who called the Purify Priest the "Unicorn Deck". Something that's so mystical and powerful that it couldn't possibly exist. The high rated version of it that is seen on the above graph is a remnant of this belief that it truly was the strongest deck, just no one knew how to use it.

## **Return to Visualization**

The highest rated decks after Purify Priest are actual good decks again, but the following behind this unicorn deck caused an interesting blip on an otherwise pristine chart.
Funnily enough, Purify only appears in 7% of Priest decks from its release until the next expansion came out 3 months later. Leading down an interesting idea of determining the most popular cards for each class in ranked decks. Let's look at the Priest cards first.

![top_50_priest_cards_by_representation][top_50_priest]

[top_50_priest]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/priest_card_percentages.png

If you're angry that our lord and savior Purify isn't on this chart, please click [here](https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/purify_purify_purify_purify.png) for a version of it that says Purify for every card. If you're not, let's proceed. Something of note on this plot is the fact that some of the top 50 Priest cards are actually Neutral cards. I felt these were important to keep in as even though they may be Neutral, these are the specific Neutral cards most used in Priest decks. Each class has different Neutral cards that happen to synergize with their cards. We can get a good idea of which Neutral cards are shared amongst the most classes by looking at the top 50 cards overall.

![top_50_all][top_50]

[top_50]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/wild_card_representation.png

That top 15 right there is what I'm talking about. Those are the Neutral cards consistently find their way into 2, 3, or even 5 different classes. Let's peek at the top 15 cards for each class.

![top_15_all_classes][top_15_all]

[top_15_all]: https://github.com/NJacobsohn/Hearthstone-Data-Analysis/blob/master/img/class_card_representation.png

Azure Drake shows up in 5 different classes, and in 40%-50% of decks for those classes. Sylvanas Windrunner, the overall 2nd place shows up in 3. These cards were later 

## **Conclusion**
It's pretty plain to see that whenever new content is released, the deck uploads spike briefly and slowly decline until new content comes out again. What makes the data most interesting to me is how easily it can be skewed. Just a single bad card made a bad deck "good" purely because people were making fun of it. Or a single good card makes marginal popularity improvements become massive improvements. Hearthstone's popularity continues to rise even if the monthly submissions slow briefly. 

## **Photo and Data Credits**
- I did not create nor do I own any images/data from the game of Hearthstone
- This data was collected from https://www.hearthpwn.com using their API by a Kaggle user named romainvincent. The data can be accessed [by clicking here.](https://www.kaggle.com/romainvincent/history-of-hearthstone/metadata)
- Hearthstone, World of Warcraft, and all related properties are owned by Blizzard Entertainment
- The gameplay image was pulled from an article on https://www.windowscentral.com, the article can be found [here.](https://www.windowscentral.com/hearthstone-rise-mech-event-starts-june)
- The image of the Purify card was pulled from the [Hearthstone Wiki](https://hearthstone.gamepedia.com), the page about the card Purify [can be found here.](https://hearthstone.gamepedia.com/Purify)
- All graphs and charts were made by myself in matplotlob using the data from Kaggle