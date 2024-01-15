import requests
from bs4 import BeautifulSoup

def auth(tc, password):
    def clean_html(html):
        cleaned = html.replace('<tr class="gray">', "").replace('<td>', "").replace('</td>', "").replace("<tr>", "").replace("</tr>", "")
        return cleaned.split("\n")[2].strip()  # Add .strip() to remove leading/trailing whitespace

    login_url = "https://bilgimerkezi.bilfenlisesi.com/login"
    secure_url = "https://bilgimerkezi.bilfenlisesi.com/"
    profile_url = "https://bilgimerkezi.bilfenlisesi.com/profil"

    payload = {
        "tc": tc,
        "password": password
    }

    with requests.session() as session1:
        try:
            r1 = session1.post(login_url, data=payload)
            r1.raise_for_status()  # Check for request errors
        except requests.exceptions.RequestException as e:
            print(f"Authentication Failed: {e}")
            return False

        if r1.url == secure_url:
            print("Authentication Successful.")
        elif r1.url == login_url:
            print("Authentication Failed.")
            return False

        try:
            r2 = session1.get(profile_url)
            r2.raise_for_status()  # Check for request errors
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch profile data: {e}")
            return False

        soup = BeautifulSoup(r2.text, 'html.parser')
        images = soup.find_all('img')
        try:
            with open("Profilepic.png", "wb") as f:
                f.write(requests.get(images[1]['src']).content)
        except (IndexError, requests.exceptions.RequestException) as e:
            print(f"Failed to download profile pic: {e}")

        soup2 = BeautifulSoup(r2.text, "html.parser")
        details = soup2.find_all("tr")

        userdata = {
            'Name': clean_html(str(details[1])),
            'School': clean_html(str(details[2])),
            'tc': tc,
            'Password': password,
            'gender': clean_html(str(details[4])),
            'birthday': clean_html(str(details[6])),
            'schoolno': clean_html(str(details[7])),
            'classroom': clean_html(str(details[8])),
            'address': clean_html(str(details[9])),
            'phonenumber': clean_html(str(details[11])),
            'profilepic': "Userinfo/Profilepic.png"
        }
        print(userdata)
        return True, userdata


# Example usage:
# Bilfen_Auth("your_tc_number", "your_password")
