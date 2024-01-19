from typing import List
import re, itertools, sys
import pandas as pd, numbers
from lxml import etree
import re
import random

all_chars = (chr(i) for i in range(sys.maxunicode))
control_chars = "".join(map(chr, itertools.chain(range(0x00, 0x20), range(0x7F, 0xA0))))
control_char_re = re.compile("[%s]" % re.escape(control_chars))


def remove_bin_chars(s: str) -> str:
    return control_char_re.sub("", s)


def get_sql_ready_str(pk_entities: List[int] | pd.Series) -> str:
    return "(" + ",".join([str(e) if isinstance(e, numbers.Number) else f"'{e}'" for e in pk_entities]) + ")"


def extract_str_from_xml(xml_text: str) -> str:
    parser = etree.XMLParser(recover=True)
    tree = etree.fromstring(xml_text, parser=parser)
    notags = etree.tostring(tree, encoding="utf8", method="text").decode("utf-8")
    return notags


def remove_tags(text: str) -> str:
    regex = re.compile("<.*?>")
    cleantext = re.sub(regex, "", text)
    return cleantext


def clean_text(text: str) -> str:
    text_ = text.strip()
    text_ = remove_bin_chars(text_)

    try:
        return extract_str_from_xml(text_)
    except:
        return remove_tags(text_).strip()


def clean_text_pgsql(text: str) -> str:
    text_ = text.strip()
    text_ = text_.replace("'", "''")
    text_ = text_.replace(":", "\:")

    return text_


def get_random_color():
    r = hex(random.randrange(0, 255))[2:].zfill(2)
    g = hex(random.randrange(0, 255))[2:].zfill(2)
    b = hex(random.randrange(0, 255))[2:].zfill(2)
    return '#'  + r + g + b


def compact_string(string, line_size=5):
    splitted = string.split(' ')
    new_splitted = []
    current_line = []
    for word in splitted:
        current_line.append(word)

        if len(current_line) >= line_size: 
            new_splitted.append(' '.join(current_line))
            current_line = []
        
    new_splitted.append(' '.join(current_line))

    return '\n'.join(new_splitted)
