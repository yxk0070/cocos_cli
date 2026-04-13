import click
import requests
from bs4 import BeautifulSoup

def search_cocos_docs(query, max_results=3):
    """
    Search the official Cocos documentation using DuckDuckGo HTML version.
    This acts as the retrieval step for a RAG pipeline.
    """
    click.echo(f"[*] Searching Cocos official docs for: '{query}'")
    
    search_query = f"site:docs.cocos.com {query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    
    try:
        res = requests.post("https://html.duckduckgo.com/html/", data={"q": search_query}, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        results = []
        for a in soup.find_all('a', class_='result__url', limit=max_results):
            href = a.get('href')
            snippet_elem = a.find_parent('div', class_='result').find('a', class_='result__snippet')
            snippet = snippet_elem.text.strip() if snippet_elem else "No snippet available."
            results.append({"href": href, "body": snippet})

        if not results:
            click.echo("[-] No relevant documentation found.")
            return

        click.echo(f"[+] Found {len(results)} relevant documents:\n")
        
        for idx, res in enumerate(results, 1):
            click.echo(f"--- Document {idx} ---")
            click.echo(f"URL:   {res.get('href')}")
            click.echo(f"Snippet:\n{res.get('body')}\n")
            
    except Exception as e:
        click.echo(f"[!] RAG Search failed: {e}")
