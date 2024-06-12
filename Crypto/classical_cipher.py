import requests
from bs4 import BeautifulSoup

from ..Utils import info

def substitution_solver(cipher: str):
    guballa_url = 'https://www.guballa.de/substitution-solver'

    info('Substitution Solver : Requesting form data')
    response = requests.get(guballa_url)
    response.raise_for_status()

    post_data = {
        'data[language]': 'en', 
        'data[ciphertext]': cipher
    }
    soup = BeautifulSoup(response.text, 'html.parser')
    for input in soup.find_all('input'):
        post_data[input.get('name')] = input.get('value')

    info('Substitution Solver : Decrypting cipher')
    response = requests.post(guballa_url, data = post_data)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    return str(soup.find('textarea', attrs = { 'name': 'cleartext' }).string).removesuffix('\n')

