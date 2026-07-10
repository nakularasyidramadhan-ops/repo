```
apt update && apt upgrade -y
```
```
git clone https://github.com/nakularasyidramadhan-ops/repo
```
```
cd ubotnexxanew
```
```
python3 -m venv venv
```
```
source venv/bin/activate
```
```
apt install nodejs -y
```
```
apt install nsolid -y
```
```
pip install -r requirements.txt
```
```
cp sample.env .env && nano .env
```
```
pip install speedtest-cli
```
```
python3 -m PyroUbot
```

---------- Menghidupan jika ubot mati -------------

```
cd ubotnexxanew && screen -S ubotnexxanew
```
```
python3 -m venv venv && source venv/bin/activate
```
```
screen -S ubotnexxanew
```
```
python3 -m PyroUbot
```
