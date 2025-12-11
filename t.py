
import requests

url = "https://www.youtube.com/watch?v=LUJDHPCEdSc"

res = requests.get(url)

for r in res:
    print(r)