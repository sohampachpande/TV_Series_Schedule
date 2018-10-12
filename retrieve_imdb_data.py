import requests
import bs4 as bs
import re
import datetime

base_url = 'https://www.imdb.com'

# This function returns search result page in beautifulsoup datatype for given tv series title query
def search_tv_series_soup(tv_series_title):
    search_link = base_url + '/search/title'
    params = {'title':tv_series_title,'title_type':'tv_series'}
    tvr = requests.request('GET', url = search_link, params = params)
    tvr_soup = bs.BeautifulSoup(tvr.text,'lxml')
    return tvr_soup


# This function returns link to the page of given tv series.
def find_tv_series_page_link(tv_series_title):
    if type(tv_series_title)!= str:
        print('Invalid argument data type passed to find_link function')    
    # get search results in html
    tvr_soup = search_tv_series_soup(tv_series_title)
    tv_temp = tv_series_title.lower().replace('+','')
    tv_temp = tv_temp.lower().replace(' ','')
    for a in tvr_soup.findAll('a', href= True):
        stemp = str(a.string)
        if tv_temp in stemp.lower().replace(' ',''):
            link = a['href']
            break
    return base_url+link[0:link.find('?')-1]

# This function returns episodes page in beautifulsoup datatype for given tv series title query for the given season
# the default for season = -1 gives last season
def get_episodes_page(tv_series_title, season=-1):
    link = find_tv_series_page_link(tv_series_title)
    params = {'season': season}
    eps_resp = requests.request('GET', link + '/episodes', params = params)
    eps_soup = bs.BeautifulSoup(eps_resp.text, 'lxml')
    return eps_soup
a = get_episodes_page('friends')

# This function gets episode date in datetime format from the html value passed to it
def get_ep_date(ep):
    ep_text = ep.text.replace(' ','')
    list_ep_date = ep_text.split()[0]
    try:
        ep_date = datetime.datetime.strptime(ep_text,'\n%d%b.%Y\n')
    except ValueError:
        try:
            ep_date = datetime.datetime.strptime(ep_text,'\n%d%b%Y\n')
        except ValueError:
            ep_date = datetime.datetime.strptime(ep_text,'\n%Y\n')
    return ep_date.date()


def get_final_schedule(tv_series_title):
    now_date = datetime.datetime.now().date()
    
    episode_list_page_soup = get_episodes_page(tv_series_title)

    list_ep = episode_list_page_soup.findAll('div',{'class':'airdate'})
    
    i = -1
    while len(list_ep[i].string)<=1:
        i -=1
    last_ep_date = get_ep_date(list_ep[i])
    
    first_ep_date = get_ep_date(list_ep[0])
    
    if last_ep_date<now_date:
        return ("The TV series has finished streaming its episodes in {} {}".format(last_ep_date.strftime('%B'), last_ep_date.year))
    
    elif first_ep_date>now_date:
        return ("Next season begins in {}".format(first_ep_date.year))
    
    else:
        for ep in list_ep:
            ep_date = get_ep_date(ep)
            if ep_date>=now_date:
                return("Next Episode would stream on {} {} {}".format(ep_date.day, ep_date.strftime('%B'), ep_date.year))  
    
        return ("The TV series has finished streaming its episodes in {} {}".format(ep_date.strftime('%B'), ep_date.year))


# print(get_final_schedule('game of thrones'))