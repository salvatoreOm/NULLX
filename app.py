import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)

# My price comparison functions


def get_meesho_price(product_name):
  url = f'https://www2.hm.com/search?keyword={product_name.replace(" ", "-")}'
  headers = {
      'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/109.0.0.0 Safari/537.36'),
  }

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  price = soup.find('span', {'class': 'pdp-price'})
  return price.text.strip() if price else 'N/A'


def get_snapdeal_price(product_name):
  url = f'https://www.snapdeal.com/search?keyword={product_name.replace(" ", "%20")}'
  headers = {
      'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/109.0.0.0 Safari/537.36'),
  }

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  price = soup.find('span', {'class': 'lfloat product-price'})
  return price.text.strip() if price else 'N/A'


def get_amazon_price(product_name):
  url = f'https://www.amazon.com/s?k={product_name.replace(" ", "+")}'
  headers = {
      'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/109.0.0.0 Safari/537.36'),
  }

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  price = soup.find('span', {'class': 'a-price-whole'})
  return price.text.strip() if price else 'N/A'


def get_flipkart_price(product_name):
  url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}'
  headers = {
      'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/109.0.0.0 Safari/537.36'),
  }

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  price = soup.find('div', {'class': '_30jeq3'})
  return price.text.strip() if price else 'N/A'


@app.route('/', methods=['GET', 'POST'])
def price_comparison():
  meesho_price = None
  snapdeal_price = None
  amazon_price = None
  flipkart_price = None

  if request.method == 'POST':
    product_name = request.form.get('product_name')
    meesho_price = get_meesho_price(product_name)
    snapdeal_price = get_snapdeal_price(product_name)
    amazon_price = get_amazon_price(product_name)
    flipkart_price = get_flipkart_price(product_name)

  return render_template('home.html',
                         meesho_price=meesho_price,
                         snapdeal_price=snapdeal_price,
                         amazon_price=amazon_price,
                         flipkart_price=flipkart_price)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
