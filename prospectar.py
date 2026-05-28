"""
Máquina de Prospecção com IA — Clube Divos da IA
Extrai empresas do Google Maps e salva em CSV
"""

import asyncio
import csv
import re
import sys
from datetime import datetime
from pathlib import Path

try:
    from scrapling.fetchers import DynamicFetcher
except ImportError:
    print("❌ Scrapling não instalado. Rode:")
    print('   pip install "scrapling[fetchers]"')
    print("   scrapling install")
    sys.exit(1)


SCROLL_ROUNDS = 8

# Domínios a ignorar na extração de links
IGNORAR_DOMINIOS = re.compile(
    r'(google\.|goo\.gl|googleapis|googletagmanager|facebook\.com/tr|'
    r'schema\.org|w3\.org|openstreetmap|apple\.com/maps)',
    re.I
)


async def scroll_results(page):
    for _ in range(SCROLL_ROUNDS):
        await page.evaluate("""
            const panel = document.querySelector('[role="feed"]') ||
                          document.querySelector('.m6QErb') ||
                          document.querySelector('.DxyBCb');
            if (panel) panel.scrollTop += 1000;
            else window.scrollBy(0, 1000);
        """)
        await asyncio.sleep(1.8)


async def buscar_link_google(nome: str, cidade: str, fetcher: DynamicFetcher) -> str:
    """Busca o site ou Instagram da empresa no Google."""
    try:
        query = f"{nome} {cidade}".replace(' ', '+')
        url = f"https://www.google.com/search?q={query}"

        async def aguardar(page):
            await asyncio.sleep(2)

        resp = await fetcher.async_fetch(url, wait=2000, page_action=aguardar)
        html = str(resp)

        # Prioridade: site oficial > Instagram > Facebook > Linktree
        padroes = [
            r'href="(https?://(?:www\.)?instagram\.com/(?!p/|reel/|explore/)[a-zA-Z0-9_.]{3,40}/?)"',
            r'href="(https?://linktr\.ee/[^"]{3,60})"',
            r'href="(https?://(?!(?:www\.)?(?:google|goo\.gl|facebook|instagram|youtube|twitter|tiktok|whatsapp|wikipedia|amazon))[a-zA-Z0-9\-]{3,}\.(?:com\.br|com|net|org|io|co)[^"]{0,60})"',
            r'href="(https?://(?:www\.)?facebook\.com/(?!sharer|share|dialog)[a-zA-Z0-9_.]{3,60}/?)"',
        ]

        for padrao in padroes:
            m = re.search(padrao, html, re.I)
            if m:
                return m.group(1)
    except Exception:
        pass
    return ''


async def scrape(nicho: str, cidade: str) -> list[dict]:
    query = f"{nicho} {cidade}"
    url = f"https://www.google.com/maps/search/{query.replace(' ', '+')}"

    async def page_action(page):
        await asyncio.sleep(3)
        await scroll_results(page)

    fetcher = DynamicFetcher()
    response = await fetcher.async_fetch(url, network_idle=True, wait=2000, page_action=page_action)

    items = response.css('[role="article"]')
    results = []
    seen = set()

    for item in items:
        html = str(item)
        nome = item.attrib.get('aria-label', '').strip()
        if not nome or nome in seen:
            continue
        seen.add(nome)

        rating_m = re.search(r'class="MW4etd"[^>]*>([^<]+)', html)
        reviews_m = re.search(r'aria-label="[\d,.]+ estrelas[^(]*\(([\d.]+)\)', html)
        tel_m = re.search(r'\((\d{2})\)\s*([\d\s\-]{8,13}\d)', html)
        end_m = re.search(r'>(R\.|Av\.|Rua |Alameda|Al\.|Travessa|Praça)[^<"]{5,80}', html)

        # Link direto no card
        site_m = re.search(
            r'href="(https?://(?!(?:www\.)?(?:google|goo\.gl))[^"]{5,80})"',
            html
        )
        link_card = site_m.group(1) if site_m and not IGNORAR_DOMINIOS.search(site_m.group(1)) else ''

        # URL da página de detalhes do Maps para buscar link depois
        maps_link_m = re.search(r'href="(https://www\.google\.com/maps/place/[^"]+)"', html)
        maps_link = maps_link_m.group(1) if maps_link_m else ''

        results.append({
            'nome': nome,
            'avaliacao': rating_m.group(1) if rating_m else '',
            'reviews': reviews_m.group(1) if reviews_m else '',
            'telefone': f"({tel_m.group(1)}) {tel_m.group(2).strip()}" if tel_m else '',
            'endereco': end_m.group().lstrip('>').strip() if end_m else '',
            'link': link_card,
            '_maps_link': maps_link,
            'nicho': nicho,
            'cidade': cidade,
        })

    # Leads sem link ficam marcados para pesquisa na próxima etapa
    for r in results:
        if not r['link']:
            r['link'] = ''

    # Remove coluna interna
    for r in results:
        r.pop('_maps_link', None)

    return results


def salvar_csv(results: list[dict], nicho: str, cidade: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    slug = f"{nicho}_{cidade}".replace(' ', '_')
    nome_arquivo = f"leads_{slug}_{timestamp}.csv"
    caminho = Path(__file__).parent / nome_arquivo

    campos = ['nome', 'avaliacao', 'reviews', 'telefone', 'endereco', 'link', 'nicho', 'cidade']
    with open(caminho, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(results)

    return str(caminho)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python3 prospectar.py \"nicho\" \"cidade\"")
        sys.exit(1)

    nicho, cidade = sys.argv[1], sys.argv[2]
    results = asyncio.run(scrape(nicho, cidade))

    if not results:
        print("Nenhum resultado encontrado.")
        sys.exit(1)

    caminho = salvar_csv(results, nicho, cidade)
    print(caminho)  # só retorna o caminho do CSV
