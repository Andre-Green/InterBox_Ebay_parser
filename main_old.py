import requests
import json

class eBayProductInfo:
    def __init__(self, app_id):
        self.base_url = "https://api.ebay.com/buy/browse/v1/item_summary/search"
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {app_id}',
        }

    def get_product_info(self, keywords):
        params = {
            'q': keywords,
        }
        response = requests.get(self.base_url, headers=self.headers, params=params)

        if response.status_code == 200:
            data = response.json()
            if data.get('itemSummaries'):
                products = data['itemSummaries']
                results = []
                for product in products:
                    product_info = {
                        'image_url': product.get('image', {}).get('imageUrl'),
                        'price': product.get('price', {}).get('value'),
                        'currency': product.get('price', {}).get('currency'),
                        'description': product.get('title'),
                        'seller': product.get('seller', {}).get('username'),
                        'product_url': product.get('itemWebUrl'),
                        'delivery_price': product.get('shippingOptions', [{}])[0].get('shippingCost', {}).get('value')
                    }
                    results.append(product_info)
                return results
            else:
                return {"error": "No products found"}
        else:
            return {"error": "Failed to retrieve data", "status_code": response.status_code}

    def save_product_info(self, keywords, filename):
        product_info = self.get_product_info(keywords)
        with open(filename, 'w') as json_file:
            json.dump(product_info, json_file, indent=4)


if __name__ == "__main__":
    app_id = 'AndreMas-TestInte-SBX-d93e580d4-b5bb08b9'  # Replace with your eBay API app ID
    ebay_product = eBayProductInfo(app_id)

    keywords = input("Enter the keywords to search: ")
    filename = input("Enter the filename to save the product info: ")

    ebay_product.save_product_info(keywords, filename)
    print(f"Product information saved to {filename}")
