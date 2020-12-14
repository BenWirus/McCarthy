#! /usr/bin/env python3

"""
Mccarthyism is back in style. Make these bitches rout.
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
    print(sys.argv[0] + ' -n <name>')
    print(sys.argv[0] + ' --name <name>')
    sys.exit(code)


def run(name):
    # Open the DB
    conn = sqlite3.connect('ccp.db')
    cursor = conn.cursor()
    # Translate the name to Chinese
    zh_name = do_translate_auto_zh(name)
    # The search query @todo implement FTS with ranks instead of ugly like search
    name_query = """SELECT *  FROM member WHERE member.name LIKE '%'||?||'%';"""
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
        'chinese_translated': [],
        'untranslated': []
    }

    # Search the DB for the translated chinese name
    print('Searching for name ' + zh_name + '(' + name + ')...')
    cursor.execute(name_query, [zh_name])
    zh_search_rows = cursor.fetchall()

    # Search the DB for the untranslated name
    print('Searching for name ' + name + '...')
    cursor.execute(name_query, [name])
    untrans_search_rows = cursor.fetchall()

    # Close the DB
    cursor.close()
    conn.close()

    print('Found %s Chinese translated search results' % str(len(zh_search_rows)))
    print('Found %s untranslated search results' % str(len(untrans_search_rows)))

    # Translate the results to english
    print('Translating results...')
    for row in zh_search_rows:
        try:
            results['chinese_translated'].append(
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

    # Translate the results to english
    for row in untrans_search_rows:
        try:
            results['untranslated'].append(
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

    # Run threads
    pool.close()
    pool.join()

    # Dump json to file
    with open('out/' + name + '-' + str(time.time() * 1000.0) + '.json', 'w') as outfile:
        json.dump(results, outfile)
    # Dump json to stdout
    print(json.dumps(results))


def main(argv):
    """
    Parses arguments from the commandline
    :param argv: list
    :return: void
    """
    name = False

    try:
        opts, args = getopt.getopt(argv, "h:n:", ["name="])
    except getopt.GetoptError:
        print_help(1)

    for opt, arg in opts:
        if opt == '-h':
            print_help()
        elif opt in ("-n", "--name"):
            name = arg

    if not name:
        print_help(1)

    run(name)


if __name__ == "__main__":
    main(sys.argv[1:])
