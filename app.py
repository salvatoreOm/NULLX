import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)


# Defining your price comparison functions
def get_flipkart_data(product_name):
  url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "+")}'
  headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  results = []

  for item in soup.find_all('div', class_='_4rR01T'):
    product = item.get_text(strip=True)
    price_item = item.find_next('div', class_=['_30jeq3 _1_WHN1'])
    if price_item:
      price = price_item.get_text(strip=True)
    else:
      price = 'N/A'
    results.append({'product': product, 'price': price})

  return results if results else [{'product': 'N/A', 'price': 'N/A'}]


def get_amazon_data(product_name):
  url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
  headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  results = []

  for item in soup.find_all('div', class_='s-result-item'):
    product = item.find('span', class_='a-text-normal')
    price_item = item.find('span', class_='a-price-whole')
    if product and price_item:
      product_name = product.get_text(strip=True)
      price = price_item.get_text(strip=True)
      results.append({'product': product_name, 'price': price})

  return results if results else [{'product': 'N/A', 'price': 'N/A'}]


def get_snapdeal_data(product_name):
  url = f'https://www.snapdeal.com/search?keyword={product_name.replace(" ", "%20")}'
  headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  results = []

  for item in soup.find_all('div', class_='product-tuple-description'):
    product = item.find('p', class_='product-title')
    price_item = item.find('span', class_='lfloat product-price')
    if product and price_item:
      product_name = product.get_text(strip=True)
      price = price_item.get_text(strip=True)
      results.append({'product': product_name, 'price': price})

  return results if results else [{'product': 'N/A', 'price': 'N/A'}]


def get_reliance_digital_data(product_name):
  url = f'https://www.reliancedigital.in/search?q={product_name.replace(" ", "+")}'
  headers = {
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  results = []

  for item in soup.find_all('div', class_='product-details'):
    product = item.find('a', class_='product-title')
    price_item = item.find('span', class_='priceboxw__price')
    if product and price_item:
      product_name = product.get_text(strip=True)
      price = price_item.get_text(strip=True)
      results.append({'product': product_name, 'price': price})

  return results if results else [{'product': 'N/A', 'price': 'N/A'}]


@app.route('/', methods=['GET', 'POST'])
def price_comparison():
  product_results = []

  if request.method == 'POST':
    product_names = request.form.getlist('product_name')

    for product_name in product_names:
      flipkart_data = get_flipkart_data(product_name)
      amazon_data = get_amazon_data(product_name)
      snapdeal_data = get_snapdeal_data(product_name)
      reliance_digital_data = get_reliance_digital_data(product_name)

      product_results.append({
          'product_name': product_name,
          'data': {
              'Flipkart': flipkart_data,
              'Amazon': amazon_data,
              'Snapdeal': snapdeal_data,
              'RelianceDigital': reliance_digital_data,
          }
      })

  return render_template('home.html', product_results=product_results)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
