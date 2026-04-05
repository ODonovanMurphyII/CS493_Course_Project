import requests
import pathlib 
import datetime
import os
from urllib.robotparser import RobotFileParser

class Logger:
    def __init__(self):
        self.timestamp = datetime.now()
        self.urlsCrawled = []
        self.noLog = False
        try:
            self.logFile = open("log.txt", "w", encoding="utf-8")
        except Exception as e:
            print(f"Error creating log file: {e}")
            self.noLog = True
        
class Crawler:
    def __init__(self, userAgent):
        self.userAgent = userAgent
        self.RobotsParser = RobotFileParser()
        self.req = None
        self.halt = 5               # delay in seconds between requests
        self.outputFile = None
        self.outputFilename = None
        self.fileOutputAllowed = True
        try:
            self.outputDirectory = pathlib.Path(__file__).parent / "storedPages"
            self.outputDirectory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.fileOutputAllowed = False
            print(f"Error File Output Not Allowed. Check Permissions. {e}")

    def parse_robots_txt(self):
        print("Enter URL:", end="")
        URL = input()                       ## TODO maybe its useful to hang onto the URL
        print("Parsing File...")
        self.req = requests.get("https://www.cnn.com/robots.txt")           ## TODO hardcoded for now
        if (self.req.ok):
            self.RobotsParser.parse(self.req.text.splitlines())
        else:
            print("Failed to parse robots.txt" + str(self.req))

    def storePages(self, sentinel):
        currentNumberOfFiles = len(file for file in self.outputDirectory.iterdir() if file.is_file())
        currentNumberOfFiles += 1
        self.outputFilename = "site" + str(currentNumberOfFiles)
        if not sentinel: 
            print("No sentienl provided. Storing every allowable page to ~/storedPages")
        else:
            for site in self.RobotsParser.site_maps():
                self.reg = requests.get(site)
                if(self.req.ok):
                    pass

                
            
        
        
    
    


newsBot = Crawler('StudentCrawlerv1.0@CCSU.EDU')
newsBot.parse_robots_txt()

## Lets see all the sites we are allowed to crawl
siteMaps = newsBot.RobotsParser.site_maps()
for site in siteMaps:
    if newsBot.RobotsParser.can_fetch(newsBot.userAgent[1],site):
        print("We can crawl:" + site)
    else:
        print("Site not allowed:" + site)





    
    

