import requests

print("Please enter URL:", end="")
URL = input()
pagesToExplore = []
pagesToAvoid = []

attempt = requests.get(URL)
if attempt.status_code == 200:
    rawData = attempt.content
    rawData = rawData.decode('utf-8')
    strings = rawData.splitlines()
    i = 0
    while i < len(strings):
        if "sitemap" in strings[i]:
            pagesToExplore.append(strings[i])
        elif "Disallow" in strings[i]:
            pagesToAvoid.append(strings[i])
        i += 1
else:
    print("Error:" + attempt.status_code)


