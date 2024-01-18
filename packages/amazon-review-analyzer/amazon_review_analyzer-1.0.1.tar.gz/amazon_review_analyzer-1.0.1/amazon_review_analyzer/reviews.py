
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
import demoji  
import csv
import re
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError


def extract_asin(url):
    pattern = r'/dp/([A-Za-z0-9]{10})'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None

def get_reviews(asin):
    review_list = []
    base_url = f"https://www.amazon.in/product-reviews/{asin}"
    page = 1

    while True:
        url = f"{base_url}/ref=cm_cr_getr_d_paging_btm_next_{page}?pageNumber={page}"
        print(url)

        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
        req = Request(url, headers=headers)

        try:
            html = urlopen(req)
        except HTTPError as e:
            if e.code == 404:
                print(f"Page {page} not found. Exiting.")
                break
            else:
                print(f"Error accessing page {page}: {e}")
                continue

        soup = BeautifulSoup(html, 'html.parser')
        review_elements = soup.find_all('span', class_='a-size-base review-text review-text-content')
        review_element_1 = soup.find_all('div', class_="a-row a-spacing-small review-data")

        for review_element in zip(review_elements, review_element_1):
            # print(review_element[0].text.strip() + review_element[1].text.strip())
            review_list.append(review_element[0].text.strip() + review_element[1].text.strip())

        next_button = soup.find('li', class_='a-last')
        if not next_button:
            print(f"No more pages. Exiting.")
            break

        page += 1
        time.sleep(10) 
    return review_list

def get_sentiment():
    amazon_url = input("Enter the Amazon URL: ")
    asin = extract_asin(amazon_url)
    reviews = get_reviews(asin)

    csv_file_path = 'reviews.csv'
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Reviews'])
        for review_text in reviews:
            csv_writer.writerow([review_text])
    print(f"Reviews have been saved to {csv_file_path}.")

    data = pd.read_csv('reviews.csv')
    query = data['Reviews']

    # Ensure that the values are strings before applying demoji.replace
    query = query.apply(lambda x: demoji.replace(str(x), ''))

    analyser = SentimentIntensityAnalyzer()
    sentiment = analyser.polarity_scores(query)


    # Positive, Negative, Neutral results
    if sentiment['compound'] >= 0.05:
        print("Positive. Definitely recommended buy this product")
    elif sentiment['compound'] <= -0.05:
        print("Negative. Don't buy this product")
    elif -0.05 < sentiment['compound'] < 0.05:
        print("Neutral. Depends on your choice to buy or not")
