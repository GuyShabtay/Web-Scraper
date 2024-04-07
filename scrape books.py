import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

def scrape_page(page_number):
    print("Currently scraping page:", page_number)

    url = "https://books.toscrape.com/catalogue/page-" + str(page_number) + ".html"
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")

    if soup.title.text == "404 Not Found":
        return None

    data = []
    all_books = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for book in all_books:
        item = {}
        item['Title'] = book.find("img").attrs["alt"]
        item['Link'] = "https://books.toscrape.com/catalogue/" + book.find("a").attrs["href"]
        item['Price'] = float(book.find("p", class_="price_color").text[2:])  # Convert price to float

        item['Stock'] = book.find("p", class_="instock availability").text.strip()

        def convert_rating_to_number(rating_text):
            ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
            return ratings.get(rating_text.capitalize(), None)

        # Extracting rating
        rating_tag = book.find("p", class_="star-rating")
        if rating_tag:
            rating_classes = rating_tag.get("class")
            if rating_classes:
                rating = rating_classes[-1]  # Last class in the list is the rating
                numeric_rating = convert_rating_to_number(rating)

                item['Rating'] = f'{numeric_rating} stars'
            else:
                item['Rating'] = "Unknown"
        else:
            item['Rating'] = "Unknown"

        data.append(item)

    return data

def main():
    max_pages = 50  # Set the maximum number of pages to scrape

    data = []
    with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
        future_to_page = {executor.submit(scrape_page, page_number): page_number for page_number in range(1, max_pages + 1)}

        for future in as_completed(future_to_page):
            page_number = future_to_page[future]
            page_data = future.result()
            if page_data:
                data.extend(page_data)

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Save scraped data to CSV and Excel files
    csv_file_path = "books.csv"
    df.to_csv(csv_file_path, index=False)

    # Data visualization
    # Histogram of book prices
    plt.figure(figsize=(10, 6))
    plt.hist(df['Price'], bins=20, color='skyblue', edgecolor='black')
    plt.title('Distribution of Book Prices')
    plt.xlabel('Price ($)')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.savefig("price_histogram.png")
    plt.show()

    print(f"Scraped data saved to: {csv_file_path}")

if __name__ == "__main__":
    main()


