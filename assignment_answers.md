# Bookstore Intelligence — Results

**Scope:** First 5 catalogue pages; 100 books.

## Mission 1 — HTML reconnaissance
| Data | HTML tag / class | Notes |
|---|---|---|
| Book title | `article.product_pod h3 a` | Read the `title` attribute for the full title. |
| Price | `p.price_color` | Remove the £ symbol and convert to a number. |
| Rating | `p.star-rating` | Convert One–Five class names to 1–5. |
| Availability | `p.instock.availability` | Read the stock message and standardize it. |

## Mission 4 — Answers
1. Most expensive: **The Death of Humanity: and the Case for Life** (£58.11).
2. Cheapest: **Patience** (£10.16).
3. Average price: **£34.56**.
4. Five-star books: **19**.
5. In stock: **100.0%**.
6. Top five highest-rated (ties ordered by lowest price):

| Title | Price | Stars |
|---|---:|---:|
| Princess Between Worlds (Wide-Awake Princess #5) | £13.34 | 5 |
| Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1) | £13.61 | 5 |
| Sophie's World | £15.94 | 5 |
| Thirst | £17.27 | 5 |
| Set Me Free | £17.46 | 5 |

7. Cheapest five-star book: **Princess Between Worlds (Wide-Awake Princess #5)** (£13.34).

## CEO challenge — £100 budget
Each title can be purchased at most once. The basket maximizes the total star score, and breaks score ties by spending less.

| Selected title | Price | Stars |
|---|---:|---:|
| Sophie's World | £15.94 | 5 |
| Untitled Collection: Sabbath Poems 2014 | £14.27 | 4 |
| Thirst | £17.27 | 5 |
| Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1) | £13.61 | 5 |
| Princess Between Worlds (Wide-Awake Princess #5) | £13.34 | 5 |
| Patience | £10.16 | 3 |
| Mama Tried: Traditional Italian Cooking for the Screwed, Crude, Vegan, and Tattooed | £14.02 | 4 |
| **Total** | **£98.61** | **31** |

## Rating counts
| Stars | Books |
|---:|---:|
| 1 | 22 |
| 2 | 19 |
| 3 | 22 |
| 4 | 18 |
| 5 | 19 |

## Business recommendation
I would start with **Princess Between Worlds (Wide-Awake Princess #5)** and **Princess Jellyfish 2-in-1 Omnibus, Vol. 01 (Princess Jellyfish 2-in-1 Omnibus #1)**. Both are listed as in stock, and their ratings are 5 and 5 stars, respectively. Their prices (£13.34 and £13.61) also make them useful options to compare before choosing an opening product range.

Note: The practice website assigns ratings and prices randomly. These figures are useful for demonstrating analysis, not real customer demand.
