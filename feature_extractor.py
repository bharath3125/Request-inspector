import re

def extract_features(text: str):
    return [
        len(text),
        text.count("'"),
        text.count('"'),
        text.count("<"),
        text.count(">"),
        text.lower().count("select"),
        text.lower().count("union"),
        text.lower().count("script"),
        len(re.findall(r"\d+", text)),
        int(bool(re.search(r"(=|--|;|%27|%3D)", text)))
    ]
