# QRGenerator-Bot
Simple bot for generation QRCodes based on input data. Uses Redis for contains data about user qrcode color, therefore requires connection with **Redis-server** for normal functioning

# Installing
```bash
git clone https://github.com/resources3312/QRGenerator-Bot.git
cd QRGenerator-Bot
echo 'TOKEN="<your_bot_token>"\nREDIS_HOST="<redis-server-addr>"\nREDIS_PORT="<redis-server-port>"' > .env
pip install -r requirements.txt
python QRGenerator.py
```
