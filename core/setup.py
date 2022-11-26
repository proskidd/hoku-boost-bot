import yaml
from core.logger import logger
import time, os

class setup:
    def __init__(self):
        self.data = yaml.load(open("config.yml"), Loader=yaml.FullLoader) 
        self.statuses = ["online", "do_not_disturb", "idle"]
        self.activities = ["playing", "listening", "streaming", "watching", "competing"]

        self.misc = self.data["misc"]
        self.capmonster = self.misc["capmonster"]
        self.main = self.misc["main_stock"]


        self.settings_main = self.data["bot settings"]["main"]

        self.status_type = self.settings_main["status"]
        self.token = self.settings_main["token"]
        self.acti_type = self.settings_main["activity_type"]
        self.activity = self.settings_main["activity"]
        self.prefix = self.settings_main["prefix"]

        self.settings_other = self.data["bot settings"]["other"]

        self.guild = self.settings_other["guild_id"]
        self.admins = self.settings_other["admins"]


        self.commands = self.data["commands"]

        self.boost = self.commands["boost"]
        self.stock = self.commands["stock"]
        self.restock = self.commands["restock"]
        self.send = self.commands["send_tokens"]
        self.reformat = self.commands["reformat"]
        self.acti = self.commands["activity"]
        self.license = self.commands["license"]
        self.payment = self.commands["payments"]


        self.watermark_data = self.data["watermark settings"]["data"]
        self.watermarks = self.data["watermark settings"]["watermarks"]

        self.cuser = self.watermark_data["change_nick"]
        self.cbio = self.watermark_data["change_bio"]
        self.user = self.watermarks["username"]
        self.bio = self.watermarks["bio"]


        self.payments = self.data["payments"]

        self.p_data = self.payments["data"]
        self.d_pp = self.p_data["Paypal"]
        self.d_ca = self.p_data["Cashapp"]
        self.d_btc = self.p_data["Bitcoin"]
        self.d_ltc = self.p_data["Litecoin"]
        self.d_eth = self.p_data["Ethereum"]
        self.d_sol = self.p_data["Solana"]
        self.d_mon = self.p_data["Monero"]
        self.d_bhc = self.p_data["Bitcoin Cash"]

        self.tag = self.payments["addresses"]
        self.paypal = self.tag["Paypal"]
        self.cashapp = self.tag["Cashapp"]
        self.bitcoin = self.tag["Bitcoin"]
        self.litecoin = self.tag["Litecoin"]
        self.ethereum = self.tag["Ethereum"]
        self.solana = self.tag["Solana"]
        self.monero = self.tag["Monero"]
        self.bit_cash = self.tag["Bitcoin Cash"]

        self.emoji = self.payments["emojis"]
        self.pp = self.emoji["Paypal"]
        self.capp = self.emoji["Cashapp"]
        self.btc = self.emoji["Bitcoin"]
        self.ltc = self.emoji["Litecoin"]
        self.eth = self.emoji["Ethereum"]
        self.sol = self.emoji["Solana"]
        self.mon = self.emoji["Monero"]
        self.bhc = self.emoji["Bitcoin Cash"]

    def print_data(self):
        if self.status_type not in self.statuses: logger().error(f"Invalid status: {self.status_type}, change to a valid one from {self.statuses}")
        elif self.acti_type not in self.activities: logger().error(f"Invalid activity type: {self.acti_type}, select a valid one from: {self.activities}")
        else:
            logger().info(f"- Token: {self.token}")
            logger().info(f"- Status: {self.status_type}")
            logger().info(f"- Activity: {self.activity}")
            logger().info(f"- Guild: {self.guild}")
            logger().info(f"- Captcha key: {self.capmonster}")
            logger().info(f"- Main Stock: {self.main}")
            logger().info(f"- Boost: {self.boost}")
            logger().info(f"- Stock: {self.stock}")
            logger().info(f"- Restock: {self.restock}")
            logger().info(f"- Send Tokens: {self.send}")
            logger().info(f"- Reformat: {self.reformat}")
            logger().info(f"- Activity: {self.acti}")
            logger().info(f"- License: {self.license}")
            logger().info(f"- Payments: {self.payment}")
            logger().info(f"- Change User: {self.cuser}")
            logger().info(f"- Change Bio: {self.cbio}")
            logger().info(f"- Paypal: {self.d_pp}")
            logger().info(f"- Cashapp: {self.d_ca}")
            logger().info(f"- Bitcoin: {self.d_btc}")
            logger().info(f"- Litecoin: {self.d_ltc}")
            logger().info(f"- Ethereum: {self.d_eth}")
            logger().info(f"- Solana: {self.d_sol}")
            logger().info(f"- Monero: {self.d_mon}")
            logger().info(f"- Bitcoin Cash: {self.d_bhc}")

        time.sleep(10)
        os.system('cls')