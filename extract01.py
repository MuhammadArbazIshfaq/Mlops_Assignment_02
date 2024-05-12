def extract():
    import requests
    from bs4 import BeautifulSoup

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
    sportsArticleData = []
    for article in articles:
        headline = article.h2.a.text.replace("\n", "")
        link = article.h2.a['href'].replace("\n", "")
        description = article.find("div", class_="story__excerpt").text.replace("\n", "")
        description = description.split('.')[0].replace("\n", "")

        try:
            source = article.find("span", class_="story__byline").a.text
        except AttributeError:
            source = "Unknown"

        article_data = {
            "headline": headline,
            "link": link,
            "description": description,
            "source": source,
            "type": "sports"
        }
        sportsArticleData.append(article_data)

    # Finding link towards the tech page
    techLink = soup.find("a", title="Tech")['href']
    techLink = url + techLink

    # Scraping the tech page
    response = requests.get(techLink)

    soupTech = BeautifulSoup(response.content, "html.parser")

    articles = soupTech.find_all("article")
    techArticleData = []
    for article in articles:
        headline = article.h2.a.text.replace("\n", "")
        link = article.h2.a['href'].replace("\n", "")
        description = article.find("div", class_="story__excerpt").text.replace("\n", "")
        
        try:
            source = article.find("span", class_="story__byline").a.text.replace("\n", "")
        except AttributeError:
            source = "Unknown"

        description = description.split('.')[0].replace("\n", "")
        article_data = {
            "headline": headline,
            "link": link,
            "description": description,
            "source": source,
            "type": "tech"
        }
        techArticleData.append(article_data)

    techArticleData.extend(sportsArticleData)

    # Debugging: Print the collected data
    print("Tech Articles:")
    print(techArticleData)
    print("\nSports Articles:")
    print(sportsArticleData)

    fieldnames = ['headline', 'link', 'description', 'source', 'type']
    import csv

    # Specify the file path
    csv_file = 'data.csv'

    # Write the data to a CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="|")

        # Write the header
        writer.writeheader()

        # Write the data
        for row in techArticleData:
            writer.writerow(row)

    print(f'Data has been successfully saved to {csv_file}')


# Call the function to execute
extract()
