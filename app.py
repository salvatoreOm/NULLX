import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, request

app = Flask(__name__)


# Your price comparison functions
def get_ajio_price(product_name):
  url = f'https://www.ajio.com/{product_name.replace(" ", "-")}'
  headers = {
      # Replace with your User-Agent string
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
      # Replace with your User-Agent string
      'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/109.0.0.0 Safari/537.36'),
  }
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  price = soup.find('span', {'class': 'lfloat product-price'})
  return price.text.strip() if price else 'N/A'


@app.route('/', methods=['GET', 'POST'])
def price_comparison():
  ajio_price = None
  snapdeal_price = None

  if request.method == 'POST':
    product_name = request.form.get('product_name')
    ajio_price = get_ajio_price(product_name)
    snapdeal_price = get_snapdeal_price(product_name)

  return render_template('home.html',
                         ajio_price=ajio_price,
                         snapdeal_price=snapdeal_price)


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
