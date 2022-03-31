# %%
# imports:
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import requests

# step 1 lets scrape the guided project website with all the posts:
url = "https://community.dataquest.io/c/share/guided-project/55"
html = urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

# look for every 'a' tag with 'class' title raw-link raw-topic-link:
list_all = soup.find_all("a", class_="title raw-link raw-topic-link")

# check how many elements we've extracted:
len(list_all)

# %%
import codecs
import pandas as pd
# this is the file of the website, after scrolling all the way down:
file = codecs.open("dataquestProjects.html", "r", "utf-8")
# parse the file:
parser = BeautifulSoup(file, 'html.parser')

# look for every 'tr' tag, scrape its contents and create a pandas series from the list:
list_all = parser.find_all('tr')
series_4_df = pd.Series(list_all)

# create a dataframe from pandas series:
df = pd.DataFrame(series_4_df, columns=['content'])
df['content'] = df['content'].astype(str)
df.head()

# %%
print(df['content'][32])
N = 32
df = df.iloc[N: , :]

# %%
# remove 1st row:
df = df.iloc[1:,:]
# extract title, link and number of replies:
df['title'] = df['content'].str.extract('<span dir="ltr">(.*?)</span>')
df['link'] = df['content'].str.extract('href=\"(.*?)\" role')
df['replies'] = df['content'].str.extract("This topic has (.*) re").astype(int)
df['views'] = df['content'].str.extract("this topic has been viewed (.*?) times")
df['views'] = df['views'].str.replace(',','').astype(int)

# remove 1 generic post and posts with 0 replies:
df = df[df['replies']>0]
df = df[df['replies']<100]
df.head()


# %%
df['link'][36]

# %%
# create a function for scraping the actual posts website:
def get_reply(one_link):
    response = requests.get(one_link)
    content = response.content
    parser = BeautifulSoup(content, 'html.parser')
    tag_numbers = parser.find_all("div", class_="post")
    # we're only going to scrape the content of the first reply (that's usually the feedback)
    feedback = tag_numbers[1].text
    return feedback

# %%
df.head(5)

# %%
# create a test dataframe to test scraping on 5 rows:
df_test = df[:5]

# %%
df_test.head(3)

# %%


# we'll use a loop on all the elements of pd.Series (faster than using 'apply')
feedback_list = []
for el in df_test['link']:
    feedback_list.append(get_reply(el))
    # print(feedback_list)
df_test['feedback'] = feedback_list
df_test

# %%
def scrape_replies(df):
    feedback_list = []
    for el in df['link']:
        feedback_list.append(get_reply(el))
    df['feedback'] = feedback_list
    return df

df = scrape_replies(df)

# %%
df.head(4)

# %%
df.to_csv('dataquest.csv')


