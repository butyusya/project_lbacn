# Miraculous: Tales of recommendations and statistics

The result of this project is a website dedicated to Miraculous, where a user can get recommendations for viewing or look at different types of statistics. It can be seen here: https://miraculousrecsandstats.pythonanywhere.com/

## How to use the website

There are three sections on the site.

### Get an episode

It is the main page. To get a recommendation two fields need to be filled (a user can choose from two lists of options using search): a similar episode and a participating character. Both of them are optional and can be left blank. Here is how the recommendation depends on the filling of this two fields:

1. If **both of them are empty** recommendation is a random episode.

2. If only a **character** is present recommendation is a random episode with that character.

3. If only an **episode** is present recommendation is the one most similar to it. It is always the same recommendation for the same source episode. (Every other episode is ranked based on its similarity to this one, so recommendation is the top 1 everytime.)

4. If **both are present** recommendation is a combo: most similar to the source episode with the desired character. And again recommendation is always the same for the same fillings.

NB: if some character is only present in one episode, and both this character and this episode is filled in, recommendation will be this exact episode.

The recommendation is presented in the form: picture, title, synopsis. Click on 'MORE INFO' will lead to the fan wiki page about this episode.

### Statistics

There are four types of statistics: **for a character**, **for an episode**, **for a season**, and **overall**. This four options is dropped down after a click on the 'Statistics'

1. For the first three categories (character, episode, season) a field will be present to fill. Exact option can be chosen. If the field is empty statistics for a random option will be presented.

2. Overall statistics is presented just after clicking on the respective category.

NB: on fan wiki some characters can be written differently on different pages (for example, Jagged or Jagged Stone or Stone), so they considered to be different characters in every place on this website.

### Help

This section explains how website works.

## Project structure

* *crawler.ipynb* – collecting information from [fan wiki](https://miraculousladybug.fandom.com/wiki/Miraculous_Ladybug_Wiki) and saving it to **lbacn.db** (first edition) in the table *episodes* (ep_id, season, ep_href, ep_title, synopsis, plot, script). Also saving **images** for every episode in the directory */static*.

* *clean_db.ipynb* – saving the second edition of **lbacn.db**. It adds two tables. The first one is *characters_lines* (ep_id, character, num_of_replics) with information about number of lines by character per episode. After cleaning and lemmatizing all texts for each episode, vectorizing them, and ranking by cosine similarity it creates table similarity (ep_id, top_1_id, ...). It also saves all **characters** and **episodes** in respective txt files (each character and episode on a new line).

* *get_ep.py* – defines four functions that return recommendation based on source date (one for each combination of presence or absence of a character and an episode).

* *stats.py* – defines four functions that return statistics for each of the four categories (episode, character, season, and overall).

* *overall_stats.py* – uses function for overall statistics, saves returned information to **overall_stats.txt** (in binary form) and saves returned diagrams to directiry */static*.

* *main.py* – main file. It uses images from */static* and html files from */templates* to return the target website. It also uses functions from *get_ep.py* and *stats.py* to get information from *lbacn.db* for each input.

## Used packages

* *requests, fake_useragent* – to get information from fan wiki pages

* *bs4* – to present that information in a convenient way

* *sqlite3* – to work with the database

* *re, spacy, nltk* – to clean and lemmatize texts for each episode

* *sklearn* – to vectorize all cleaned texts and find cosine similarity 

* *flask* – to return the website

* *matplotlib, seaborn* – for visualization

* *pickle* – to save answer (list) to overall_stats.txt and later read it

* *random* – to get random episodes for recommendations

### Some sources of the code

[w3schools](https://www.w3schools.com/bootstrap5/index.php) – for information on website making

[stackoverflow](https://stackoverflow.com/a/57809086) – for choice from the list of options with search on website
