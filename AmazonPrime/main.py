from selenium import webdriver 
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

#CSS Variables 
titleClass = "h1"
titleName = "_2IIDsE _3I-nQy"
ratingClass = "span"
ratingName = "XqYSS8 FDDgZI"
synopsisClass = "div"
synopsisName = "_3qsVvm _1wxob_"

storeFrontURL = "https://www.amazon.com/gp/video/storefront/"
vidDownloadUrL = "/gp/video/detail"

videoLinks = []
titles = []
rating = [] 
synopsis = []

def scrapeText(lst,classType,className):
    findClass = soup.find_all(classType,class_=className)
    if len(findClass)==0 :
        lst.append(None)
    else:
        for n in findClass:
            if className == ratingName:
                   lst.append(float(n.text[-3:]))
            else:
                lst.append(n.text)

#Initial browser to be controlled by Python

driver = webdriver.Chrome(executable_path="/Users/vandanathannir/Downloads/chromedriver")
driver.get(storeFrontURL)

elems = driver.find_elements_by_xpath("//a[@href]")
for elem in elems:
    if vidDownloadUrL in elem.get_attribute("href"):
        videoLinks.append(elem.get_attribute("href"))
        
videoLinks = list(dict.fromkeys(videoLinks))

for i in range (0,10):
    driver.get(videoLinks[i])
    content =driver.page_source
    soup = BeautifulSoup(content)

    scrapeText(titles,titleClass,titleName)
    scrapeText(rating,ratingClass,ratingName)
    scrapeText(synopsis,synopsisClass,synopsisName)

data = {'Title': titles, 'Rating': rating, 'Synopsis': synopsis}
df = pd.DataFrame(data)
df.to_csv('PrimeVid.csv', index = False, encoding ='utf-8')

def wordcloud(df,filename):
    if len(df) > 1:
        text = ' '.join(df.Synopsis)
        wordcloud = WordCloud().generate(text)

        plt.imshow(wordcloud, interpolation= 'bilinear')
        plt.axis("off")

        plt.savefig(filename+".png")

df1 = df.loc[(df['Rating'] <6)]
df2 = df.loc[(df['Rating'] >=6) & (df['Rating'] < 8)]
df3 = df.loc[(df['Rating'] >=8)]

wordcloud(df1, "below 6")
wordcloud(df2, "6to7")
wordcloud(df3, "above8")

