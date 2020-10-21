from requests import put, get, post

with open('TJMS_FILE.xml', 'rb') as f:
    r = post('http://127.0.0.1:5000/xml', data={'xmlTribunal': f.read()})
    print(r.text)
