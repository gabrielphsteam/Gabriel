#!/usr/bin/env python3
"""Gera um recibo ou uma cobrança em PDF a partir de um arquivo JSON.

Uso: python3 gerar_documento.py dados.json saida.pdf
Requer: pip install reportlab
Este documento NÃO é nota fiscal.
"""
import json
import sys
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from xml.sax.saxutils import escape


def brl(valor: float) -> str:
    """Formata como R$ 1.234,56."""
    texto = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {texto}"


def data_br(texto: str) -> str:
    """Aceita AAAA-MM-DD ou DD/MM/AAAA e devolve DD/MM/AAAA."""
    if not texto:
        return ""
    for formato in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(texto, formato).strftime("%d/%m/%Y")
        except ValueError:
            continue
    raise ValueError(f"Data inválida: {texto!r}. Use AAAA-MM-DD ou DD/MM/AAAA.")


def validar(dados: dict) -> None:
    obrigatorios = ["tipo", "emitente", "cliente", "itens"]
    faltando = [c for c in obrigatorios if c not in dados]
    if faltando:
        raise ValueError(f"Campos obrigatórios ausentes: {', '.join(faltando)}")
    if dados["tipo"] not in ("recibo", "cobranca"):
        raise ValueError('"tipo" deve ser "recibo" ou "cobranca".')
    if not dados["itens"]:
        raise ValueError("Informe ao menos um item.")
    for i, item in enumerate(dados["itens"], 1):
        for campo in ("descricao", "quantidade", "valor_unitario"):
            if campo not in item:
                raise ValueError(f"Item {i}: falta o campo {campo!r}.")
        if item["quantidade"] <= 0 or item["valor_unitario"] < 0:
            raise ValueError(f"Item {i}: quantidade deve ser > 0 e valor >= 0.")


def p(texto, estilo):
    return Paragraph(escape(str(texto)), estilo)


def gerar(dados: dict, caminho_pdf: str) -> float:
    validar(dados)
    base = getSampleStyleSheet()
    normal = ParagraphStyle("n", parent=base["Normal"], fontSize=10, leading=14)
    pequeno = ParagraphStyle("s", parent=normal, fontSize=8.5, textColor=colors.HexColor("#555555"))
    titulo = ParagraphStyle("t", parent=base["Title"], fontSize=20, alignment=0, spaceAfter=2)

    eh_recibo = dados["tipo"] == "recibo"
    nome_doc = "RECIBO" if eh_recibo else "COBRANÇA"
    emitente, cliente = dados["emitente"], dados["cliente"]

    doc = SimpleDocTemplate(
        caminho_pdf, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
        title=f"{nome_doc} {dados.get('numero', '')}".strip(),
        author=emitente.get("nome", ""),
    )
    e = []

    cabecalho = f"{nome_doc}"
    if dados.get("numero"):
        cabecalho += f" nº {dados['numero']}"
    e.append(p(cabecalho, titulo))
    e.append(p(f"Emissão: {data_br(dados.get('data_emissao') or datetime.now().strftime('%Y-%m-%d'))}", pequeno))
    if not eh_recibo and dados.get("vencimento"):
        e.append(p(f"Vencimento: {data_br(dados['vencimento'])}", pequeno))
    e.append(Spacer(1, 6 * mm))

    def bloco(rotulo, pessoa):
        linhas = [f"<b>{rotulo}</b>", escape(pessoa.get("nome", ""))]
        for chave, nome in (("documento", "Documento"), ("contato", "Contato"), ("endereco", "Endereço")):
            if pessoa.get(chave):
                linhas.append(f"{nome}: {escape(str(pessoa[chave]))}")
        return Paragraph("<br/>".join(linhas), normal)

    partes = Table([[bloco("DE", emitente), bloco("PARA", cliente)]], colWidths=[85 * mm, 85 * mm])
    partes.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    e.append(partes)
    e.append(Spacer(1, 8 * mm))

    linhas = [["Descrição", "Qtd.", "Valor unit.", "Subtotal"]]
    subtotal = 0.0
    for item in dados["itens"]:
        valor = round(item["quantidade"] * item["valor_unitario"], 2)
        subtotal += valor
        qtd = item["quantidade"]
        qtd_txt = str(int(qtd)) if float(qtd).is_integer() else str(qtd).replace(".", ",")
        linhas.append([p(item["descricao"], normal), qtd_txt, brl(item["valor_unitario"]), brl(valor)])

    desconto = float(dados.get("desconto", 0) or 0)
    total = round(subtotal - desconto, 2)
    if total < 0:
        raise ValueError("O desconto não pode ser maior que o subtotal.")
    if desconto:
        linhas.append(["", "", "Subtotal", brl(subtotal)])
        linhas.append(["", "", "Desconto", f"- {brl(desconto)}"])
    linhas.append(["", "", "TOTAL", brl(total)])

    tabela = Table(linhas, colWidths=[84 * mm, 16 * mm, 35 * mm, 35 * mm], repeatRows=1)
    tabela.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#222222")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 1), (-1, -2), 0.25, colors.HexColor("#CCCCCC")),
        ("FONTNAME", (2, -1), (-1, -1), "Helvetica-Bold"),
        ("LINEABOVE", (2, -1), (-1, -1), 0.8, colors.black),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    e.append(tabela)
    e.append(Spacer(1, 8 * mm))

    if eh_recibo:
        forma = dados.get("forma_pagamento", "")
        data_pg = data_br(dados.get("data_pagamento", ""))
        texto = f"Recebi de {escape(cliente.get('nome', ''))} a quantia de <b>{brl(total)}</b>"
        if forma:
            texto += f" via {escape(forma)}"
        if data_pg:
            texto += f", em {data_pg}"
        texto += ", referente aos itens acima."
        e.append(Paragraph(texto, normal))
    else:
        if dados.get("chave_pix"):
            e.append(Paragraph(f"<b>Pagamento via Pix</b><br/>Chave: {escape(str(dados['chave_pix']))}", normal))
            e.append(Spacer(1, 3 * mm))

    if dados.get("observacoes"):
        e.append(Spacer(1, 3 * mm))
        e.append(p(dados["observacoes"], normal))

    e.append(Spacer(1, 12 * mm))
    e.append(p("Documento sem valor fiscal. Não substitui nota fiscal.", pequeno))
    doc.build(e)
    return total


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Uso: python3 gerar_documento.py dados.json saida.pdf")
    with open(sys.argv[1], encoding="utf-8") as f:
        total = gerar(json.load(f), sys.argv[2])
    print(f"PDF gerado: {sys.argv[2]} (total {brl(total)})")
