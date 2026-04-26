import requests
import pathlib 
import datetime
import os
import time
import re
import sys
from urllib.robotparser import RobotFileParser

class Logger:
    def __init__(self):
        self.timestamp = datetime.date.today()
        self.urlsCrawled = []
        self.noLog = False
        try:
            self.logFile = open("log.txt", "w", encoding="utf-8")
            self.logFile.write("Session Init:" + str(self.timestamp) + "\n")
        except Exception as e:
            print(f"Error creating log file: {e}" + "\n")
            self.noLog = True

    def log_entry(self, entry):
        self.timestamp = str(datetime.date.today())
        try:
            self.logFile.write(self.timestamp + " ")
            self.logFile.write(entry + '\n')
        except Exception as e:
            print("Logger Failed")
            self.logFile.write(self.timestamp)
            self.logFile.write(e)
            self.logFile.write("\n")
        
class Crawler:
    def __init__(self, userAgent):
        self.userAgent = userAgent
        self.RobotsParser = RobotFileParser()
        self.req = None
        self.haltTime = 5               # delay in seconds between requests
        self.outputFile = None
        self.outputFilename = None
        self.outputFiles = []
        self.fileOutputAllowed = True
        self.sentinel = None
        self.downloadedPages = 0
        try:
            self.outputDirectory = pathlib.Path(__file__).parent / "allowedSitemaps"
            self.outputDirectory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.fileOutputAllowed = False
            print(f"Error File Output Not Allowed. Check Permissions. {e}")

    def parse_robots_txt(self, logger: Logger):
        print("Please enter full path to target robots.txt file:", end="")
        URL = input()                       ## TODO maybe its useful to hang onto the URL
        print("Attempting to Parse Robots.txt...")
        if(re.search("/robots.txt", URL, re.IGNORECASE)):
            self.req = requests.get(URL)          
            if (self.req.ok):
                if("crawl_delay" in self.req.text):
                    pass #TODO implement some code to pull the crawl delay from robots.txt otherwise defaults to 5 seconds
                self.RobotsParser.parse(self.req.text.splitlines())
                self.sentinel = input("Add a search topic or just press enter to download all sitemaps:")
                logger.log_entry("Parsed Robots.txt!")
            else:
                print("Failed to parse robots.txt" + str(self.req))
                logger.log_entry("Failed to parse robots.txt")
        else:
            print("Invalid robots.txt path. Try again")
            sys.exit()


    def storeSitemaps(self, sentinel, logger: Logger):
        all = False
        locsToTryAgain = []
        currentNumberOfFiles = len([file for file in self.outputDirectory.iterdir() if file.is_file()])
        currentNumberOfFiles += 1
        self.outputFilename = "site" + str(currentNumberOfFiles) + ".xml"
        sites = self.RobotsParser.site_maps()
        if not sentinel: 
            print("No sentienl provided. Storing every allowable page to ~/allowedSitemaps")
            all = True
        if all:
            for site in sites:
                print("Working on " + site)
                logger.log_entry("Parsing sitemap:" + site)
                self.req = requests.get(site)
                if(self.req.ok):
                    self.outputFile = open(self.outputDirectory / self.outputFilename, "w", encoding="utf-8")
                    self.outputFile.write(self.req.content.decode('utf-8'))
                    self.outputFile.close()
                else:
                    locsToTryAgain.append(self.req)
                time.sleep(self.haltTime)
                currentNumberOfFiles += 1
                self.outputFilename = "site" + str(currentNumberOfFiles)
        else:
            currentNumberOfFiles = 0
            self.outputDirectory = pathlib.Path(__file__).parent /  "_pages" / self.sentinel
            self.outputDirectory.mkdir(parents=True, exist_ok=True)
            for site in sites:
                print("Working on " + site)
                self.req = requests.get(site)
                if(self.req.ok):
                    needle = rf"\b{self.sentinel}\b"
                    if(re.search(needle,self.req.content.decode('utf-8')) or re.search(needle,site)):
                        logger.log_entry(f"Found {needle} in {site} adding to xml stash")
                        currentNumberOfFiles += 1
                        self.outputFilename = self.sentinel + "_" + str(currentNumberOfFiles) + ".xml"
                        self.outputFiles.append(self.outputFilename)
                        self.outputFile = open(self.outputDirectory / self.outputFilename, "w", encoding="utf-8")
                        self.outputFile.write(self.req.content.decode('utf-8'))
                        self.outputFile.close()
                time.sleep(self.haltTime)
        
    
    def downloadPages(self, sitemapFileName, sentinal, logger: Logger):
            self.outputDirectory = pathlib.Path(__file__).parent /  "_pages" / sentinal
            sitemap = open(self.outputDirectory / sitemapFileName, "r", encoding="utf-8")
            targetPages = []
            cleanUrls = []
            data = sitemap.read()
            URLEntries = re.findall(r'<url>(.*?)</url>', data, re.DOTALL)
            for entry in URLEntries:
                if sentinal in entry:
                    targetPages.append(entry)
            targetPages = "".join(targetPages)
            cleanUrls = re.findall(r'<loc>(.*?)</loc>', targetPages, re.DOTALL)
            currentNumberOfPages = 0
            for cleanUrl in cleanUrls:
                if(self.RobotsParser.can_fetch(self.userAgent,cleanUrl)):
                    self.req = requests.get(cleanUrl)
                    time.sleep(self.haltTime)
                    if(self.req.ok):
                        logger.log_entry(f"Good REQ. Saving page {cleanUrl}")
                        self.outputFilename = sentinal + "_page" + str(currentNumberOfPages) + ".html"
                        self.outputFile = open(self.outputDirectory / self.outputFilename, "w", encoding="utf-8")
                        self.outputFile.write(self.req.content.decode('utf-8'))
                        self.outputFile.close()
                        currentNumberOfPages += 1
            self.downloadedPages += currentNumberOfPages

        


                    

                
            
        
        
logger = Logger()
crawler = Crawler('*')
crawler.parse_robots_txt(logger)
crawler.storeSitemaps(crawler.sentinel, logger)
for file in crawler.outputFiles:
    crawler.downloadPages(file, crawler.sentinel, logger)
if(crawler.downloadedPages != 0):
    crawler.downloadedPages -= 1        ## Hacky but good enough for now
print(str(crawler.downloadedPages) + " pages found related to " + crawler.sentinel)
logger.logFile.close()







    
    

