import pymongo
import json
import subprocess
import os
import time
import schedule

def scrape_update():
    # Run Scrapy crawl command for 'kitapsepeti' spider and save the output to 'kitapsepeti.json' file
    subprocess.run(['scrapy', 'crawl', 'kitapsepeti','-o','kitapsepeti.json'],cwd='booksdatabase')

    # Delay for 10 seconds
    time.sleep(10)

    # Run Scrapy crawl command for 'kitapyurdu' spider and save the output to 'kitapyurdu.json' file
    subprocess.run(['scrapy', 'crawl', 'kitapyurdu','-o','kitapyurdu.json'],cwd='booksdatabase')
    
    # Connect to MongoDB database
    client = pymongo.MongoClient("mongodb://localhost:27017/")

    # Select the 'smartmaple' database
    database = client["smartmaple"]

    # Select the 'kitapyurdu' and 'kitapsepeti' collections
    collection1 = database["kitapyurdu"]
    collection2 = database["kitapsepeti"]

    # Changing working direction for files
    os.chdir('booksdatabase')
    
    # Load data from 'kitapyurdu.json' file
    with open('kitapyurdu.json',encoding="utf-8") as file:
        data = json.load(file)
    
    # Delete existing documents in 'kitapyurdu' collection
    collection1.delete_many({})
    
    # Insert new data into 'kitapyurdu' collection    
    for books in data:
        collection1.insert_one(books)
        
    # Load data from 'kitapsepeti.json' file
    with open('kitapsepeti.json',encoding="utf-8") as file:
        data2 = json.load(file)
    
    # Delete existing documents in 'kitapsepeti' collection
    collection2.delete_many({})
    
    # Insert new data into 'kitapsepeti' collection    
    for books in data2:
        collection2.insert_one(books)    
        
    # Remove the temporary JSON files
    os.remove("kitapsepeti.json")
    os.remove("kitapyurdu.json")

# Schedule the 'scrape_update' function to run every day at midnight    
schedule.every().day.at("02:16").do(scrape_update)

# Continuous loop to check for scheduled tasks and execute them
while True:
    schedule.run_pending()
    time.sleep(1)   
    
    
            




