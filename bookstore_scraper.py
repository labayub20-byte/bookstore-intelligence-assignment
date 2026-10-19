"""Bookstore Intelligence — scrape the practice catalogue and analyse it."""
from pathlib import Path
from urllib.parse import urljoin
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

BASE = 'https://books.toscrape.com/'
PAGES = 5  # Change to 50 for the boss-level challenge.
RATINGS = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
OUT = Path(__file__).resolve().parent


def scrape_books(pages=PAGES):
    records = []
    with requests.Session() as session:
        session.headers.update({'User-Agent': 'BookstoreClassProject/1.0 (educational)'})
        for page in range(1, pages + 1):
            url = urljoin(BASE, f'catalogue/page-{page}.html')
            response = session.get(url, timeout=20)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            cards = soup.select('article.product_pod')
            if not cards:
                raise ValueError(f'No product cards found on page {page}')
            for card in cards:
                link = card.select_one('h3 a')
                rating = card.select_one('p.star-rating')
                price = card.select_one('p.price_color')
                stock = card.select_one('p.instock.availability')
                if not all((link, rating, price, stock)):
                    raise ValueError(f'Missing data on page {page}')
                word = next((c for c in rating.get('class', []) if c in RATINGS), None)
                if word is None:
                    raise ValueError(f'Unknown rating on page {page}')
                records.append({
                    'Title': link.get('title', link.get_text(' ', strip=True)),
                    'Price': float(price.get_text(strip=True).replace('£', '').replace('Â', '')),
                    'Rating': RATINGS[word],
                    'Availability': 'In stock' if 'In stock' in stock.get_text(' ', strip=True) else 'Out of stock',
                    'Product URL': urljoin(url, link['href']),
                })
            print(f'Page {page}: {len(cards)} books')
            if page < pages:
                time.sleep(0.3)
    df = pd.DataFrame(records)
    if df.empty or df[['Title', 'Price', 'Rating', 'Availability']].isna().any().any():
        raise ValueError('Dataset is empty or incomplete')
    return df


def best_basket(df, budget_pence=10000):
    """0/1 knapsack: maximize stars; among ties, minimize cost."""
    states = {0: (0, ())}
    for i, book in df.iterrows():
        cost = int(round(float(book['Price']) * 100))
        stars = int(book['Rating'])
        for old_cost, (old_stars, selected) in list(states.items()):
            new_cost = old_cost + cost
            if new_cost > budget_pence:
                continue
            candidate = (old_stars + stars, selected + (i,))
            if new_cost not in states or candidate[0] > states[new_cost][0]:
                states[new_cost] = candidate
    cost, (stars, indices) = max(states.items(), key=lambda pair: (pair[1][0], -pair[0]))
    return df.loc[list(indices)], cost / 100, stars


def main():
    df = scrape_books()
    df.to_csv(OUT / 'competitor_books.csv', index=False, encoding='utf-8-sig')
    print('\nFirst five rows:\n', df.head().to_string(index=False))
    print('\nColumns:', list(df.columns))
    counts = df['Rating'].value_counts().reindex(range(1, 6), fill_value=0).sort_index()
    counts.to_csv(OUT / 'rating_counts.csv', header=['Count'])
    ax = counts.plot.bar(title='Books by star rating', rot=0)
    ax.set_xlabel('Star rating')
    ax.set_ylabel('Number of books')
    plt.tight_layout()
    plt.savefig(OUT / 'rating_counts.png', dpi=180)
    plt.close()
    five = df[df.Rating == 5].sort_values(['Price', 'Title'])
    top = df.sort_values(['Rating', 'Price', 'Title'], ascending=[False, True, True]).head(5)
    basket, spent, score = best_basket(df)
    basket.to_csv(OUT / 'ceo_basket.csv', index=False)
    lines = [
        '# Bookstore Intelligence — Results',
        '',
        f'**Scope:** First {PAGES} catalogue pages; {len(df)} books.',
        '',
        '## Mission 1 — HTML reconnaissance',
        '| Data | HTML tag / class | Notes |',
        '|---|---|---|',
        '| Book title | `article.product_pod h3 a` | Read the `title` attribute for the full title. |',
        '| Price | `p.price_color` | Remove the £ symbol and convert to a number. |',
        '| Rating | `p.star-rating` | Convert One–Five class names to 1–5. |',
        '| Availability | `p.instock.availability` | Read the stock message and standardize it. |',
        '',
        '## Mission 4 — Answers',
        f'1. Most expensive: **{df.loc[df.Price.idxmax(), "Title"]}** (£{df.Price.max():.2f}).',
        f'2. Cheapest: **{df.loc[df.Price.idxmin(), "Title"]}** (£{df.Price.min():.2f}).',
        f'3. Average price: **£{df.Price.mean():.2f}**.',
        f'4. Five-star books: **{len(five)}**.',
        f'5. In stock: **{(df.Availability == "In stock").mean()*100:.1f}%**.',
        '6. Top five highest-rated (ties ordered by lowest price):',
        '',
        '| Title | Price | Stars |', '|---|---:|---:|',
    ]
    lines.extend(f'| {row.Title.replace("|", "-")} | £{row.Price:.2f} | {row.Rating} |' for row in top.itertuples())
    lines += ['', f'7. Cheapest five-star book: **{five.iloc[0].Title}** (£{five.iloc[0].Price:.2f}).' if len(five) else '7. No five-star books in this sample.', '',
              '## CEO challenge — £100 budget',
              'Each title can be purchased at most once. The basket maximizes the total star score, and breaks score ties by spending less.',
              '', '| Selected title | Price | Stars |', '|---|---:|---:|']
    lines.extend(f'| {row.Title.replace("|", "-")} | £{row.Price:.2f} | {row.Rating} |' for row in basket.itertuples())
    lines += [f'| **Total** | **£{spent:.2f}** | **{score}** |', '',
              '## Rating counts', '| Stars | Books |', '|---:|---:|']
    lines.extend(f'| {stars} | {count} |' for stars, count in counts.items())
    available = df[df.Availability == 'In stock']
    priority = available.sort_values(['Rating', 'Price'], ascending=[False, True]).head(2)
    if len(priority) >= 2:
        a, b = priority.iloc[0], priority.iloc[1]
        lines += ['', '## Business recommendation',
                  f'I would start with **{a.Title}** and **{b.Title}**. Both are listed as in stock, and their ratings are {int(a.Rating)} and {int(b.Rating)} stars, respectively. Their prices (£{a.Price:.2f} and £{b.Price:.2f}) also make them useful options to compare before choosing an opening product range.',
                  '', 'Note: The practice website assigns ratings and prices randomly. These figures are useful for demonstrating analysis, not real customer demand.']
    (OUT / 'assignment_answers.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    print('\nSaved CSV, answers, basket, rating counts and chart.')


if __name__ == '__main__':
    main()
