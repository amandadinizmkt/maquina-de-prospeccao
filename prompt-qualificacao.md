# Prompt de Qualificação de Leads

Cole esse prompt no Claude logo após colar o CSV com sua lista de leads.

---

## PROMPT

```
Você é um especialista em prospecção para agências de marketing digital e social media.

Abaixo está uma lista de empresas extraída do Google Maps. Sua tarefa é qualificar cada lead e indicar quais têm mais potencial para contratar serviços de social media / marketing digital.

[COLE O CONTEÚDO DO CSV AQUI]

Para cada empresa, avalie:
1. Relevância do nicho para marketing digital (negócios locais que dependem de presença online)
2. Avaliação e número de reviews (empresas com muitas avaliações já investem na experiência do cliente)
3. Presença de site (tem site = mais digital, sem site = pode precisar do zero)

Retorne uma tabela com as colunas:
- Nome
- Score (1-10)
- Motivo (1 frase)
- Canal sugerido (WhatsApp / Instagram DM / E-mail)
- Prioridade (Alta / Média / Baixa)

Depois da tabela, me dê o TOP 5 leads para abordar primeiro com uma justificativa de 2 linhas para cada.
```

---

## Como usar

1. Rode o script: `python3 prospectar.py "seu nicho" "sua cidade"`
2. Abra o CSV gerado (pode abrir no Excel, Numbers ou qualquer editor de texto)
3. Copie todo o conteúdo do CSV
4. Abra o Claude (claude.ai)
5. Cole o prompt acima + o conteúdo do CSV
6. Receba a lista qualificada com score e prioridade
