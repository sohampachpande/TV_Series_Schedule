import requests
import bs4 as bs
import pickle
import string


# Code snippets in functions for edit distance- edits1(word) and edits2(word) from blog on spell correction by Peter Norvig
# link: http://norvig.com/spell-correct.html
letters    = 'abcdefghijklmnopqrstuvwxyz'

# this function finds all words which are atmost 1 dissimilarity/edit operation away given word
# edit operations are deletion, substitution, insertion and transposition
def edits1(word):
    # splits gives substrings to left and right of all characters in word
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)> 1]
    substitute   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + substitute + inserts)


# this function finds all words which are atmost 2 dissimilarities/edit operation away given word
def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# get names of all tv series from wikiquote and store them on disk using pickle
def get_titles():
    base_url = 'https://en.wikiquote.org/wiki/List_of_television_shows'
    suffix = ['_(A–H)', '_(I–P)', '_(Q–Z)']
    list_titles = []    
    for s in suffix:
        link = base_url + s
        wiki_page = requests.request('GET',link)
        wiki_soup = bs.BeautifulSoup(wiki_page.text,'lxml')
        for t in wiki_soup.findAll('a', href= True):
                tt = str(t.string)
                tt = tt.lower()

                # # remove all punctuation marks
                # punctuation_char = string.punctuation + '“”'
                # tt = tt.translate(str.maketrans('','',punctuation_char))

                list_titles.append(tt)
                # print(tt, '\n')
    with open('tv_series_titles', 'wb') as fp:
        pickle.dump(list_titles, fp)


# Reload the list of tv series titles from pickle file if it exists.
# If the file does not exist, create it by calling the function get_titles
try:
    with open('tv_series_titles', 'rb') as fp:
        list_titles = pickle.load(fp)
except FileNotFoundError:
    get_titles()
    with open('tv_series_titles', 'rb') as fp:
        list_titles = pickle.load(fp)


# This functions finds the tv series with correct spelling
# The scope of tv series spellings is restricted to max 2 edit distances
def correct_tv_title(word):
    # If the spellings with edit distance < 2 are present in tv series titles from wiki then we have correct spelling
    for w in edits2(word):
        if w in list_titles:
            return w
    return word

# print('game of throns' in list_titles)
# print(correct_tv_title('game of throns'))