"""
Pesquisa digital de um lead — busca Instagram, site e gargalos reais
Usa Playwright Python (já instalado pelo Scrapling)
"""

import asyncio
import json
import re
import sys


async def buscar_instagram(nome: str, cidade: str) -> dict:
    """Busca o Instagram de uma empresa via Google e retorna dados do perfil."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Busca no Google
        query = f"{nome} {cidade} instagram".replace(' ', '+')
        await page.goto(f"https://www.google.com/search?q={query}", wait_until="domcontentloaded")
        await asyncio.sleep(2)

        # Pega links do Instagram nos resultados
        links = await page.eval_on_selector_all(
            'a[href*="instagram.com"]',
            'els => els.map(e => e.href)'
        )
        ig_links = [l for l in links if 'instagram.com' in l
                    and '/p/' not in l and '/reel/' not in l
                    and 'google' not in l]

        if not ig_links:
            await browser.close()
            return {}

        handle_url = ig_links[0]

        # Visita o perfil do Instagram
        await page.goto(handle_url, wait_until="domcontentloaded")
        await asyncio.sleep(2)

        meta = await page.evaluate(
            '() => document.querySelector(\'meta[name="description"]\')?.content || ""'
        )

        await browser.close()

        # Extrai dados da meta description
        seg_m = re.search(r'([\d,.KkMm]+)\s*seguidores', meta)
        posts_m = re.search(r'([\d,.]+)\s*posts|publicações', meta)
        follow_m = re.search(r'([\d,.]+)\s*seguindo', meta)

        handle_m = re.search(r'instagram\.com/([a-zA-Z0-9_.]+)', handle_url)

        return {
            'url': handle_url,
            'handle': f"@{handle_m.group(1)}" if handle_m else '',
            'seguidores': seg_m.group(1) if seg_m else '',
            'posts': posts_m.group(1) if posts_m else '',
            'seguindo': follow_m.group(1) if follow_m else '',
            'bio': meta,
        }


async def buscar_site(nome: str, cidade: str) -> str:
    """Busca o site oficial de uma empresa via Google."""
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        query = f"{nome} {cidade} site oficial".replace(' ', '+')
        await page.goto(f"https://www.google.com/search?q={query}", wait_until="domcontentloaded")
        await asyncio.sleep(2)

        links = await page.eval_on_selector_all('cite', 'els => els.map(e => e.innerText)')
        await browser.close()

        ignorar = re.compile(r'google|instagram|facebook|youtube|tiktok|wikipedia|amazon', re.I)
        for l in links:
            if l and not ignorar.search(l):
                return l.strip()
        return ''


async def pesquisar(nome: str, cidade: str) -> dict:
    print(f"  🔍 Pesquisando {nome}...", flush=True)

    ig_task = buscar_instagram(nome, cidade)
    site_task = buscar_site(nome, cidade)

    ig_data, site = await asyncio.gather(ig_task, site_task, return_exceptions=True)

    if isinstance(ig_data, Exception):
        ig_data = {}
    if isinstance(site, Exception):
        site = ''

    return {
        'nome': nome,
        'cidade': cidade,
        'instagram': ig_data,
        'site': site,
    }


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 pesquisar_lead.py \"Nome da Empresa\" \"Cidade\"")
        sys.exit(1)

    nome = sys.argv[1]
    cidade = sys.argv[2]

    resultado = asyncio.run(pesquisar(nome, cidade))
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
