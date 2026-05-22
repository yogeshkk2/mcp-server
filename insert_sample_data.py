from tools.neo4j_client import store_article, list_articles

# Insert sample articles
sample_articles = [
    ('Breaking News: AI Advances', 'https://example.com/ai-advances'),
    ('Tech Giants Announce Partnership', 'https://example.com/partnership'),
    ('Latest Security Updates Released', 'https://example.com/security'),
    ('Cloud Computing Trends 2026', 'https://example.com/cloud-trends'),
    ('Python 3.12 Features Overview', 'https://example.com/python-312'),
]

for title, url in sample_articles:
    store_article(title, url)
    print(f'✓ Stored: {title}')

# Verify insertion
articles = list_articles(limit=10)
print(f'\nTotal articles in database: {len(articles)}')
for article in articles:
    title = article['title']
    print(f'  - {title}')
