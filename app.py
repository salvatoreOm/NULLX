import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)


# My price comparison functions
def get_walmart_price(product_name):
  url = f'https://www.walmart.com/search?q={product_name.replace(" ", "+")}'
  headers = {
      # Replace with your User-Agent string
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  soup1 = BeautifulSoup(soup.prettify(), 'html.parser')
  price = soup1.find('div', class_='mr1 mr2-xl b black lh-copy f5 f4-l')
  return price.text.strip() if price else 'N/A'


def get_flipkart_price(product_name):
  url = f'https://www.flipkart.com/search?q={product_name.replace(" ", "%20")}'
  headers = {
      # Replace with your User-Agent string
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  soup1 = BeautifulSoup(soup.prettify(), 'html.parser')
  price = soup1.find('div', class_='_30jeq3 _1_WHN1')
  return price.text.strip() if price else 'N/A'


def get_amazon_price(product_name):
  url = f'https://www.amazon.in/s?k={product_name.replace(" ", "+")}'
  headers = {
      # Replace with your User-Agent string
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, 'html.parser')
  soup1 = BeautifulSoup(soup.prettify(), 'html.parser')
  price = soup1.find('span', class_='a-price')
  return price.text.strip() if price else 'N/A'


def get_snapdeal_price(product_name):
  url = f'https://www.snapdeal.com/search?keyword={product_name.replace(" ", "%20")}'
  headers = {
      # Replace with your User-Agent string
      'User-Agent':
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  price = soup.find('span', {'class': 'lfloat product-price'})
  return price.text.strip() if price else 'N/A'


@app.route('/', methods=['GET', 'POST'])
def price_comparison():
  walmart_price = None
  snapdeal_price = None
  amazon_price = None
  flipkart_price = None

  if request.method == 'POST':
    product_name = request.form.get('product_name')
    walmart_price = get_walmart_price(product_name)
    snapdeal_price = get_snapdeal_price(product_name)
    amazon_price = get_amazon_price(product_name)
    flipkart_price = get_flipkart_price(product_name)

  return render_template('home.html',
                         walmart_price=walmart_price,
                         snapdeal_price=snapdeal_price,
                         amazon_price=amazon_price,
                         flipkart_price=flipkart_price)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
