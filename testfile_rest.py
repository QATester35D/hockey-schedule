### Here are some examples of the Get, Put, Post and Delete API calls

# import requests
# api_url = "https://jsonplaceholder.typicode.com/todos/1"
# response = requests.get(api_url)
# response.json()

#Adds a new photo reference
import requests
url = 'https://jsonplaceholder.typicode.com/photos/'
response = requests.get(url)
jsonPayload = {'albumId':1,'title':'test','url':'nothing.com','thumbnailUrl':'nothing.com'}
# response = requests.post(url,json=jsonPayload)
# print(response.json())
response = requests.get(url,params=jsonPayload)
print (response.url)
response = requests.get(url,)

# #We're modifying the photo ID 100 to the current information
# import requests
# url = 'https://jsonplaceholder.typicode.com/photos/100'
# response = requests.get(url)
# jsonPayload = {'albumId':1,'title':'test','url':'nothing.com','thumbnailUrl':'nothing.com','id':5001}
# response = requests.put(url,json=jsonPayload)
# print(response.json())

# import requests
# url = 'https://jsonplaceholder.typicode.com/photos/100'
# response = requests.get(url)
# jsonPayload = {'albumId':1,'title':'test','url':'nothing.com','thumbnailUrl':'nothing.com','id':100}
# response = requests.delete(url)
# print(response.json())