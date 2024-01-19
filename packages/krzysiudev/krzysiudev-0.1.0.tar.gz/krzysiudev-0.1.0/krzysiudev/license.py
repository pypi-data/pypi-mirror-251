import requests
from colorama import Fore

class License():
    def __init__(self):
        self.license_key = "test"
        self.user_id = "000"
        self.url = f"http://profmc.pl/licenseSystem/check.php?license_key={self.license_key}&user_id={self.user_id}"

    def check(self):
        try:
            url = self.url
            response = requests.get(url=url)
            data = response.json()
            if data['valid'] == True:
                print(f"{Fore.GREEN}[OK] Your license is valid until {data['expiration_date']}!")
                return True
            else:
                print(f'{Fore.RED}[BAD] Your license is invalid!')
                return False
        except Exception as e:
            print(f'{Fore.RED}[ERROR] Connection error! {e}')