import requests
from bs4 import BeautifulSoup

def fetch_market_prices_full():
    url = "https://agmarknet.gov.in/SearchCmmMkt.aspx"
    params = {
        'Tx_Commodity': '19',  # Banana
        'Tx_State': 'KK',       # Karnataka
        'Tx_District': '6',     # Davangere
        'Tx_Market': '114',     # Davangere Market
        'DateFrom': '14-Aug-2025',
        'DateTo': '14-Aug-2025',
        'Fr_Date': '14-Aug-2025',
        'To_Date': '14-Aug-2025',
        'Tx_Trend': '0',
        'Tx_CommodityHead': 'Banana',
        'Tx_StateHead': 'Karnataka',
        'Tx_DistrictHead': 'Davangere',
        'Tx_MarketHead': 'Davangere'
    }

    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', {'class': 'tableagmark_new'})
    if not table:
        return {'error': 'Price table not found'}

    all_rows = []

    # Skip header row
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) >= 10:
            try:
                row_data = {
                    'sl_no': cols[0].text.strip(),
                    'district': cols[1].text.strip(),
                    'market': cols[2].text.strip(),
                    'commodity': cols[3].text.strip(),
                    'variety': cols[4].text.strip(),
                    'grade': cols[5].text.strip(),
                    'min_price': float(cols[6].text.strip()),
                    'max_price': float(cols[7].text.strip()),
                    'modal_price': float(cols[8].text.strip()),
                    'price_date': cols[9].text.strip()
                }
                all_rows.append(row_data)
            except ValueError:
                continue  # Skip rows with invalid numeric data

    return all_rows

# Example usage

