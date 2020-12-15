# McCarthy

Search for CCP members by name and get English results.

---

## General Install

Make sure you have python3, pip, & sqlite installed on your system.

```bash
git clone https://github.com/BenWirus/McCarthy.git mccarthy
cd mccarthy
python3 -m pip install -r requirements.txt
```

Download the SQLite db
from [here](https://git.maga.host/BenWirus/ChiomDB/-/raw/master/ccp_zh.db) and
copy it to the `mccarthy` project folder and name it `ccp.db`.

## Docker Install

```bash
docker run -ti debian /bin/bash
cd ~
apt update
apt install python3 python3-pip sqlite3 wget git
git clone https://github.com/BenWirus/McCarthy.git mccarthy
cd mccarthy
wget -O ccp.db https://git.maga.host/BenWirus/ChiomDB/-/raw/master/ccp_zh.db
python3 -m pip install -r requirements.txt
```

## Usage

*nix:

```bash
./mccarthy.py -n <name> -h <home> -o <organization> -a <address> -m <mobile_phone_number> -p <phone_number>
./mccarthy.py --name <name> --home <home> --org <organization> --address <address> --mobile <mobile_phone_number> --phone <phone_number>
```

win:

```bash
python3 mccarthy.py -n <name> -h <home> -o <organization> -a <address> -m <mobile_phone_number> -p <phone_number>
python3 mccarthy.py --name <name> --home <home> --org <organization> --address <address> --mobile <mobile_phone_number> --phone <phone_number>
```

## Results

Translated JSON results will be dumped to stdout, and a timestamped JSON file will be created in the `out/` folder.

## Features

* Translates the results from Chinese to English
* Multiple result sets
    * Searches the name as a Chinese translated string
    * Searches the name as it was entered
* Search:
    * Name
    * Hometown
    * Organization
    * Address
    * Mobile Number
    * Phone Number

## Needed Improvements

* Something other than SQLite to store the searchable data maybe Elasticsearch?
* Translation result caching.
* Support other languages besides English.
