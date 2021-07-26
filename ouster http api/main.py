import requests

URL = 'http://169.254.53.146/'
response = requests.get(URL)
# print(response.status_code)
print(response.text)


# if __name__ == "__main__":
#     main()