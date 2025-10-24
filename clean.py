with open('dbcreate.json', 'rb') as f:
    data = f.read()

clean_data = data.decode('latin-1').encode('utf-8')

with open('dbcreate_utf8.json', 'wb') as f:
    f.write(clean_data)
