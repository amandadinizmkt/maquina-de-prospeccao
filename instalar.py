"""
Setup da Máquina de Prospecção — Clube Divos da IA
Verifica e instala tudo que é necessário: Python, Scrapling e Playwright
"""

import sys
import subprocess


def check(cmd):
    try:
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except Exception:
        return False


def run(cmd, desc):
    print(f"  → {desc}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ❌ Erro: {result.stderr.strip()[:200]}")
        return False
    return True


def main():
    print("\n" + "=" * 55)
    print("  Instalando Máquina de Prospecção — Divos da IA")
    print("=" * 55 + "\n")

    # 1. Python
    version = sys.version_info
    if version.major < 3 or version.minor < 10:
        print(f"❌ Python {version.major}.{version.minor} detectado.")
        print("   Necessário Python 3.10 ou superior.")
        print("   Baixe em: https://python.org/downloads")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor} — ok")

    # 2. Scrapling
    try:
        import scrapling
        print(f"✅ Scrapling {scrapling.__version__} — já instalado")
    except ImportError:
        print("📦 Instalando Scrapling...")
        ok = run(
            [sys.executable, "-m", "pip", "install", "scrapling[fetchers]",
             "--break-system-packages", "-q"],
            "pip install scrapling[fetchers]"
        )
        if not ok:
            # tenta sem --break-system-packages (Windows/venv)
            run([sys.executable, "-m", "pip", "install", "scrapling[fetchers]", "-q"],
                "pip install scrapling[fetchers] (alternativo)")

    # 3. Playwright browsers (via scrapling install)
    print("🌐 Instalando navegadores do Playwright...")
    run(["scrapling", "install"], "scrapling install")

    # 4. Playwright Python (para pesquisa de leads)
    try:
        import playwright
        print("✅ Playwright Python — já instalado")
    except ImportError:
        run([sys.executable, "-m", "pip", "install", "playwright",
             "--break-system-packages", "-q"],
            "pip install playwright")
        run([sys.executable, "-m", "playwright", "install", "chromium"],
            "playwright install chromium")

    # 5. python-docx (para gerar mensagens)
    try:
        import docx
        print("✅ python-docx — já instalado")
    except ImportError:
        run([sys.executable, "-m", "pip", "install", "python-docx",
             "--break-system-packages", "-q"],
            "pip install python-docx")

    print("\n✅ Tudo instalado! Pronto para prospectar.")
    print("\nComo usar:")
    print('  python3 prospectar.py "seu nicho" "sua cidade"\n')


if __name__ == "__main__":
    main()
