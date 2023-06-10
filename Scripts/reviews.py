# callable module Reviews
from requests_html import HTMLSession
import json
import time

class Reviews:
    def __init__(self, asin) -> None:
        self.session = HTMLSession()        # session object that is used continuously whenever this class instance is called
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}
        self.asin = asin
        self.url = f'https://www.amazon.co.uk/product-reviews/{self.asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber='


    def pagination(self, page):
        response = self.session.get(self.url + str(page), headers=self.headers)     # getting the new page URLs
        # check if there are reviews in the new url o not, using CSS selectors
        if not response.html.find('div[data-hook=review]'):
            return False
        else:
            return response.html.find('div[data-hook=review]')
    

    def parse(self, reviews):
        total = []
        # looping on reviews to parse the data i will extract and put in a .json file later on
        for review in reviews:
            # .find() outputs a list, so with first=True i say that i want the first element of that list
            # .text to convert into text (string)
            try:
                title = review.find('a[data-hook=review-title] span', first=True).text
                rating = review.find('i[data-hook=review-star-rating] span', first=True).text   
                # span means i'm selecting the span value of the element i[data-hook=review-star-rating] -> basically here i'm getting the number of stars of the review
                place_date = review.find('span[data-hook="review-date"]', first=True).text
                content = review.find('span[data-hook=review-body] span', first=True).text.replace('\n', '.').strip()
                # .replace('\n') and .strip() to eliminate backslashes and clean the text
            except:
                continue        # for sure will end up with some missing pages or data to be cleaned

            data = {'title': title,
                    'rating': rating,
                    'place and date': place_date,
                    'body': content[:2000]}      # crop excessively long reviews
            total.append(data)
        return total
    

    def save(self, results):
        # opening a new file named 'ASIN_ID_reviews.json', in which i will write ('w') all the results
        # assigning the new .json file to a new variable called f
        with open(self.asin + '_reviews.json', 'w') as f:
            json.dump(results, f)
