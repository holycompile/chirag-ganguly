import os
import glob
import json
import re
from bs4 import BeautifulSoup

def clean(t):
    if not t: return ''
    return re.sub(r'\s+', ' ', t).strip()

print("=== 1. EXPERIENCES ===")
with open('scraped_pages/experiences.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')
for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p']):
    t = clean(h.get_text())
    if len(t) > 20:
        print(f"[{h.name}] {t[:120]}")

print("\n=== 2. PUBLICATIONS ===")
with open('scraped_pages/publications.html', 'r', encoding='utf-8') as f:
    psoup = BeautifulSoup(f.read(), 'html.parser')
for el in psoup.find_all(['h1', 'h2', 'h3', 'h4', 'article', 'div']):
    t = clean(el.get_text())
    if any(k in t.lower() for k in ['paper', 'springer', 'ieee', 'conference', 'journal', 'doi', 'isbn', 'nature', 'cyber']):
        if len(t) > 30 and len(t) < 400:
            print(f"- {t}")

print("\n=== 3. SOCIALS & CODE LINKS ===")
for fname in ['socials.html', 'code.html', 'card.html', 'linker.html']:
    fpath = f'scraped_pages/{fname}'
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            s = BeautifulSoup(f.read(), 'html.parser')
        print(f"-- {fname} --")
        for a in s.find_all('a', href=True):
            print(f"{clean(a.get_text())} -> {a['href']}")

print("\n=== 4. BLOGS & UTILITIES ===")
for bname in ['blogs.html', 'utilities.html', 'til.html']:
    fpath = f'scraped_pages/{bname}'
    if os.path.exists(fpath):
        with open(fpath, 'r', encoding='utf-8') as f:
            s = BeautifulSoup(f.read(), 'html.parser')
        print(f"-- {bname} --")
        for el in s.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'a'])[:20]:
            t = clean(el.get_text())
            if len(t) > 15:
                print(f"[{el.name}] {t[:100]}")
