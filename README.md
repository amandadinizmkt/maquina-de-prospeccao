# Máquina de Prospecção com IA
### Clube Divos da IA — Amanda Diniz

Ferramenta para encontrar leads no Google Maps, pesquisar gargalos digitais de cada empresa e gerar mensagens de abordagem personalizadas — tudo dentro do Claude Code, sem precisar abrir terminal.

---

## Como usar

Você não precisa rodar nada manualmente. Basta abrir o **Claude Code** e seguir os passos abaixo.

### Passo 1 — Instalar (uma vez só)

No Claude Code, peça:
> *"Clona o repositório github.com/amandadinizmkt/maquina-de-prospeccao, verifica se tenho Python instalado e instala o Scrapling"*

### Passo 2 — Buscar leads

> *"Busca [tipo de empresa] em [cidade]"*

O Claude roda o script, mostra a lista e entrega o arquivo CSV.

### Passo 3 — Escolher os leads

Olhe a planilha e diga quais quer aprofundar:
> *"Quero os números 3, 7 e 12"* ou *"Você escolhe os 5 melhores"*

### Passo 4 — Pesquisar gargalos

O Claude visita o site e Instagram de cada lead escolhido e identifica problemas reais: site desatualizado, Instagram abandonado, sem WhatsApp, sem agendamento online.

### Passo 5 — Receber as mensagens

> *"Agora gera as mensagens. Meu nome é [nome] e trabalho com [serviço]"*

O Claude entrega um arquivo `.docx` com mensagens personalizadas para cada lead.

---

## Requisitos

- [Claude Code](https://claude.ai/code) instalado
- Python 3.10+ (o Claude verifica e instala se precisar)
- Scrapling (o Claude instala automaticamente)

---

## Arquivos

| Arquivo | O que faz |
|---------|-----------|
| `prospectar.py` | Busca empresas no Google Maps e gera CSV |
| `pesquisar_lead.py` | Visita site e Instagram de cada lead |
| `gerar_mensagens.py` | Gera o DOCX com mensagens personalizadas |

---

## Custos

| Ferramenta | Custo |
|------------|-------|
| Claude Code | Incluído no plano |
| Scrapling | Gratuito |
| Google Maps scraping | Gratuito |

---

Clube Divos da IA · agenciafurtacor.com
