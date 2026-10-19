# Bookstore Intelligence — Assignment 2

This project collects book titles, prices, ratings, stock availability and product links from [Books to Scrape](https://books.toscrape.com/). It cleans the data, answers the assignment questions and chooses a basket of books that maximizes total stars within £100.

## Run

```bash
pip install -r requirements.txt
python bookstore_scraper.py
```

The script scrapes five pages by default (100 books). Change `PAGES = 5` to `PAGES = 50` for the full catalogue. The results are created automatically in this folder: `competitor_books.csv`, `assignment_answers.md`, `ceo_basket.csv`, `rating_counts.csv`, and `rating_counts.png`.

The £100 challenge is solved using a 0/1 knapsack algorithm, so each book is selected at most once. Among equally high star totals, the program chooses the cheaper basket.

This is an educational practice site. Its prices and ratings are randomly assigned and should not be treated as actual market evidence.
