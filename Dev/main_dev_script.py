import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin

def visit_url():
    url = input("Please provide the URL you'd like to visit: ")

    print("Visiting", url)
    try:
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            print("Successfully landed on", url)

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, 'html.parser')

            # Find all <a> tags with class "lightsaber-link"
            lightsaber_links = soup.find_all('a', class_='lightsaber-link')

            # Initialize lists to store names and email addresses
            names = []
            emails = []

            # Extract names from lightsaber_links and visit hrefs
            for link in lightsaber_links:
                # Copy the name
                name = link.text.strip()
                names.append(name)
                print(name)

                # Visit the href and look for the email address
                href = link.get('href')
                if href:
                    # Ensure complete URL
                    href = urljoin(url, href)

                    # Visit the href
                    response_sub = requests.get(href)

                    # Parse the HTML content of the subpage
                    sub_soup = BeautifulSoup(response_sub.content, 'html.parser')

                    # Find <div> with class "email-address__address label-above"
                    email_div = sub_soup.find('div', class_='email-address__address label-above')
                    if email_div:
                        # Find <a> tag inside the div
                        email_link = email_div.find('a')
                        if email_link:
                            email = email_link.text.strip()
                            emails.append(email)
                            print(email)
                        else:
                            emails.append(None)
                            print(f"No email found for {name}")
                    else:
                        emails.append(None)
                        print(f"No email found for {name}")

                    time.sleep(1)  # Pause for 1 second

            # Write names to "name.txt"
            with open("name.txt", "w") as name_file:
                for name in names:
                    name_file.write(name + "\n")

            # Write emails to "email.txt"
            with open("email.txt", "w") as email_file:
                for email in emails:
                    if email:
                        email_file.write(email + "\n")

            print("Names and emails have been written to files.")

        else:
            print("Failed to land on", url)
    except Exception as e:
        print("An error occurred:", e)

visit_url()
