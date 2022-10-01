from flask import Flask
import math
import re
import requests
from collections import Counter
from googlesearch import search
from flask import request
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route('/')
def index():
    query = request.args.get('data', default='*', type=str)
    print(query)
    find = hanap(query)
    print(find)
    out_data = []
    for data in find:
        if "0.txt" in data:
            out_data.append(data)
    return out_data


def hanap(query):
    results = set()
    # to search
    for j in search(query, tld="co.in", num=6, stop=6, pause=3):
        try:
            response = requests.get(j)
            print(response.status_code)
            html = (response.content)
            soup = BeautifulSoup(html, features="html.parser")
            name = j.replace(":", "@")
            name = name.replace("/", "AAAA")
            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out

            # get text
            text = ""
            for data in soup.find_all("p"):
                text += data.get_text()
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines
                      for phrase in line.split("  "))
            # drop blank lines
            text = ' '.join(chunk for chunk in chunks if chunk)
            q = re.sub('[^A-Za-z0-9\,\-\.\ ]+', ' ', query)
            t = re.sub('[^A-Za-z0-9\,\-\.\ ]+', ' ', text)
            vector1 = text_to_vector(q.lower())
            vector2 = text_to_vector(t.lower())
            common = longest_common_substring(q.lower(), t.lower())
            cosine = get_cosine(vector1, vector2)
            name = j.replace(":", "@")
            name = name.replace("/", "AAAA")
            score = "0.txt", name, cosine, common

            results.add(score)

        except:
            print("404")
    return results


WORD = re.compile(r"\w+")


def get_cosine(vec1, vec2):
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in list(vec1.keys())])
    sum2 = sum([vec2[x]**2 for x in list(vec2.keys())])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator


def text_to_vector(text):
    words = WORD.findall(text)
    return Counter(words)


def longest_common_substring(s1, s2):
    m = [[0] * (1 + len(s2)) for _ in range(1 + len(s1))]

    longest, x_longest = 0, 0

    for x in range(1, 1 + len(s1)):
        for y in range(1, 1 + len(s2)):
            if s1[x - 1] == s2[y - 1]:
                m[x][y] = m[x - 1][y - 1] + 1
                if m[x][y] > longest:
                    longest = m[x][y]
                    x_longest = x
            else:
                m[x][y] = 0

    return s1[x_longest - longest:x_longest]

