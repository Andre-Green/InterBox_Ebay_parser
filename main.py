import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent

class EbayProductScraper:
    def __init__(self, user_agent=None):
        self.user_agent = user_agent or UserAgent()
        self.headers = {
            'accept': 'application/json, text/plain, */*',
            'user-Agent': self.user_agent.chrome,
        }

    def scrape_product(self, url):
        try:
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

        item_id = url.split('/')[4].split('?')[0]
        soup = BeautifulSoup(r.text, 'lxml')
        items_description = soup.findAll('div', class_='main-container')

        description_list = []

        for item in items_description:
            name = item.find('h1', class_='x-item-title__mainTitle').find('span').text if item.find('h1', class_='x-item-title__mainTitle') else 'N/A'
            seller_info = item.find('div', class_='x-sellercard-atf__info__about-seller')
            seller = seller_info.find('span', class_='ux-textspans ux-textspans--BOLD').text if seller_info else 'N/A'
            reviews = seller_info.find('span', class_='ux-textspans ux-textspans--SECONDARY').text if seller_info else 'N/A'
            reviews_qty = item.find('ul', class_='x-sellercard-atf__data-item-wrapper').find('span', class_='ux-textspans ux-textspans--PSEUDOLINK').text if item.find('ul', class_='x-sellercard-atf__data-item-wrapper') else 'N/A'
            price_info = item.find('div', class_='vim x-bin-price')
            price = price_info.find('span').text if price_info else 'N/A'
            image_link = item.find('div', class_='ux-image-carousel-container image-container').find('img').get('src')
            shipping_info = item.find('div', class_='ux-labels-values__values-content')
            shipping_price = shipping_info.find('span', class_='ux-textspans ux-textspans--BOLD').text if shipping_info and shipping_info.find('span', class_='ux-textspans ux-textspans--BOLD') else 'N/A'
            try:
                item.find('div', class_='x-item-title__badgehighlight')
                authenticity = ' + '
            except:
                authenticity = ' - '
            product_url = f'https://www.ebay.com/itm/{item_id}'

            description_list.append({
                'name': name,
                'seller': seller,
                'reviews': reviews,
                'reviews_qty': reviews_qty,
                'price': price,
                'image_link': image_link,
                'shipping_price': shipping_price,
                'authenticity': authenticity,
                'product_url': product_url,

            })

        return description_list

if __name__ == "__main__":
    url = input('Input URL of product: ')
    scraper = EbayProductScraper()
    result = scraper.scrape_product(url)

    # Print the JSON output
    print(json.dumps(result, indent=4))

    # Optionally, save to a JSON file
    # with open('product_info.json', 'w') as json_file:
    #     json.dump(result, json_file, indent=4)
