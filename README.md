# McCarthy

Search for CCP members by name and get English results.

---

## General Install

Make sure you have python3, pip, & sqlite installed on your system.

```bash
git clone https://github.com/BenWirus/Mccarthy.git
cd mccarthy
python3 -m pip install -r requirements.txt
```

Download the SQLite db from [here](https://gitlab.com/shanghai-ccp-member-db/shanghai-ccp-member-db/-/raw/master/shanghai-ccp-member.db) and copy it to the `mccarthy` project folder and name it `ccp.db`.

## Docker Install

```bash
docker run -ti debian /bin/bash
cd ~
apt update
apt install python3 python3-pip sqlite3 wget git
git clone https://github.com/BenWirus/Mccarthy.git
cd mccarthy
wget -O ccp.db https://gitlab.com/shanghai-ccp-member-db/shanghai-ccp-member-db/-/raw/master/shanghai-ccp-member.db
python3 -m pip install -r requirements.txt
```

## Usage

*nix:

```bash
./mccarthy.py -n <name>
./mccarthy.py --name <name>
```

win:

```bash
python3 mccarthy.py -n <name>
python3 mccarthy.py --name <name>
```

## Results

Translated JSON results will be dumped to stdout, and a timestamped JSON file will be created in the `out/` folder.

## Features

* Translates the results from Chinese to English
* Multiple result sets
    * Searches the name as a Chinese translated string
    * Searches the name as it was entered

## Needed Improvements

* Something other than SQLite to store the searchable data maybe Elasticsearch?
* Translation result caching.
* Search more than the name. E.G. address, phone, hometown, CCP ID Number, etc.
* Support other languages besides English.
