import lxml.html
import requests
import os.path

n = 1
for page in range(1, 10):
    r = requests.get('http://www.bensound.com/royalty-free-music/%s' % page)
    root = lxml.html.fromstring(r.content)
    for element in root.cssselect('.bloc_cat > div '):
        title = element.cssselect('.titre p')[0].text.strip()
        url = element.cssselect('#player')[0].get('src').strip()
        filename = '%03d. %s.mp3' % (n, title)
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        print(filename)
        n += 1
