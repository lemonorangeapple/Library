import requests
from lxml import etree
from flask import *

def find(title):
    result = []
    for j in range(1, 10):
        try:
            page = requests.get("http://libgen.top/index.php?req=" + str(title) + "&page=" + j).text
        except:
            page = requests.get("http://libgen.top/index.php?req=" + str(title)).text
        tree = etree.HTML(page)
        title = tree.xpath('//*[@id="tablelibgen"]/tbody/tr/td/b/text()')
        dl = tree.xpath('//*[@id="tablelibgen"]/tbody/tr/td/nobr/a[1]/@href')
        ext = tree.xpath('//*[@id="tablelibgen"]/tbody/tr/td[8]/text()')
        for i in range(min(len(dl), len(title), len(ext))):
            dl[i] = dl[i].replace('http://', 'https://')
            dl[i] = dl[i].replace('https://libgen.rocks/ads', '')
            dl[i] = dl[i].replace('https://libgen.me/book/', '')
            dl[i] = dl[i].replace('https://library.lol/main/', '')
            dl[i] = dl[i][0:32]
            if dl[i][0] != '/' and ({'title': title[i], 'dl': 'https://library.lol/main/' + dl[i], 'ext': ext[i]} not in result):
                result.append({'title': title[i], 'dl': 'https://library.lol/main/' + dl[i], 'ext': ext[i]})
    return result

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        return render_template('search.html', result = find(request.values.get('q')), q = request.values.get('q'))

app.run()