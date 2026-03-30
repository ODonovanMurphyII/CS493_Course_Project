import requests
from urllib.robotparser import RobotFileParser

headerInfo = {
    'User Agent': 'StudentCrawlerv1.0'
}
print("https://", end="")
URL = input()
pagesToExplore = []
pagesToAvoid = []

# First stage
attempt = requests.get("https://" + URL + "/robots.txt")
if attempt.status_code == 200:
    rawData = attempt.content
    rawData = rawData.decode('utf-8')
    strings = rawData.splitlines()
    i = 0
    currentString = rawData[i]
    while(currentString != "User-agent: *"):
        i += 1
        currentString = strings[i]
    print(currentString)

else:
    print("Error:" + str(attempt.status_code))

#eventual recursive call and possible DFS algorithm
#for now, just getting header and URL information
i = 0
while(i < len(pagesToExplore)):
    site = requests.get(pagesToExplore.pop())
    strings = site.content.decode('utf-8').splitlines()
    
    

