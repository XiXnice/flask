import requests

response = requests.post('http://127.0.0.1:5000/adv',
                         json={'title': 'title_1', 'description': 'Первое объявление', 'owner': 'Петя'},
                         headers={'Authorization': 'some_token'})

# response = requests.get('http://127.0.0.1:5000/adv/1')

# response = requests.delete('http://127.0.0.1:5000/adv/1', )

# response = requests.get('http://127.0.0.1:5000/adv/1', )

print(response.status_code)
print(response.text)
