# [assistant-tgbot](https://github.com/bishalqx980/assistant-tgbot)

This is a Telegram bot designed to maintain the owner's anonymity by forwarding received messages directly to the owner. It also includes additional features such as broadcasting messages to all active users, retrieving user IDs and information, and more. The bot is developed using the `python-telegram-bot` library (v22.1).

**A simple assistant telegram bot**
- **This bot can be found as [Eva](https://t.me/EvaTheLovebot) on Telegram.**

> **Looking for Ultimate All-in-one Telegram Bot? Checkout [tgbot](https://github.com/bishalqx980/tgbot)**

## Deploy your own bot 👩‍🚀

**Steps**

- Preparation 📦
- Host 🚀

**Preparation 📦**
---
- Download & Rename `sample_config.env` to `config.env` then fillup `config.env` file value's

    **⚠️ Note:** _Don't share or upload the `config.env` any public place or repository_

**`config.env` Values**

- `BOT_TOKEN` Get from [https://t.me/BotFather](https://t.me/BotFather) E.g. `123456:abcdefGHIJK...`
- `OWNER_ID` Get from bot by /id command E.g. `2134776547`
- `MONGODB_URI` Get from [https://www.mongodb.com/](https://www.mongodb.com/) (Check Below for instruction)
- `DB_NAME` anything E.g. `MissCiri_db`

**[Creating MongoDB URI](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/#create-a-connection-string)**

> **Note (MongoDB):** _On the left side list click on `Network Access` section click on `ADD IP ADDRESS` and set ip to `0.0.0.0/0` (Its important to access database without network restriction)_

**Host 🚀**
---
**Local Hosting 💻**

- Windows/Linux
    - Required `python 3.11` (also tested on `3.13`)
    - Open `tgbot` directory on cmd/shell
    - Run on cmd/shell `pip install -r requirements.txt`
    - Finally `python -m bot`

**Render Deploy ⚡**

- Signin/Signup on [Render](https://render.com/)
- Goto dashboard & create a New `Web Service`
- Select `Public Git Repository`: `https://github.com/bishalqx980/tgbot`
- Then 👇
    ```
    > Language: Docker
    > Branch: main
    > Instance Type: Free [or paid]
    ```
- Advanced option 👇
    ```
    Secret Files

    > Filename: 'config.env'
    > File Contents: Paste all content from 'sample_config.env' (make sure you filled up everything)
    ```

    > **Note (Render Hosting):** _If you face anyproblem accessing `Advanced option` then just click on `Create Web Service` then from `Environment` > `Secret Files` and add the `config.env` values. Then restart/redeploy the web service._

    > **Important (Render Hosting):** _After deployment complete go to [Render Dashboard](https://dashboard.render.com/) and open your service then you can see service url on top left corner [https://example.onrender.com]() copy that and server url using `/server` cmd (**So that bot won't go to sleep**)_

---

```
𝓐 𝓹𝓻𝓸𝓳𝓮𝓬𝓽 𝓸𝓯

 ▄▄▄▄    ██▓  ██████  ██░ ██  ▄▄▄       ██▓    
▓█████▄ ▓██▒▒██    ▒ ▓██░ ██▒▒████▄    ▓██▒    
▒██▒ ▄██▒██▒░ ▓██▄   ▒██▀▀██░▒██  ▀█▄  ▒██░    
▒██░█▀  ░██░  ▒   ██▒░▓█ ░██ ░██▄▄▄▄██ ▒██░    
░▓█  ▀█▓░██░▒██████▒▒░▓█▒░██▓ ▓█   ▓██▒░██████▒
░▒▓███▀▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░▓  ░
▒░▒   ░  ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░  ▒   ▒▒ ░░ ░ ▒  ░
 ░    ░  ▒ ░░  ░  ░   ░  ░░ ░  ░   ▒     ░ ░   
 ░       ░        ░   ░  ░  ░      ░  ░    ░  ░
      ░                                        
```
