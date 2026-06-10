"""Small public-web scraper used when no search API is configured."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


@dataclass(frozen=True, slots=True)
class PageLink:
    title: str
    url: str


def fetch_page(url: str, timeout: int = 20) -> str:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "GoblinRecon/0.1 public research bot"},
    )
    response.raise_for_status()
    return response.text


def extract_links(url: str, html: str | None = None, limit: int = 25) -> list[PageLink]:
    html = html if html is not None else fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")
    links: list[PageLink] = []
    seen: set[str] = set()
    for anchor in soup.find_all("a", href=True):
        title = " ".join(anchor.get_text(" ").split())
        href = urljoin(url, anchor["href"])
        if not title or href in seen:
            continue
        seen.add(href)
        links.append(PageLink(title=title, url=href))
        if len(links) >= limit:
            break
    return links


def extract_text(url: str, html: str | None = None) -> str:
    html = html if html is not None else fetch_page(url)
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    return "\n".join(line for line in soup.get_text("\n").splitlines() if line.strip())
