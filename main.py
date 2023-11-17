import requests
from bs4 import BeautifulSoup
import os

def get_amazon_price(url):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", 
        "Accept-Encoding": "gzip, deflate, br", 
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Dest": "document", 
        "Sec-Fetch-Mode": "navigate", 
        "Sec-Fetch-Site": "cross-site", 
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15", 
    }
    
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # print(soup)
        price = soup.find(class_='a-price-whole')
        cents = soup.find(class_="a-price-fraction")
        if price:
            return price.get_text().strip() + cents.get_text().strip()
        else:
            return "Price not found"
    else:
        return "Failed to retrieve page"
    
def lambda_handler(event, context):
    url = os.environ.get('AMZN_URL')
    price = get_amazon_price(url)
    return {
        'statusCode': 200,
        'body': json.dumps({'price': price})
    }


if __name__ == '__main__':
    lambda_handler()
