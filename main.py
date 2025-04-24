import configparser
import json
import asyncio
import json
import time
import string
import random
from binance.client import Client
api_key = ""          #Kendi Binance Hesabınıza giriş yaptıktan sonra https://bit.ly/3tbqNvJ
api_secret = ""       #Linkinden api_key ve api_secret alın, yoksa kod çalışmayacaktır.
from datetime import date, datetime
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import (GetHistoryRequest)
from telethon.tl.types import (
    PeerChannel
)

asciiletters = string.ascii_letters
randomFilename = ''.join(random.choice(asciiletters) for i in range(5)) 
print("Mesaj Dosyası İsmi: " + randomFilename + ".txt")
# some functions to parse json date
class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()

        if isinstance(o, bytes):
            return list(o)

        return json.JSONEncoder.default(self, o)


# Reading Configs
config = configparser.ConfigParser()
config.read("config.ini")

# Setting configuration values
api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']

api_hash = str(api_hash)

phone = config['Telegram']['phone']
username = config['Telegram']['username']

# Create the client and connect
client = TelegramClient(username, api_id, api_hash)

async def main(phone):
    await client.start()
    print("Client Created")
    # Ensure you're authorized
    if await client.is_user_authorized() == False:
        await client.send_code_request(phone)
        try:
            await client.sign_in(phone, input('Enter the code: '))
        except SessionPasswordNeededError:
            await client.sign_in(password=input('Password: '))

    me = await client.get_me()

    user_input_channel = ""               #Telegram Grup Linki

    if user_input_channel.isdigit():
        entity = PeerChannel(int(user_input_channel))
    else:
        entity = user_input_channel

    my_channel = await client.get_entity(entity)

    offset_id = 0
    limit = 1
    all_messages = []
    total_messages = 0
    total_count_limit = 1

    while True:
        print("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
        history = await client(GetHistoryRequest(
            peer=my_channel,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
        if not history.messages:
            break
        messages = history.messages
        for message in messages:
            all_messages.append(message.to_dict())
        offset_id = messages[len(messages) - 1].id
        total_messages = len(all_messages)
        if total_count_limit != 0 and total_messages >= total_count_limit:
            break

    with open(randomFilename + ".txt", 'a') as outfile:
        json.dump(all_messages, outfile, cls=DateTimeEncoder, indent=1)

with client:
    client.loop.run_until_complete(main(phone))

import json
from binance.client import Client
import re

errors = []
linenum = 0
pattern = re.compile(r"#")
with open (randomFilename + ".txt", 'rt') as myfile:
    for line in myfile:
        linenum += 1
        if pattern.search(line) != None:
            errors.append((linenum, line.rstrip('\n')))
for err in errors:
    print(err[1])
test_string = err[1]
res = test_string.split()
src_str = str(res)
sub_index = src_str.find('#')
sub_index2 = src_str.find('\\')

coin = (src_str)[sub_index+1:sub_index2]
print("Ulaşılan coin: " + coin)

client = Client(api_key, api_secret)
Toplam = float(0.000160)                                #BTC Olarak Toplam Bütçe Girilir, Noktalı Girilmesine Dikkat Edin!
btcprice = client.get_symbol_ticker(symbol='BTCUSDT')   #Piyasadan USDT Bazında BTC Fiyatı Alınır
src_btccoin = str(btcprice)
sub_indexcoin = src_btccoin.find("price")
btc_price = (src_btccoin)[sub_indexcoin+9:sub_indexcoin+14]
finalcoin = coin+"BTC"
resprice = client.get_symbol_ticker(symbol=finalcoin)
src_strcoin = str(resprice)
sub_indexcoin = src_strcoin.find("price")
coin_price = (src_strcoin)[sub_indexcoin+9:sub_indexcoin+19]
print(coin +  " Fiyatı: " + coin_price + " BTC")
print("Toplam Alış: "f'{Toplam:.6f}' + " BTC")
print("BTC Fiyatı: " + btc_price + " $")
print("Toplam Dolar Bazlı Fiyat: " + str((float(Toplam) * float(btc_price))) + " $")

configtime = configparser.ConfigParser()
configtime.read("zaman.ini")
zaman = configtime['Zaman']['zaman']

qtypull = client.get_symbol_info(finalcoin)
src_qtypullsearch = str(qtypull)
sub_qtypull = src_qtypullsearch.find("'minQty': '1.00000000'")

if sub_qtypull != -1:
    floatpoint = 0
else:
    floatpoint = 1

print("Float Point = " + str(floatpoint))
lastprice = client.get_ticker(symbol=finalcoin)
src_lastpricecoin = str(resprice)
sub_indexcoin2 = src_lastpricecoin.find("price")
guncelFiyat = float((src_lastpricecoin)[sub_indexcoin2+9:sub_indexcoin2+19])
alinacak = round((Toplam/guncelFiyat),floatpoint)
print(str(float(alinacak)) + " " + coin + "$")


client.order_market_buy(
    symbol=finalcoin,
    quantity=alinacak)
print("Alış İşlemi Başarılı")

while (time.strftime('%I:%M:%S %p') != zaman):  
    print("Süre Bekleniyor...")
    time.sleep(1)

openOrders = client.get_open_orders(symbol=finalcoin)
if openOrders == []:
    client.order_market_sell(
    symbol=finalcoin,
    quantity=alinacak)
else:
    print("Tekrar Deneniyor...")
    time.sleep(0.5)
    if openOrders == []:
        client.order_market_sell(
        symbol=finalcoin,
        quantity=alinacak)

print("Satış İşlemi Başarılı!")
bal = client.get_asset_balance(asset='BTC')
src_strbal = str(bal)
sub_indexbal = src_strbal.find('free')
finalBal = (src_strbal)[sub_indexbal+8:sub_indexbal+16]
print("Anlık BTC Bakiye: " + finalBal)

while True:
    giris = input("Pencereyi Kapatmak İçin Aşağıdaki Bölüme 'Tamam' Yazınız...")
    if giris == "Tamam":
        break
    elif giris == "tamam":
        break
    elif giris == "TAMAM":
        break