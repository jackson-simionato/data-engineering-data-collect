import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from tenacity import retry, stop_after_attempt, wait_exponential
from requests.exceptions import RequestException, Timeout, ConnectionError

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

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    reraise=True
)
def get_content(url, headers=headers, cookies=cookies):
    """
    Fetch content from given URL using provided headers and cookies.
    
    Args:
        url (str): Target URL to scrape
        headers (dict): HTTP headers
        cookies (dict): Browser cookies
        
    Returns:
        requests.Response: Response object from the request
        
    Raises:
        RequestException: For any request-related errors after retries
    """
    try:
        response = requests.get(
            url, 
            cookies=cookies, 
            headers=headers,
            timeout=(3, 10)  # (connect timeout, read timeout)
        )
        response.raise_for_status()
        return response
        
    except Timeout:
        print(f"Timeout occurred while accessing {url}")
        raise
    except ConnectionError as e:
        print(f"Connection error occurred while accessing {url}: {str(e)}")
        raise
    except RequestException as e:
        print(f"Error occurred while accessing {url}: {str(e)}")
        raise
    
def get_basic_data(response):
    """
    Extract basic character information from the page content.
    
    Args:
        response (requests.Response): Response object containing page HTML
        
    Returns:
        dict: Dictionary containing character's basic information
    """
    soup = BeautifulSoup(response.text, 'html.parser')
    td_page_content = soup.find('div', class_='td-page-content')
    paragrafo = td_page_content.find_all('p')[1]
    data = {}

    # Handle different HTML structures for character info
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
    """
    Extract character appearances from the page content.
    
    Args:
        response (requests.Response): Response object containing page HTML
        
    Returns:
        list: List of games where the character appears
    """
    soup = BeautifulSoup(response.text, 'html.parser')
    td_page_content = soup.find('div', class_='td-page-content')
    appearences = [li.text for li in 
                 td_page_content.
                 find('h4').
                 find_next().
                 find_all('li')]

    return appearences

def get_character_data(url):
    """
    Combine basic info and appearances for a character.
    
    Args:
        url (str): Character page URL
        
    Returns:
        dict: Combined character data or None if fetch fails
    """
    try:
        response = get_content(url)
        character_data = get_basic_data(response)
        character_data['Aparicoes'] = get_appearences_data(response)
        return character_data
    except RequestException as e:
        print(f"Failed to get character data for {url}: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error processing character {url}: {str(e)}")
        return None

def get_character_links(url='https://www.residentevildatabase.com/personagens/'):
    """
    Get all character page URLs from the main character listing.
    
    Args:
        url (str): Main characters page URL
        
    Returns:
        list: List of character page URLs
        
    Raises:
        RequestException: If unable to fetch the character listing page
    """
    try:
        response = get_content(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_content = soup.find('div', class_='td-page-content')
        if not page_content:
            raise ValueError("Could not find page content div")
            
        h3s = page_content.find_all('h3')
        if not h3s:
            raise ValueError("No character sections found")

        characters = []
        for h3 in h3s:
            try:
                paragraph = h3.find_next('p')
                if not paragraph:
                    print(f"Warning: No paragraph found after header {h3.text}")
                    continue
                    
                links = paragraph.find_all('a')
                letter_characters = [anchor['href'] for anchor in links if 'href' in anchor.attrs]
                characters.extend(letter_characters)
            except Exception as e:
                print(f"Error processing section {h3.text}: {str(e)}")
                continue

        if not characters:
            raise ValueError("No character links found")
            
        return characters
    except Exception as e:
        print(f"Failed to get character links: {str(e)}")
        raise

try:
    # Get list of all character URLs
    print("Fetching character URLs...")
    characters = get_character_links()
    print(f"Found {len(characters)} characters")

    # Scrape data for each character
    data_list = []
    for url in tqdm(characters, desc="Scraping characters"):
        character_data = get_character_data(url)
        if character_data:
            character_data['url'] = url
            data_list.append(character_data)
        else:
            print(f"Warning: Unable to fetch data for {url}")

    if not data_list:
        raise ValueError("No character data was collected")

    # Create DataFrame and ensure directory exists
    print("Saving data to parquet...")
    df = pd.DataFrame(data_list)
    
    # Create the dados directory if it doesn't exist
    import os
    os.makedirs('dados', exist_ok=True)
    
    # Save to parquet
    df.to_parquet('dados/personagens.parquet', index=False)
    
    # Verify data
    print("Verifying saved data...")
    df_parquet = pd.read_parquet('dados/personagens.parquet')
    print(f"Successfully saved data for {len(df_parquet)} characters")
    print("\nSample of characters with wrong birth dates field:")
    print(df[~df['de nascimento'].isna()])
    print("\nFirst few records:")
    print(df_parquet.head())

except Exception as e:
    print(f"Critical error: {str(e)}")
    raise
