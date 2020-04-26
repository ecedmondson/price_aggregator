import requests
from time import sleep
from time import time

headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

start = time()
rs = []
counter = 0
while counter < 500:
    r = requests.get("https://www.amazon.com/HP-Chromebook-x360-14-FHD-Touch/dp/B08121BNBS", headers=headers)
    print(r)
    rs.append(r)
    counter += 1
    sleep(30)
end = time()

val = dict()
for r in rs:
    if r.status_code in val.keys():
        val[r.status_code] = val[r.status_code] + 1
    else:
        val[r.status_code] = 1

print(val)
print("30 sec intervals")
print(f"took {end - start} secs")
