import lxml.html
import requests
import codecs

mapping = [ (' [NCS Release]', ''), ('–', '-'), ('’', '') ]
cookie = {'wordpress_logged_in_...': '...'} # copy this cookie from your browser

n = 1
for page in range(1, 20):
    r = requests.get('http://nocopyrightsounds.co.uk/playlist/page/%s/?orderby=popular' % page)
    root = lxml.html.fromstring(r.content)
    for element in root.cssselect('.list-item-list li .post .info a:not([rel~=category])'):
        name = element.text
        for k, v in mapping:
            name = name.replace(k, v)
        url = element.get('href')
        filename = '%03d. %s.mp3' % (n, name)
        dl = lxml.html.fromstring(requests.get('%s?download=1' % url, cookies=cookie).content).cssselect('.download_5sec a')[0].get('href')
        r = requests.get(dl, stream=True)
        if r.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in r:
                    f.write(chunk)
        print(filename)
        n += 1
