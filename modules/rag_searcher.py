import click
import requests
from bs4 import BeautifulSoup
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type((requests.exceptions.RequestException, ValueError))
)
def fetch_duckduckgo_results(search_query, max_results):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    # 添加 timeout，防止请求挂起
    res = requests.post("https://html.duckduckgo.com/html/", data={"q": search_query}, headers=headers, timeout=10)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')
    
    results = []
    for a in soup.find_all('a', class_='result__url', limit=max_results):
        href = a.get('href')
        parent_div = a.find_parent('div', class_='result')
        snippet_elem = parent_div.find('a', class_='result__snippet') if parent_div else None
        snippet = snippet_elem.text.strip() if snippet_elem else "No snippet available."
        results.append({"href": href, "body": snippet})
    
    # 增加校验机制：如果 DuckDuckGo 拦截了爬虫导致没有获取到有效结构，这里抛出异常以便触发重试
    if not results and "No results." not in res.text:
        raise ValueError("No results parsed. The HTML structure might have changed or access was blocked.")
        
    return results

def search_cocos_docs(query, max_results=3):
    """
    Search the official Cocos documentation using DuckDuckGo HTML version.
    This acts as the retrieval step for a RAG pipeline.
    """
    click.echo(f"[*] Searching Cocos official docs for: '{query}'")
    
    search_query = f"site:docs.cocos.com {query}"
    
    try:
        results = fetch_duckduckgo_results(search_query, max_results)

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
