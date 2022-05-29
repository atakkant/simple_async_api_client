from bs4 import BeautifulSoup

def parse_html(source,elements):
    soup = BeautifulSoup(source)
    items = []
    for el in elements:
        item = {}
        title = el.get('title')
        item[title] = soup.find(el.get('tag'),{el.get('attribute'):el.get('value')}).text.strip()
        items.append(item)
        print('{} is {}'.format(title,item[title]))
    
    return items

def parse_json(source):
    try:
        data = source.json()
        print(data.get('Name'))
    except Exception as e:
        print('source not converted to json')
        print(e)
        print(data)
    return data

def parser(response,elements=None):
    if isinstance(response,dict):
        return response
    else:
        return parse_html(response,elements)