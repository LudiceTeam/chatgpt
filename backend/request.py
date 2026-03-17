import requests



{"access_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzEyMzQ1Njc4IiwiZXhwIjoxNzczNzQxMDY0LCJ0eXBlIjoiYWNjZXNzIn0._hwugysOUyNgRtk1XpG9BzovPk3xkz45l5y3JG78VOA",
 "refresh_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzEyMzQ1Njc4IiwiZXhwIjoxNzc4MDU5MjY0LCJ0eXBlIjoicmVmcmVzaCJ9.B5wh6S56HRxHxEfRg_tkf9GKpy7QfD93Me_x8CUy5r0",
 "token_type":"bearer"}


url = "http://127.0.0.1:1488/ask"

headers = {
    "Authorization":f"Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzEyMzQ1Njc4IiwiZXhwIjoxNzczNzQxMDY0LCJ0eXBlIjoiYWNjZXNzIn0._hwugysOUyNgRtk1XpG9BzovPk3xkz45l5y3JG78VOA"
}

data = {
    "request":"привет ты кто"
}

resp = requests.post(url,json = data,headers=headers)


print(resp.text)