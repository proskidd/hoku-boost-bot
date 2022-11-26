from core.logger import logger
import core.setup
import httpx, requests
from capmonster_python import HCaptchaTask
import time, yaml


data = core.setup.setup()

class boosting:            
    def __init__(self) -> None:
        self.session = httpx.Client()
        self.name = data.user
        self.bio = data.bio
        self.capmonster = data.capmonster

    def remove(self, token: str, user):
        with open(f'users/{user}.txt', "r") as f:
            Tokens = f.read().split("\n")
            for t in Tokens:
                if len(t) < 5 or t == token:
                    Tokens.remove(t)
            open(f'users/{user}.txt', "w").write("\n".join(Tokens))

    def boost(self, user, invite: str, amount: int):
        self.invite = invite; done = 0 
        for token in open(f'users/{user}.txt', 'r').read().splitlines():
            if done >= amount:
                return
            self.headers = self.get_headers(token)
            boost_data = self.session.get(f"https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots", headers=self.headers)
            if boost_data.status_code == 200:
                if len(boost_data.json()) != 0:
                    joined = self.join(invite)
                    if joined:
                        logger().success(f"Attemping to Join with: ({token})")

                        for boost in boost_data.json():
                            if done >= amount:
                                self.remove(token, user)
                            boost_id = boost["id"]
                            bosted = self.do_boost(boost_id)
                            if bosted:
                                logger().success(f"SuccesFully Boosted Once (Server invite:{invite}) Used Token :({token})")
                                done += 1
                            else:
                                logger().error(f"Boost Used Or some other error: {token}")
                        if data.cbio:
                            self.change_bio()
                        if data.cuser:
                            self.change_guild_name()    
                        self.remove(token, user)
                    else:   
                        logger().error(f"Error Joining : {token}")
                else:
                    self.remove(token, user)
                    logger().error(f"Token Doesnt have nitro:  {token}")

    def get_cookies(self):
        s = requests.Session()
        s.get("https://discord.com")
        cookies = s.cookies.get_dict()
        __dcfduid = cookies.get("__dcfduid")
        __sdcfduid = cookies.get("__sdcfduid")
        logger().info(f"Fetched Cookies: ({__dcfduid[:20]}), ({__sdcfduid[:20]})")
        s.close()
        return __dcfduid, __sdcfduid

    def get_fingerprint(self):
        data = self.session.get("https://discord.com/api/v9/experiments")
        fingerprint = data.json()['fingerprint']
        logger().info(f"Got Fingerprint: ({fingerprint})")
        return fingerprint


    def get_headers(self, token):
        __dcfduid, __sdcfduid = self.get_cookies()
        headers = {
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate',
                'accept-language': 'en-GB',
                'authorization': token,
                'content-type': 'application/json',
                'origin': 'https://discord.com',
                'referer': 'https://discord.com/channels/@me',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'cookie': f'__dcfduid={__dcfduid}; __sdcfduid={__sdcfduid}; locale=en-GB',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.1.9 Chrome/83.0.4103.122 Electron/9.4.4 Safari/537.36',
                'x-debug-options': 'bugReporterEnabled',
                'x-fingerprint': self.get_fingerprint(),
                'x-context-properties': 'eyJsb2NhdGlvbiI6IlVzZXIgUHJvZmlsZSJ9',
                'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjAuMS45Iiwib3NfdmVyc2lvbiI6IjEwLjAuMTc3NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTM1NTQsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9',
                'te': 'trailers',
            }
        return headers

    def solve(self, sitekey):
        for i in range(10):
            try:
                cap = HCaptchaTask(self.capmonster)
                task = cap.create_task("https://discord.com/channels/@me", sitekey)
                time.sleep(1)
                solution = cap.get_task_result(task)["gRecaptchaResponse"]
                logger().success(f"Solved Captcha Task: ({solution[:75]}...)")
                break
            except TypeError:
                continue
        return solution

    def join(self, invite):
        self.headers["content-type"] = 'application/json'
        for i in range(5):
            r = self.session.post(f"https://discord.com/api/v9/invites/{invite}", headers=self.headers, json={})
            if r.status_code == 200:
                self.guild_id = r.json()["guild"]["id"]
                join_outcome = True
                break
            if "captcha_sitekey" in r.text:
                sitekey = r.json()['captcha_sitekey']
                solution = self.solve(sitekey)
            r = self.session.post(f"https://discord.com/api/v9/invites/{invite}", headers=self.headers, json={"captcha_key": solution})
            if r.status_code == 200:
                self.guild_id = r.json()["guild"]["id"]
                join_outcome = True
                break
            else:
                logger().error(r.text)
            
        return join_outcome

    def do_boost(self, boost_id):
        boost_data = {"user_premium_guild_subscription_slot_ids": [boost_id]}
        boosted = self.session.put(f"https://discord.com/api/v9/guilds/{self.guild_id}/premium/subscriptions", json=boost_data, headers=self.headers)
        if boosted.status_code == 201:
            return True
        else:
            return False

    def change_bio(self):
        logger().info(f"Trying to Change bio")
        r = self.session.patch("https://discord.com/api/v9/users/@me", headers=self.headers, json = {'bio': self.bio})
        if r.status_code == 200:
            logger().success(f"Renamed Bio to {self.bio}")
        else:
            logger().error(f"Couldn't rename bio: {r.json()}")

    def change_guild_name(self):
        logger().info(f"Attemping to Change Nickname")
        r = self.session.patch(f"https://discord.com/api/v9/guilds/{self.guild_id}/members/@me", headers=self.headers, json={"nick": self.name})
        if r.status_code == 200:
            logger().success(f"Succesfully Renamed Used to: {self.name}")
        else:
            logger().error(f"Couldn't rename user: {r.json()}")