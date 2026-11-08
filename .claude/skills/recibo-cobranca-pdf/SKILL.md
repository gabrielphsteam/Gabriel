---
name: recibo-cobranca-pdf
description: Gera recibo ou cobrança em PDF (valores em reais, datas em formato brasileiro, chave Pix opcional) a partir dos dados do emitente, do cliente e dos itens. Use quando o usuário pedir "recibo", "cobrança em PDF", "fatura simples" ou "comprovante para o cliente". Não emite nota fiscal.
---

# Recibo e cobrança em PDF

Gera um documento simples e limpo com o script `scripts/gerar_documento.py`. O documento sai com a frase "Documento sem valor fiscal. Não substitui nota fiscal." Se o usuário precisa de nota fiscal, diga que isso é emitido pelo sistema da prefeitura ou da Receita, não por esta skill.

## Passo a passo

1. **Reúna os dados** (pergunte só o que faltar):
   - tipo: `recibo` (pagamento já feito) ou `cobranca` (pagamento a receber);
   - emitente e cliente (nome; documento, contato e endereço são opcionais);
   - itens: descrição, quantidade e valor unitário;
   - para cobrança: vencimento e, se houver, chave Pix;
   - para recibo: forma e data do pagamento;
   - número do documento, desconto e observações, se houver.
2. **Monte o JSON** em um arquivo (modelo abaixo). Nunca coloque CPF, chave Pix ou dados de cliente em lugar público ou em commits do repositório; trabalhe com o arquivo na pasta temporária da sessão.
3. **Gere o PDF:**
   ```sh
   pip install reportlab   # se ainda não estiver instalado
   python3 .claude/skills/recibo-cobranca-pdf/scripts/gerar_documento.py dados.json documento.pdf
   ```
4. **Confira o resultado:** abra o PDF (por exemplo, `pdftoppm -png -r 70 documento.pdf pagina` e veja a imagem) e confirme nomes, valores, datas e total. Confira a soma de cabeça: o script calcula, mas você valida.
5. **Entregue** o PDF ao usuário com uma frase de resumo (tipo, cliente, total). Não envie a ninguém em nome dele sem pedido explícito.

## Modelo de dados

```json
{
  "tipo": "cobranca",
  "numero": "2026-014",
  "data_emissao": "2026-11-08",
  "vencimento": "2026-11-15",
  "emitente": {"nome": "Nome de quem cobra", "contato": "(11) 90000-0000"},
  "cliente": {"nome": "Nome do cliente"},
  "itens": [
    {"descricao": "Plano mensal", "quantidade": 1, "valor_unitario": 39.90}
  ],
  "desconto": 0,
  "chave_pix": "chave@exemplo.com",
  "observacoes": "Obrigado pela preferência."
}
```

Para recibo, troque `"tipo"` por `"recibo"` e use `"forma_pagamento": "Pix"` e `"data_pagamento": "2026-11-08"` no lugar de vencimento e chave Pix.

## Regras do script

- Datas aceitas: `AAAA-MM-DD` ou `DD/MM/AAAA`; saem como `DD/MM/AAAA`.
- Valores saem como `R$ 1.234,56`.
- O script para com erro claro se faltar campo, se a quantidade for zero ou se o desconto passar do subtotal.
