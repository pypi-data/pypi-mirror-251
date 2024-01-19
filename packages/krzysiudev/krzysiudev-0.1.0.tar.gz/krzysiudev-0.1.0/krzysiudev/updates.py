import requests
from colorama import Fore


class Update():
    def __init__(self):
        self.program = "test"
        self.version = "1.0"
        self.url = f"https://raw.githubusercontent.com/ProfKrzys/programs/main/updates/{self.program}" 

    def check(self):
        try:
            url = self.url
            response = requests.get(url)
            print(response)
            data = response.json()
            if data["version"] == self.version:
                print(Fore.GREEN + f"{Fore.GREEN}[OK] The program is in the latest version!")
                return True
            else:
                print(Fore.RED + f"{Fore.RED}[BAD] A new version of the program is available {Fore.GREEN}{data['version']}{Fore.RED}! Download it from: {Fore.GREEN}{data['url']}")
        except Exception as e:
            print(Fore.RED + f"{Fore.RED}[ERROR] An error occurred while checking for updates! {e}")