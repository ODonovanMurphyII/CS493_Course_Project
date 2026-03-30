import requests

print("Please enter URL:", end="")
URL = input()
print("Please enter a keyword to look for")
keyword = input()
pagesToExplore = []
pagesToAvoid = []

# First stage
attempt = requests.get(URL)
if attempt.status_code == 200:
    rawData = attempt.content
    rawData = rawData.decode('utf-8')
    strings = rawData.splitlines()
    i = 0
    while i < len(strings):  #TODO need to make this section more robust
        if "sitemap" in strings[i]:
            strings[i] = strings[i].lstrip("Sitemap: ")
            pagesToExplore.append(strings[i])
        elif "Disallow" in strings[i]:
            pagesToAvoid.append(strings[i])
        i += 1
else:
    print("Error:" + attempt.status_code)

#eventual recursive call and possible DFS algorithm
#for now, just getting header and URL information
i = 0
while(i < len(pagesToExplore)):
    site = requests.get(pagesToExplore.pop())
    strings = site.content.decode('utf-8').splitlines()
    
    

