import requests
from bs4 import BeautifulSoup

# Define the URL of the webpage
url = "https://www.gem.wiki/Category:Solar_farms"

# Send a GET request to the URL
response = requests.get(url)

print(response)
# Create a BeautifulSoup object to parse the HTML content
soup = BeautifulSoup(response.content, "html.parser")

# Print the parsed HTML content
print(soup.prettify())

# for each href in the soup, print the href
for link in soup.find_all('a'):
    print(link.get('href'))


# create a list of the links
links = [link.get('href') for link in soup.find_all('a')]

# filter out the links that don't include solar 
solar_links = [link for link in links if link and "solar" in link.lower()]

print(solar_links)



# Find all table elements on the webpage
tables = soup.find_all("table")

# Iterate over each table
for table in tables:
    # Find all rows in the table
    rows = table.find_all("tr")
    
    # Iterate over each row
    for row in rows:
        # Find all cells in the row
        cells = row.find_all("td")
        
        # Extract the data from each cell
        data = [cell.text.strip() for cell in cells]
        
        # Do something with the extracted data
        print(data)