import requests
from urllib.robotparser import RobotFileParser


class Crawler:
    def __init__(self, userAgent):
        self.userAgent = userAgent
        self.RobotsParser = RobotFileParser()
        self.req = None
        self.mSdelay = 1000 
        pass

    def parse_robots_txt(self):
        print("Enter URL:", end="")
        URL = input()                       ## TODO maybe its useful to hang onto the URL
        print("Parsing File...")
        self.req = requests.get("https://www.cnn.com/robots.txt")           ## TODO hardcoded for now
        if (self.req.ok):
            self.RobotsParser.parse(self.req.text.splitlines())
        else:
            print("Failed to parse robots.txt" + str(self.req))


newsBot = Crawler('StudentCrawlerv1.0@CCSU.EDU')
newsBot.parse_robots_txt()

## Lets see all the sites we are allowed to crawl
siteMaps = newsBot.RobotsParser.site_maps()
for site in siteMaps:
    if newsBot.RobotsParser.can_fetch(newsBot.userAgent[1],site):
        print("We can crawl:" + site)
    else:
        print("Site not allowed:" + site)



    
    

