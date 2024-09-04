import requests
from bs4 import BeautifulSoup

# Supabase URL and API Key
SUPABASE_URL = "https://ailogxgeobaebkemxgho.supabase.co"  # Replace with your actual Supabase project URL
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFpbG9neGdlb2JhZWJrZW14Z2hvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU0NDAxNzEsImV4cCI6MjA0MTAxNjE3MX0.YJD16IimFgt2xfoYt5JoLUmYVtt37RlxTfYJmN4TMcQ"  # Replace with your actual Supabase API key
SUPABASE_TABLE = "disruptions"  # Replace with your table name

# Function to insert data into Supabase
def insert_into_supabase(data):
    url = f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print("Data inserted successfully")
    else:
        print(f"Failed to insert data: {response.status_code}, {response.text}")

# URL of the webpage containing the HTML element
url = "https://www.nationalrail.co.uk/status-and-disruptions/"  # Replace with the actual URL

try:
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the section containing the disruption information
    section = soup.find("section", class_="styled__NotificationBoxListWrapper-sc-nisfz3-4 bvLDEA")

    if section:  # Check if section is found before accessing its attributes
        # Extract the headline
        headline = section.find("h2").text

        # Find all the disruption items
        disruption_items = section.find_all("li", class_="styled__StyledNotificationListItem-sc-nisfz3-3 dZudnM")

        # Iterate through each disruption item and extract details
        for item in disruption_items:
            # Extract the link
            link = item.find("a").get("href")

            # Extract the summary
            summary = item.find("p", class_="styled__StyledParagraph-sc-1bdsaxr-1 dAAkXV").text

            # Create a data dictionary
            data = {
                "headline": headline,
                "link": link,
                "summary": summary
            }

            # Insert the data into Supabase
            insert_into_supabase(data)

            # Print the extracted information (optional)
            print(f"Headline: {headline}")
            print(f"Link: {link}")
            print(f"Summary: {summary}")
            print("-" * 30)
    else:
        print("Section element not found. Disruption information might be unavailable or the website structure might have changed.")

except requests.exceptions.RequestException as e:
    print(f"An error occurred while fetching the webpage: {e}")
