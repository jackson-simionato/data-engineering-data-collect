# %%
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

cookies = {
'_gid': 'GA1.2.171527606.1737985240',
'_ga_DJLCSW50SC': 'GS1.1.1737985238.1.1.1737985290.8.0.0',
'_ga_D6NF5QC4QT': 'GS1.1.1737985239.1.1.1737985290.9.0.0',
'_ga': 'GA1.2.382328942.1737985239',
'FCNEC': '%5B%5B%22AKsRol_LQhaty1HV2n9lqs8bp2bcNYqwNySicBApEgSbX25vEta0HcgVhVROjMVrDWtadSRprhElIOOq0G_zUtZtkr4xyH6B0iEcZSmS5Z-QRT89goPK-pUGz_CL_h5fAuq37zdPn5-SLFDFSXt5JnGtXn4gJzaioA%3D%3D%22%5D%5D',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'cache-control': 'max-age=0',
    # 'cookie': '_gid=GA1.2.171527606.1737985240; _ga_DJLCSW50SC=GS1.1.1737985238.1.1.1737985290.8.0.0; _ga_D6NF5QC4QT=GS1.1.1737985239.1.1.1737985290.9.0.0; _ga=GA1.2.382328942.1737985239; FCNEC=%5B%5B%22AKsRol_LQhaty1HV2n9lqs8bp2bcNYqwNySicBApEgSbX25vEta0HcgVhVROjMVrDWtadSRprhElIOOq0G_zUtZtkr4xyH6B0iEcZSmS5Z-QRT89goPK-pUGz_CL_h5fAuq37zdPn5-SLFDFSXt5JnGtXn4gJzaioA%3D%3D%22%5D%5D',
    'priority': 'u=0, i',
    'referer': 'https://www.residentevildatabase.com/personagens/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
}

def get_content(url, headers=headers, cookies=cookies):
    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code != 200:
        print('Erro ao acessar a página')
    
    return response
    
def get_basic_data(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    td_page_content = soup.find('div', class_='td-page-content')
    paragrafo = td_page_content.find_all('p')[1]
    data = {}

    if len(paragrafo.find_all('em')) > 1:
        for em in paragrafo.find_all('em'):
            key, value = em.text.split(':')
            key = key.strip()
            value = value.split('.')[0].strip()
            data[key] = value
    elif len(paragrafo.find_all('em')) == 1:
        em = paragrafo.find('em')
        lines = em.text.split('\n')
        for line in lines:
            key, value = line.split(':')
            key = key.strip()
            value = value.split('.')[0].strip()
            data[key] = value
    return data

def get_appearences_data(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    td_page_content = soup.find('div', class_='td-page-content')
    appearences = [li.text for li in 
                 td_page_content.
                 find('h4').
                 find_next().
                 find_all('li')]

    return appearences

def get_character_data(url):
    response = get_content(url)

    if response.status_code != 200:
        return None
    
    character_data = get_basic_data(response)
    character_data['Aparicoes'] = get_appearences_data(response)

    return character_data

def get_character_links(url='https://www.residentevildatabase.com/personagens/'):
    soup = BeautifulSoup(get_content(url).text, 'html.parser')
    page_content = soup.find('div', class_='td-page-content')
    h3s = page_content.find_all('h3')

    characters = []

    for h3 in h3s:
        letter_characters = [anchor['href'] for anchor in 
                            h3.
                            find_next('p').
                            find_all('a')]
        
        characters.extend(letter_characters)

    return characters

# %%
## Lista de personagens
characters = get_character_links()

print(len(characters))
print(characters)
# %%
data_list = []
for url in tqdm(characters[50:]):
    print(url)
    character_data = get_character_data(url)

    if character_data:
        character_data['url'] = url
        data_list.append(character_data)

print(len(data_list))