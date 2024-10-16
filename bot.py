import requests
import json
import os
import urllib.parse
from colorama import *
from datetime import datetime, timedelta
import time
import pytz

wib = pytz.timezone('Asia/Jakarta')

class CFI:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.headers = {
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.9',
            'Cache-Control': 'no-cache',
            # 'Host': 'api.cyberfin.xyz',
            'Origin': 'https://g.cyberfin.xyz',
            'Pragma': 'no-cache',
            'Referer': 'https://g.cyberfin.xyz/',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0'
        }

    def clear_terminal(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def log(self, message):
        print(
            f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%d-%m-%Y %H:%M:%S')} WIB ]{Style.RESET_ALL}"
            f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}{message}",
            flush=True
        )

    def welcome(self):
        print(
            f"""
        {Fore.GREEN + Style.BRIGHT}Auto Claim {Fore.BLUE + Style.BRIGHT}Cyber Finance - BOT
            """
            f"""
        {Fore.GREEN + Style.BRIGHT}Rey? {Fore.YELLOW + Style.BRIGHT}<INI WATERMARK>
            """
        )

    def format_seconds(self, seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def load_data(self, query: str):
        query_params = urllib.parse.parse_qs(query)
        query = query_params.get('user', [None])[0]

        if query:
            user_data_json = urllib.parse.unquote(query)
            user_data = json.loads(user_data_json)
            first_name = user_data['first_name']
            return first_name
        else:
            raise ValueError("User data not found in query.")

    def access_token(self, query: str, retries=3, delay=2):
        url = 'https://api.cyberfin.xyz/api/v1/game/initdata'
        data = json.dumps({'initData': query})
        self.headers.update({
            'Content-Type': 'application/json'
        })

        for attempt in range(retries):
            try:
                response = self.session.post(url, headers=self.headers, data=data)
                if response.status_code == 201:
                    result = response.json()
                    if result['code'] == 200:
                        return result['message']['accessToken']
                    else:
                        self.log(f"{Fore.RED+Style.BRIGHT}[ Query Mokad ]{Style.RESET_ALL}")
                        return None
                else:
                    return None
            except (requests.RequestException, requests.HTTPError, ValueError) as e:
                print(
                    f"{Fore.CYAN + Style.BRIGHT}[ {datetime.now().astimezone(wib).strftime('%d-%m-%Y %H:%M:%S')} WIB ]{Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT} | {Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT}[ HTTP ERROR ]{Style.RESET_ALL}"
                    f"{Fore.YELLOW+Style.BRIGHT} Retrying... [{attempt + 1}/{retries}] {Style.RESET_ALL}",
                    end="\r",
                    flush=True
                )
                time.sleep(delay)
        self.log(f"{Fore.RED+Style.BRIGHT}Semua percobaan gagal.{Style.RESET_ALL}")
        return None
        
    def game_data(self, token: str):
        url = 'https://api.cyberfin.xyz/api/v1/game/mining/gamedata'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        })

        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            if result['code'] == 200:
                return result['message']
            else:
                self.log(f"{Fore.RED+Style.BRIGHT}[ Query Mokad ]{Style.RESET_ALL}")
                return None
        else:
            return None
        
    def boost_info(self, token: str):
        url = 'https://api.cyberfin.xyz/api/v1/mining/boost/info'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        })

        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            if result['code'] == 200:
                return result['message']
            else:
                return None
        else:
            return None
        
    def upgrade_boost(self, token: str, type: str):
        url = 'https://api.cyberfin.xyz/api/v1/mining/boost/apply'
        data = json.dumps({'boostType': type})
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        })

        response = self.session.post(url, headers=self.headers, data=data)
        if response.status_code == 201:
            result = response.json()
            if result['code'] == 200:
                return result['message']
            else:
                return None
        else:
            return None
        
    def claim_daily(self, token: str):
        url = 'https://api.cyberfin.xyz/api/v1/mining/claim/daily'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Content-Length': '0'
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            result = response.json()
            if result['code'] == 200:
                return result['message']
            else:
                return None
        else:
            return None
        
    def claim_mining(self, token: str):
        url = 'https://api.cyberfin.xyz/api/v1/mining/claim'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        })

        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            if result['code'] == 200:
                return result['message']
            else:
                return None
        else:
            return None
        
    def ads_count(self, token: str):
        url = 'https://api.cyberfin.xyz/api/v1/ads/count'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        })

        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            if result['code'] == 200:
                return result['message']
            else:
                return None
        else:
            return None
        
    def watch_ads(self, token: str):
        url = 'https://api.cyberfin.xyz/api/v1/ads/log'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        })

        response = self.session.post(url, headers=self.headers)
        if response.status_code == 201:
            result = response.json()
            if result['code'] == 200:
                return result['message']
            else:
                return None
        else:
            return None
        
    def game_tasks(self, token: str):
        url = 'https://api.cyberfin.xyz/api/v1/gametask/all'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        })

        response = self.session.get(url, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            if result['code'] == 200:
                return result['message']
            else:
                return None
        else:
            return None
        
    def complete_tasks(self, token: str, task_id: str):
        url = f'https://api.cyberfin.xyz/api/v1/gametask/complete/{task_id}'
        self.headers.update({
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
        })

        response = self.session.patch(url, headers=self.headers)
        if response.status_code == 200:
            result = response.json()
            if result['code'] == 200:
                return result['message']
            else:
                return None
        else:
            return None
        
    def question(self):
        while True:
            hammer_upgrade = input("Upgrade Hammer Level? [y/n] -> ").strip().lower()
            if hammer_upgrade in ["y", "n"]:
                hammer_upgrade = hammer_upgrade == "y"
                break
            else:
                print(f"{Fore.RED+Style.BRIGHT}Invalid Input.{Fore.WHITE+Style.BRIGHT} Choose 'y' to upgrade or 'n' to skip.{Style.RESET_ALL}")
        hammer_count = 0
        if hammer_upgrade:
            while True:
                try:
                    hammer_count = int(input("How many times? -> "))
                    if hammer_count > 0:
                        break
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")
        
        while True:
            egg_upgrade = input("Upgrade Egg Level? [y/n] -> ").strip().lower()
            if egg_upgrade in ["y", "n"]:
                egg_upgrade = egg_upgrade == "y"
                break
            else:
                print(f"{Fore.RED+Style.BRIGHT}Invalid Input.{Fore.WHITE+Style.BRIGHT} Choose 'y' to upgrade or 'n' to skip.{Style.RESET_ALL}")
        egg_count = 0
        if egg_upgrade:
            while True:
                try:
                    egg_count = int(input("How many times? -> "))
                    if egg_count > 0:
                        break
                    else:
                        print(f"{Fore.RED+Style.BRIGHT}Please enter a positive number.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED+Style.BRIGHT}Invalid input. Enter a number.{Style.RESET_ALL}")

        return hammer_upgrade, hammer_count, egg_upgrade, egg_count
    
    def upgrade_process(self, token, upgrade_type, count):
        for i in range(count):
            result = self.upgrade_boost(token, upgrade_type)
            if result:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Upgarde Boost ]{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} [ {upgrade_type.capitalize()} ] {Style.RESET_ALL}"
                    f"{Fore.GREEN+Style.BRIGHT}[{i + 1}/{count}]{Style.RESET_ALL}"
                )
            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Upgarde Boost ]{Style.RESET_ALL}"
                    f"{Fore.WHITE+Style.BRIGHT} [ {upgrade_type.capitalize()} ] {Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT}[{i + 1}/{count}]{Style.RESET_ALL}"
                )
            time.sleep(2)
        
    def process_query(self, query: str, hammer_upgrade, hammer_count, egg_upgrade, egg_count):

        account = self.load_data(query)
        if account:
            self.log(
                f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                f"{Fore.WHITE+Style.BRIGHT} {account} {Style.RESET_ALL}"
                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
            )
            time.sleep(1)
            
        token = self.access_token(query)
        time.sleep(1)
        if token:
            
            data = self.game_data(token)
            if data:
                boost = self.boost_info(token)
                if boost:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Balance{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {data['userData']['balance']} $xCFI {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Hammer{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} Level {boost['hammerLevel']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Timer{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} Level {boost['eggLevel']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}                       "
                    )
                time.sleep(1)

                if hammer_upgrade:
                    self.upgrade_process(token, "HAMMER", hammer_count)

                if egg_upgrade:
                    self.upgrade_process(token, "EGG", egg_count)

                if not data['dailyRewardsData']['isClaimed']:
                    claim_daily = self.claim_daily(token)
                    time.sleep(1)
                    if claim_daily:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Daily Login{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Reward{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {claim_daily['reward']} $xCFI {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Streak{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {data['dailyRewardsData']['currentDay']} {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}Day ]{Style.RESET_ALL}                       "
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Daily Login{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Failed to Claim {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Daily Login{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Already Claimed Today {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Streak{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {data['dailyRewardsData']['currentDay']} {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}Day ]{Style.RESET_ALL}                       "
                    )
                time.sleep(1)

                crack_time = data['miningData']['crackTime']
                crack_date = datetime.fromtimestamp(crack_time).astimezone(wib).strftime('%d-%m-%Y %H:%M:%S')
                now = datetime.now().astimezone(wib)

                if now >= datetime.fromtimestamp(crack_time).astimezone(wib):
                    claim_mining = self.claim_mining(token)
                    if claim_mining:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                            f"{Fore.GREEN+Style.BRIGHT} Claimed {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}] [ Balance Now{Style.RESET_ALL}"
                            f"{Fore.WHITE+Style.BRIGHT} {claim_mining['userData']['balance']} $xCFI {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                    else:
                        self.log(
                            f"{Fore.MAGENTA+Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                            f"{Fore.RED+Style.BRIGHT} Failed to Claim {Style.RESET_ALL}"
                            f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                        )
                else:
                    self.log(
                        f"{Fore.MAGENTA+Style.BRIGHT}[ Mining{Style.RESET_ALL}"
                        f"{Fore.YELLOW+Style.BRIGHT} Not Time to Claim {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}] [ Next Claim at{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {crack_date} WIB {Style.RESET_ALL}"
                        f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                    )
                time.sleep(1)

            else:
                self.log(
                    f"{Fore.MAGENTA+Style.BRIGHT}[ Account{Style.RESET_ALL}"
                    f"{Fore.RED+Style.BRIGHT} {account} {Style.RESET_ALL}"
                    f"{Fore.MAGENTA+Style.BRIGHT}Failed To Load Game Data ]{Style.RESET_ALL}"
                )
            time.sleep(1)

            ads = self.ads_count(token)
            if ads:
                count = ads['amountLeftToView']
                if count != 0:
                    while count > 0:
                        watch = self.watch_ads(token)
                        if watch:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Watch{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} Ads {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {watch['value']} $xCFI {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Watch{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} Ads {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}Failed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)

                        count -= 1
                else:
                    self.log(f"{Fore.YELLOW+Style.BRIGHT}[ Oh Sorry, Ads have Reached Their Limit ]{Style.RESET_ALL}")
            else:
                self.log(f"{Fore.YELLOW+Style.BRIGHT}[ Ads Not Found ]{Style.RESET_ALL}")
            time.sleep(1)

            tasks = self.game_tasks(token)
            if tasks:
                for task in tasks:
                    task_id = task['uuid']

                    if not task['isCompleted'] and task['isActive']:
                        complete = self.complete_tasks(token, task_id)
                        if complete:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                                f"{Fore.GREEN+Style.BRIGHT}is Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ] [ Reward{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['pointsReward']} $xCFI {Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT}]{Style.RESET_ALL}"
                            )
                        else:
                            self.log(
                                f"{Fore.MAGENTA+Style.BRIGHT}[ Task{Style.RESET_ALL}"
                                f"{Fore.WHITE+Style.BRIGHT} {task['title']} {Style.RESET_ALL}"
                                f"{Fore.RED+Style.BRIGHT}is Not Completed{Style.RESET_ALL}"
                                f"{Fore.MAGENTA+Style.BRIGHT} ]{Style.RESET_ALL}"
                            )
                        time.sleep(1)
                            
            else:
                self.log(f"{Fore.YELLOW+Style.BRIGHT}[ Task Not Found ]{Style.RESET_ALL}")
            time.sleep(1)

        else:
            self.log(f"{Fore.RED+Style.BRIGHT}[ Query Mati ]{Style.RESET_ALL}")

    def main(self):
        try:
            with open('data.txt', 'r') as file:
                queries = [line.strip() for line in file if line.strip()]

            hammer_upgrade, hammer_count, egg_upgrade, egg_count = self.question()

            while True:
                self.clear_terminal()
                self.welcome()
                self.log(
                    f"{Fore.GREEN + Style.BRIGHT}Account's Total: {Style.RESET_ALL}"
                    f"{Fore.WHITE + Style.BRIGHT}{len(queries)}{Style.RESET_ALL}"
                )
                self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                
                for query in queries:
                    query = query.strip()
                    if query:
                        self.process_query(query, hammer_upgrade, hammer_count, egg_upgrade, egg_count)
                        self.log(f"{Fore.CYAN + Style.BRIGHT}-{Style.RESET_ALL}"*75)
                        
                seconds = 1800
                while seconds > 0:
                    formatted_time = self.format_seconds(seconds)
                    print(
                        f"{Fore.CYAN+Style.BRIGHT}[ Wait for{Style.RESET_ALL}"
                        f"{Fore.WHITE+Style.BRIGHT} {formatted_time} {Style.RESET_ALL}"
                        f"{Fore.CYAN+Style.BRIGHT}... ]{Style.RESET_ALL}",
                        end="\r"
                    )
                    time.sleep(1)
                    seconds -= 1

        except KeyboardInterrupt:
            self.log(f"{Fore.RED + Style.BRIGHT}[ EXIT ] Cyber Finance - BOT{Style.RESET_ALL}")
        except Exception as e:
            self.log(f"{Fore.RED + Style.BRIGHT}An error occurred: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    cfi = CFI()
    cfi.main()