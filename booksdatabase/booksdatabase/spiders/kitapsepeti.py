import scrapy


class QuotesSpider(scrapy.Spider):
    name = "kitapsepeti"
    book_count = 1 
    start_urls = [
        "https://www.kitapsepeti.com/arastirma-inceleme-716?pg=1&stock=1"
    ]

    def parse(self, response):
        # Extract the book titles from the web page
        title = response.css("div.box.col-12.text-center a.fl.col-12.text-description.detailLink::text").getall()
        
        # Extract the publishers from the web page
        publisher = response.css("div.box.col-12.text-center a.col.col-12.text-title.mt::text").getall()
        
        # Extract the authors from the web page
        author = response.css("div.box.col-12.text-center a.fl.col-12.text-title::text").getall()
        
        # Extract the prices from the web page
        price = response.css("div.col.col-12.currentPrice::text").getall() 
        for x in range(len(title)):
            yield {
                # Assign a list number to the book based on the book count
                "list_number": self.book_count,
                
                # Assign the current title, or an empty string if the index is out of range
                "title": title[x].replace("\n","") if x < len(title) else "",
                
                # Assign the current publisher, or an empty string if the index is out of range
                "publisher": publisher[x] if x < len(publisher) else "",
                
                # Assign the current author, or an empty string if the index is out of range
                "author": author[x] if x < len(author) else "",
                
                # Assign the price, or an empty string if the index is out of range
                "price": price[x].replace("\n","") if x < len(price) else "",

            }
            # Increment the book count for the next book
            self.book_count += 1
            
            # Extract the URL of the next page, if available
        next_url = response.css("a.next::attr(href)").get()
        
        # If a next page URL exists, send a new request to that URL and call the 'parse' method recursively
        if next_url is not None:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)   