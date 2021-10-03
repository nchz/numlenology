"""
Module that exports the `languages` variable.

It's a list of named tuples with the following fields:
    code: The 2-letter language code as used in the `lang` argument of `num2words`.
    name: Language name.
    flag: URL of a country flag image that is related with the language.
"""
from collections import namedtuple


Language = namedtuple("Language", ["code", "name", "flag"])

FLAGS_BASE_URL = "https://www.worldometers.info/img/flags"
languages = [
    Language(code="ar", name="Arabic", flag=f"{FLAGS_BASE_URL}/sa-flag.gif"),
    Language(code="cz", name="Czech", flag=f"{FLAGS_BASE_URL}/ez-flag.gif"),
    Language(code="de", name="German", flag=f"{FLAGS_BASE_URL}/gm-flag.gif"),
    Language(code="dk", name="Danish", flag=f"{FLAGS_BASE_URL}/da-flag.gif"),
    Language(code="en", name="English", flag=f"{FLAGS_BASE_URL}/uk-flag.gif"),
    Language(code="es", name="Spanish", flag=f"{FLAGS_BASE_URL}/sp-flag.gif"),
    Language(code="fi", name="Finnish", flag=f"{FLAGS_BASE_URL}/fi-flag.gif"),
    Language(code="fr", name="French", flag=f"{FLAGS_BASE_URL}/fr-flag.gif"),
    Language(code="he", name="Hebrew", flag=f"{FLAGS_BASE_URL}/is-flag.gif"),
    Language(code="id", name="Indonesian", flag=f"{FLAGS_BASE_URL}/id-flag.gif"),
    Language(code="it", name="Italian", flag=f"{FLAGS_BASE_URL}/it-flag.gif"),
    Language(code="ja", name="Japanese", flag=f"{FLAGS_BASE_URL}/ja-flag.gif"),
    Language(code="kn", name="Kannada", flag=f"{FLAGS_BASE_URL}/in-flag.gif"),
    Language(code="ko", name="Korean", flag=f"{FLAGS_BASE_URL}/ks-flag.gif"),
    Language(code="lt", name="Lithuanian", flag=f"{FLAGS_BASE_URL}/lh-flag.gif"),
    Language(code="lv", name="Latvian", flag=f"{FLAGS_BASE_URL}/lg-flag.gif"),
    Language(code="nl", name="Dutch", flag=f"{FLAGS_BASE_URL}/nl-flag.gif"),
    Language(code="no", name="Norwegian", flag=f"{FLAGS_BASE_URL}/no-flag.gif"),
    Language(code="pl", name="Polish", flag=f"{FLAGS_BASE_URL}/pl-flag.gif"),
    Language(code="pt", name="Portuguese", flag=f"{FLAGS_BASE_URL}/po-flag.gif"),
    Language(code="ro", name="Romanian", flag=f"{FLAGS_BASE_URL}/ro-flag.gif"),
    Language(code="ru", name="Russian", flag=f"{FLAGS_BASE_URL}/rs-flag.gif"),
    Language(code="sl", name="Slovenian", flag=f"{FLAGS_BASE_URL}/si-flag.gif"),
    Language(code="sr", name="Serbian", flag=f"{FLAGS_BASE_URL}/ri-flag.gif"),
    Language(code="th", name="Thai", flag=f"{FLAGS_BASE_URL}/th-flag.gif"),
    Language(code="tr", name="Turkish", flag=f"{FLAGS_BASE_URL}/tu-flag.gif"),
    Language(code="uk", name="Ukrainian", flag=f"{FLAGS_BASE_URL}/up-flag.gif"),
    Language(code="vi", name="Vietnamese", flag=f"{FLAGS_BASE_URL}/vm-flag.gif"),
]
