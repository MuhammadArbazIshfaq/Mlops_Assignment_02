import re
import string
import csv
import requests
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def preprocess_text(text):
    # Convert text to lowercase
    text = text.lower()
    
    # Remove numbers
    text = re.sub(r'\d+', '', text)
    
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    
    # Remove extra white spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Tokenize text
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    # Join tokens back into string
    preprocessed_text = ' '.join(tokens)
    
    return preprocessed_text

def extract_and_preprocess_data():
    # URL of the Dawn news website
    url = "https://www.dawn.com"

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Finding link towards the sports page
    sportsLink = soup.find("a", title="Sport")['href']
    sportsLink = url + sportsLink

    # Scraping the sports page
    response = requests.get(sportsLink)

    soupSports = BeautifulSoup(response.content, "html.parser")

    articles = soupSports.find_all("article")
    articles_data = []
    for article in articles:
        headline = article.h2.a.text.replace("\n", "")
        link = article.h2.a['href'].replace("\n", "")
        description = article.find("div", class_="story__excerpt").text.replace("\n", "")
        
        # Preprocess description text
        preprocessed_description = preprocess_text(description)

        try:
            source = article.find("span", class_="story__byline").a.text
        except AttributeError:
            source = "Unknown"

        article_data = {
            "headline": headline,
            "link": link,
            "description": preprocessed_description,
            "source": source,
            "type": "sports"
        }
        articles_data.append(article_data)

    # Finding link towards the tech page
    techLink = soup.find("a", title="Tech")['href']
    techLink = url + techLink

    # Scraping the tech page
    response = requests.get(techLink)

    soupTech = BeautifulSoup(response.content, "html.parser")

    articles = soupTech.find_all("article")
    for article in articles:
        headline = article.h2.a.text.replace("\n", "")
        link = article.h2.a['href'].replace("\n", "")
        description = article.find("div", class_="story__excerpt").text.replace("\n", "")
        
        # Preprocess description text
        preprocessed_description = preprocess_text(description)

        try:
            source = article.find("span", class_="story__byline").a.text
        except AttributeError:
            source = "Unknown"

        article_data = {
            "headline": headline,
            "link": link,
            "description": preprocessed_description,
            "source": source,
            "type": "tech"
        }
        articles_data.append(article_data)

    return articles_data

def save_to_csv(data):
    fieldnames = ['headline', 'link', 'description', 'source', 'type']
    csv_file = 'data.csv'

    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="|")
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f'Data has been successfully saved to {csv_file}')

if __name__ == "__main__":
    articles_data = extract_and_preprocess_data()
    save_to_csv(articles_data)
