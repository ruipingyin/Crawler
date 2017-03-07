import gzip

# read item list
path = './reviews_Clothing_Shoes_and_Jewelry_5.json.gz'

items = {}

with gzip.open(path, 'r') as g:
    for l in g:
        items[eval(l)['asin']] = ''
        
print('items count: ' , len(items))

# read item url
path = './meta_Clothing_Shoes_and_Jewelry.json.gz'

with gzip.open(path, 'r') as g:
    for l in g:
        if eval(l)['asin'] in items:
            items[eval(l)['asin']] = eval(l)['imUrl']

# save map to file
with open('./items.list', 'w') as f:
    for key, value in items.items():
        if len(value) == 0:
            print('Empty of item: ', key)
        f.write('%s\t%s\n' % (key, value))