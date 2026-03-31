import requests
from urllib.robotparser import RobotFileParser

headerInfo = {
    'User Agent': 'StudentCrawlerv1.0@CCSU.EDU'
}

robot = RobotFileParser()
print("Enter url")
URL = input()
req = requests.get(URL)
robot.parse(req.text.splitlines())
sitemaps = robot.site_maps()
for sitemap in sitemaps:
    print(sitemap)


    
    

