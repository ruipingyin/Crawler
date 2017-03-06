with open('./items.list', 'r') as fp:
    for line in fp: items.append(line.split())

print('items count: ' , len(items))

