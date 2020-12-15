#! /usr/bin/env python3

"""
McCarthyism is back in style. Make these bitches rout.
"""

import sys
import getopt
from google_trans_new import google_translator
import sqlite3
from multiprocessing.dummy import Pool as ThreadPool
import json
import time

pool = ThreadPool(10)  # Threads


def do_translate_zh_en(text):
    """
    translates a string from Chinese to English
    :param text: str
    :return: str
    """
    t = google_translator(timeout=5)
    if isinstance(text, int):
        return text  # don't translate the IDs
    if isinstance(text, str):
        text = text.strip()  # Strip trailing crap
    return t.translate(text, lang_tgt='en', lang_src='zh').strip() if text and text != 'null' else ''


def do_translate_auto_zh(text):
    """
    translates a string to Chinese
    :param text: str
    :return: str
    """
    t = google_translator(timeout=5)
    text = text.strip()  # Strip trailing crap
    return t.translate(text, lang_tgt='zh', lang_src='auto').strip()


def print_help(code: int = 0):
    """
    Prints help to stdout and exits with the code supplied
    :param code: int
    :return: void
    """
    print(
        sys.argv[0] + ' -n <name> -h <home> -o <organization> -a <address> -m <mobile_phone_number> -p <phone_number>'
    )
    print(
        sys.argv[0] +
        ' --name <name> --home <home> --org <organization> --address <address> --mobile <mobile_phone_number> --phone <phone_number>'
    )
    sys.exit(code)


def run_translations(rows):
    results = []

    for row in rows:
        try:
            results.append(
                pool.map(do_translate_zh_en, [
                    row[0],
                    row[1],
                    row[2],
                    row[3],
                    row[4],
                    row[5],
                    row[6],
                    row[7],
                    row[8],
                    row[9],
                    row[10]
                ]))
        except Exception as e:
            raise e

    return results


def search_db(term, zh_term, type):
    # Open the DB
    conn = sqlite3.connect('ccp.db')
    cursor = conn.cursor()
    # The search query @todo implement FTS with ranks instead of ugly like search
    query = "SELECT *  FROM member WHERE member." + type + " LIKE '%'||?||'%';"

    if term != zh_term:
        # Search the DB for the translated chinese name
        print('Searching for ' + type + ' ' + zh_term + '(' + term + ')...')
        cursor.execute(query, [zh_term])
        zh_search_rows = cursor.fetchall()
    else:
        print(
            'Skipping translated search. The translated term is the same as the original term. (%s - %s)'
            % (term, zh_term)
        )
        zh_search_rows = []

    # Search the DB for the untranslated name
    print('Searching for ' + type + ' ' + term + '...')
    cursor.execute(query, [term])
    untrans_search_rows = cursor.fetchall()

    # Close the DB
    cursor.close()
    conn.close()

    print('Found %s Chinese translated %s results' % (str(len(zh_search_rows)), type))
    print('Found %s untranslated %s results' % (str(len(untrans_search_rows)), type))
    print('Translating results...')
    return [run_translations(zh_search_rows), run_translations(untrans_search_rows)]


def run(name, home, org, addr, mobile, phone):
    # Results
    results = {
        'keys': [
            'id',
            'name',
            'sex',
            'ethnicity',
            'hometown',
            'organization',
            'id_card_num',
            'address',
            'mobile_num',
            'phone_num',
            'education'
        ],
        'chinese_translated': {},
        'untranslated': {}
    }

    ###
    # Initial translations to search as Chinese
    ###
    # Translate the name to Chinese
    zh_name = do_translate_auto_zh(name) if name else False
    # Translate the home to Chinese
    zh_home = do_translate_auto_zh(home) if home else False
    # Translate the org to Chinese
    zh_org = do_translate_auto_zh(org) if org else False
    # Translate the address to Chinese
    zh_addr = do_translate_auto_zh(addr) if addr else False
    # Translate the mobile to Chinese
    zh_mobile = do_translate_auto_zh(mobile) if mobile else False
    # Translate the phone to Chinese
    zh_phone = do_translate_auto_zh(phone) if phone else False

    if name:
        r = search_db(name, zh_name, 'name')
        results['chinese_translated']['name'] = r[0]
        results['untranslated']['name'] = r[1]

    if home:
        r = search_db(home, zh_home, 'hometown')
        results['chinese_translated']['hometown'] = r[0]
        results['untranslated']['hometown'] = r[1]

    if org:
        r = search_db(org, zh_org, 'organization')
        results['chinese_translated']['organization'] = r[0]
        results['untranslated']['organization'] = r[1]

    if addr:
        r = search_db(addr, zh_addr, 'address')
        results['chinese_translated']['address'] = r[0]
        results['untranslated']['address'] = r[1]

    if mobile:
        r = search_db(mobile, zh_mobile, 'mobile_num')
        results['chinese_translated']['mobile_num'] = r[0]
        results['untranslated']['mobile_num'] = r[1]

    if phone:
        r = search_db(phone, zh_phone, 'phone_num')
        results['chinese_translated']['phone_num'] = r[0]
        results['untranslated']['phone_num'] = r[1]

    # Run threads
    pool.close()
    pool.join()

    # Dump json to file
    with open('out/' + str(time.time() * 1000.0) + '.json', 'w') as outfile:
        json.dump(results, outfile)
    # Dump json to stdout
    print(json.dumps(results))


def main(argv):
    name = False
    home = False
    org = False
    addr = False
    mobile = False
    phone = False

    try:
        opts, args = getopt.getopt(argv, "Hn:h:o:a:m:p:", [
            "help",
            "name=",
            "home=",
            "org=",
            "address=",
            "mobile=",
            "phone="
        ])
    except getopt.GetoptError:
        print_help(1)

    for opt, arg in opts:
        if opt in ('-H', '--help'):
            print_help()
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-H", "--home"):
            home = arg
        elif opt in ("-o", "--org"):
            org = arg
        elif opt in ("-a", "--address"):
            addr = arg
        elif opt in ("-m", "--mobile"):
            mobile = arg
        elif opt in ("-p", "--phone"):
            phone = arg

    if name or home or org or addr or mobile or phone:
        run(name, home, org, addr, mobile, phone)
    else:
        print_help(1)


if __name__ == "__main__":
    main(sys.argv[1:])
