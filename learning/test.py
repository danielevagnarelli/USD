import requests
response = requests.get('https://ghibliapi.herokuapp.com/films/')

if response.status_code == 200:
    print("Succesful connection with API.")
    print('-------------------------------')
    data = response.json()
    print(data)
elif response.status_code == 404:
    print("Unable to reach URL.")
else:
    print("Unable to connect API or retrieve data.")