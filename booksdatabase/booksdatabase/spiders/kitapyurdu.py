import scrapy

class QuotesSpider(scrapy.Spider):
    name = "kitapyurdu"
    book_count = 1 
    start_urls = [
        "https://www.kitapyurdu.com/index.php?route=product/category&page=1&filter_category_all=true&path=1_41&filter_in_stock=1&filter_in_shelf=1&sort=purchased_365&order=DESC&limit=20"
    ]

    def parse(self, response):
        # Extract the book titles from the web page
        title = response.css("div.name.ellipsis a span::text").getall()
        
        # Extract the publishers from the web page
        publisher = response.css("div.publisher span a span::text").getall()
        
        # Extract the authors from the web page
        author = response.css("div.author span a span::text").getall()
        
        # Extract the old prices from the web page
        
        old_price = response.css("div.price div.price-old.price-passive span.value::text").getall()
        
        # Extract the new prices from the web page
        new_price = response.css("div.price div.price-new span.value::text").getall() 
        
        for x in range(len(title)):
            # Get the current new&old prices as a string, or an empty string if the index is out of range
            old_price_str = old_price[x] if x < len(old_price) else ""
            new_price_str = new_price[x] if x < len(new_price) else ""

            # Convert the new&old price to a float, removing commas and stripping whitespace, or set it to 0.0 if it's an empty string
            old_price_float = float(old_price_str.replace(',', '').strip()) if old_price_str else 0.0
            new_price_float = float(new_price_str.replace(',', '').strip()) if new_price_str else 0.0
            
            # Calculate the discount percentage if the old price is available, otherwise set it to 0
            discount = 0
            if old_price_str:
                discount = round(((old_price_float - new_price_float) / old_price_float) * 100, 1)

            yield {
                # Assign a list number to the book based on the book count
                "list_number": self.book_count,
                
                # Assign the current title, or an empty string if the index is out of range
                "title": title[x] if x < len(title) else "",
                
                # Assign the current publisher, or an empty string if the index is out of range
                "publisher": publisher[x] if x < len(publisher) else "",
                
                # Assign the current author, or an empty string if the index is out of range
                "author": author[x] if x < len(author) else "",
                
                # Assign the current old price, or an empty string if the index is out of range
                "old_price": old_price[x] if x < len(old_price) else "",
                
                # Assign the current new price, or an empty string if the index is out of range
                "new_price": new_price[x] if x < len(new_price) else "",
                
                # Assign the discount percentage if both the old and new prices are available, otherwise set it to 0.0
                "discount": discount if old_price_str and new_price_str else 0.0,
            }
            # Increment the book count for the next book
            self.book_count += 1
            
        # Extract the URL of the next page, if available
        next_url = response.css("a.next::attr(href)").get()
        
        # If a next page URL exists, send a new request to that URL and call the 'parse' method recursively
        if next_url is not None:
            yield scrapy.Request(response.urljoin(next_url), callback=self.parse)

