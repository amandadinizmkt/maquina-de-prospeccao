"""
Pesquisa digital de um lead — busca gargalos reais no site, Instagram e Google Maps
"""

import asyncio
import sys
import json
import re
from scrapling.fetchers import DynamicFetcher, StealthyFetcher


async def analisar_site(url: str) -> dict:
    if not url:
        return {'tem_site': False}
    try:
        fetcher = StealthyFetcher()
        page = await fetcher.async_fetch(url, wait=3000)
        html = str(page)

        # Detectar sinais de qualidade do site
        tem_instagram = bool(re.search(r'instagram\.com/', html, re.I))
        tem_facebook = bool(re.search(r'facebook\.com/', html, re.I))
        tem_whatsapp = bool(re.search(r'whatsapp|wa\.me', html, re.I))
        tem_blog = bool(re.search(r'/blog|/artigos|/noticias', html, re.I))

        # Detectar tecnologia (Wix, WordPress etc)
        plataforma = 'desconhecida'
        if 'wix.com' in html or 'wixsite' in html:
            plataforma = 'Wix'
        elif 'wordpress' in html.lower() or 'wp-content' in html:
            plataforma = 'WordPress'
        elif 'webflow' in html.lower():
            plataforma = 'Webflow'
        elif 'squarespace' in html.lower():
            plataforma = 'Squarespace'
        elif 'shopify' in html.lower():
            plataforma = 'Shopify'

        # Links de redes sociais presentes
        instagram_handle = re.search(r'instagram\.com/([a-zA-Z0-9_.]+)', html)

        return {
            'tem_site': True,
            'url': url,
            'plataforma': plataforma,
            'tem_instagram_link': tem_instagram,
            'tem_facebook_link': tem_facebook,
            'tem_whatsapp': tem_whatsapp,
            'tem_blog': tem_blog,
            'instagram_handle': instagram_handle.group(1) if instagram_handle else None,
        }
    except Exception as e:
        return {'tem_site': True, 'url': url, 'erro': str(e)[:100]}


async def analisar_instagram(handle: str) -> dict:
    if not handle:
        return {}
    try:
        url = f"https://www.instagram.com/{handle.strip('@')}/"
        fetcher = StealthyFetcher()
        page = await fetcher.async_fetch(url, wait=3000)
        html = str(page)

        # Extrair dados básicos do perfil
        seguidores = re.search(r'"edge_followed_by":\{"count":(\d+)\}', html)
        seguindo = re.search(r'"edge_follow":\{"count":(\d+)\}', html)
        posts = re.search(r'"edge_owner_to_timeline_media":\{"count":(\d+)', html)
        bio = re.search(r'"biography":"([^"]{0,200})"', html)

        return {
            'handle': handle,
            'seguidores': int(seguidores.group(1)) if seguidores else None,
            'seguindo': int(seguindo.group(1)) if seguindo else None,
            'posts': int(posts.group(1)) if posts else None,
            'bio': bio.group(1) if bio else None,
        }
    except Exception:
        return {'handle': handle}


async def pesquisar(nome: str, site: str = '', instagram: str = '') -> dict:
    tasks = [analisar_site(site)]
    if instagram:
        tasks.append(analisar_instagram(instagram))

    resultados = await asyncio.gather(*tasks, return_exceptions=True)

    dados = {
        'nome': nome,
        'site': resultados[0] if not isinstance(resultados[0], Exception) else {},
        'instagram': resultados[1] if len(resultados) > 1 and not isinstance(resultados[1], Exception) else {},
    }
    return dados


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 pesquisar_lead.py \"Nome\" \"site\" \"@instagram\"")
        sys.exit(1)

    nome = sys.argv[1]
    site = sys.argv[2] if len(sys.argv) > 2 else ''
    instagram = sys.argv[3] if len(sys.argv) > 3 else ''

    resultado = asyncio.run(pesquisar(nome, site, instagram))
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
