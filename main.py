import requests

print("Please enter URL:", end="")
URL = input()
robotsLocaiton = URL + "/robots.txt"
pagesToExplore = []
pagesToAvoid = []

attempt = requests.get("http://www.cnn.com/robots.txt")
if attempt.status_code == 200:
    rawData = attempt.content
strings = rawData.splitlines()
while i < len(strings):
    if "sitemap" in strings[i]:
        pagesToExplore.append(strings[i])
    elif "Disallow" in strings[i]:
        pagesToAvoid.append(strings[i])
    i += 1


