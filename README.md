# Price Alert Tracker

Monitors a list of specific product URLs and logs items that drop to or below a target price.

## How the watch list works
The watch list is a list of dictionaries, each with a `url` and a `target_price`:

```python
watch_list = [
    {"url": "https://example.com/product1", "target_price": 55.00},
    {"url": "https://example.com/product2", "target_price": 40.00},
]
```

## Output
Deals found are appended to a CSV log file over time (not overwritten), so the log builds a history of past deals.

## Requirements

pip install requests beautifulsoup4


## How to run

python price_alert_tracker.py


## Limitation
Currently hardcoded for one site's HTML structure. Using it on another site would require updating the selectors.
