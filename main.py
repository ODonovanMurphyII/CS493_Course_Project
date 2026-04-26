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
        self.haltTime = 5               # delay in seconds between requests
        self.outputFile = None
        self.outputFilename = None
        self.outputFiles = []
        self.fileOutputAllowed = True
        self.sentinal = None
        self.downloadedPages = 0
        try:
            self.outputDirectory = pathlib.Path(__file__).parent / "allowedSitemaps"
            self.outputDirectory.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            self.fileOutputAllowed = False
            print(f"Error File Output Not Allowed. Check Permissions. {e}")

    def parse_robots_txt(self):
        print("Please enter full path to target robots.txt file:", end="")
        URL = input()                       ## TODO maybe its useful to hang onto the URL
        print("Attempting to Parse Robots.txt...")
        if(re.search("/robots.txt", URL, re.IGNORECASE)):
            self.req = requests.get(URL)          
            if (self.req.ok):
                if("crawl_delay" in self.req.text):
                    pass #TODO implement some code to pull the crawl delay from robots.txt otherwise defaults to 5 seconds
                self.RobotsParser.parse(self.req.text.splitlines())
                self.sentinal = input("Add a search topic or just press enter to download all sitemaps:")
            else:
                print("Failed to parse robots.txt" + str(self.req))
        else:
            print("Invalid robots.txt path. Try again")
            sys.exit()


    def storeSitemaps(self, sentinel):
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
            self.outputDirectory = pathlib.Path(__file__).parent /  "_pages" / self.sentinal
            self.outputDirectory.mkdir(parents=True, exist_ok=True)
            for site in sites:
                print("Working on " + site)
                self.req = requests.get(site)
                if(self.req.ok):
                    needle = rf"\b{self.sentinal}\b"
                    if(re.search(needle,self.req.content.decode('utf-8')) or re.search(needle,site)):
                        currentNumberOfFiles += 1
                        self.outputFilename = self.sentinal + "_" + str(currentNumberOfFiles) + ".xml"
                        self.outputFiles.append(self.outputFilename)
                        self.outputFile = open(self.outputDirectory / self.outputFilename, "w", encoding="utf-8")
                        self.outputFile.write(self.req.content.decode('utf-8'))
                        self.outputFile.close()
                time.sleep(self.haltTime)
        
    
    def downloadPages(self, sitemapFileName, sentinal):
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
                    time.sleep(5)
                    if(self.req.ok):
                        self.outputFilename = sentinal + "_page" + str(currentNumberOfPages) + ".html"
                        self.outputFile = open(self.outputDirectory / self.outputFilename, "w", encoding="utf-8")
                        self.outputFile.write(self.req.content.decode('utf-8'))
                        self.outputFile.close()
                        currentNumberOfPages += 1
            self.downloadedPages += currentNumberOfPages

        


                    

                
            
        
        
    
crawler = Crawler('*')
crawler.parse_robots_txt()
crawler.storeSitemaps(crawler.sentinal)
for file in crawler.outputFiles:
    crawler.downloadPages(file, crawler.sentinal)
if(crawler.downloadedPages != 0):
    crawler.downloadedPages -= 1        ## Hacky but good enough for now
print(str(crawler.downloadedPages) + " pages found related to " + crawler.sentinal)







    
    

