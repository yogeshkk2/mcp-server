from neo4j import GraphDatabase
import os

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://neo4j:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "test")

_driver = None


def init_driver():
    global _driver
    if _driver is None:
        _driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver


def close_driver():
    global _driver
    if _driver is not None:
        _driver.close()
        _driver = None


def _create_article_tx(tx, title, url):
    tx.run(
        "MERGE (a:Article {url: $url}) SET a.title = $title, a.created = coalesce(a.created, timestamp())",
        title=title,
        url=url,
    )


def store_article(title: str, url: str) -> None:
    d = init_driver()
    with d.session() as session:
        session.execute_write(_create_article_tx, title, url)


def _list_articles_tx(tx, limit: int):
    result = tx.run("MATCH (a:Article) RETURN a.title as title, a.url as url ORDER BY a.created DESC LIMIT $limit", limit=limit)
    return [record.data() for record in result]


def list_articles(limit: int = 10) -> list[dict]:
    d = init_driver()
    with d.session() as session:
        return session.execute_read(_list_articles_tx, limit)
