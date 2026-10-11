"""Monta IngressoData_01_Excel.xlsx: base bruta empilhada + tratamento 100% por fórmulas."""
import csv
import sys
from pathlib import Path

import openpyxl
from openpyxl.chart import BarChart, PieChart, Reference
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

FONTE = "Arial"
AZUL_ESCURO, VERMELHO = "1F3A5F", "A51C1C"
CABECALHO = PatternFill("solid", fgColor=AZUL_ESCURO)
ENTRADA = PatternFill("solid", fgColor="FFF2CC")
FINO = Side(style="thin", color="BFBFBF")
MOEDA = '"R$" #,##0.00'
PERCENTUAL = "0.0%"
COLUNAS_BRUTAS = ["ID_Venda", "Data_Venda", "Data_Evento", "Evento", "Categoria", "Cidade_Evento", "Tipo_Ingresso",
                  "Qtd", "Valor_Unitario", "Canal", "Comprador_ID", "Cidade_Comprador", "UF_Comprador",
                  "Pais_Comprador", "CEP_Comprador"]


def estilizar_cabecalho(ws, linha=1):
    for celula in ws[linha]:
        if celula.value is not None:
            celula.font = Font(name=FONTE, bold=True, color="FFFFFF")
            celula.fill = CABECALHO
            celula.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def fonte_padrao(ws):
    for linha in ws.iter_rows():
        for celula in linha:
            if celula.font.name != FONTE:
                celula.font = Font(name=FONTE, bold=celula.font.bold, color=celula.font.color,
                                   italic=celula.font.italic, size=celula.font.size)


def larguras(ws, valores):
    for indice, largura in enumerate(valores, start=1):
        ws.column_dimensions[get_column_letter(indice)].width = largura


def adicionar_tabela(ws, nome, ultima_linha, ultima_coluna):
    tabela = Table(displayName=nome, ref=f"A1:{get_column_letter(ultima_coluna)}{ultima_linha}")
    tabela.tableStyleInfo = TableStyleInfo(name="TableStyleLight9", showRowStripes=True)
    ws.add_table(tabela)


def ler_brutos(pasta):
    pasta = Path(pasta)
    linhas = []
    for nome in ("vendas_SP.xlsx", "vendas_RJ.xlsx"):
        ws = openpyxl.load_workbook(pasta / nome).active
        for valores in ws.iter_rows(min_row=2, values_only=True):
            linhas.append(list(valores) + [nome])
    with open(pasta / "vendas_MG.csv", encoding="utf-8") as arquivo:
        leitor = csv.reader(arquivo, delimiter=";")
        next(leitor)
        for valores in leitor:
            linhas.append([v if v != "" else None for v in valores] + ["vendas_MG.csv"])
    return linhas


def aba_de_para(wb, pasta):
    apoio = openpyxl.load_workbook(Path(pasta) / "tabelas_apoio.xlsx")
    tamanhos = {}
    for nome in ("DePara_Categoria", "DePara_Cidade", "DePara_Pais", "Cadastro_Eventos"):
        origem, destino = apoio[nome], wb.create_sheet(nome)
        for valores in origem.iter_rows(values_only=True):
            destino.append(list(valores))
        estilizar_cabecalho(destino)
        for linha in destino.iter_rows(min_row=2):
            for celula in linha:
                celula.fill = ENTRADA
        if nome == "Cadastro_Eventos":
            for celula in destino["F"][1:]:
                celula.number_format = "dd/mm/yyyy"
        larguras(destino, [34, 22, 18, 28, 14, 14])
        destino.freeze_panes = "A2"
        tamanhos[nome] = destino.max_row
    return tamanhos


def aba_base_bruta(wb, linhas):
    ws = wb.create_sheet("Base_Bruta", 1)
    ws.append(COLUNAS_BRUTAS + ["Arquivo_Origem"])
    for valores in linhas:
        ws.append(valores)
        if ws.cell(ws.max_row, 2).value is not None and not isinstance(ws.cell(ws.max_row, 2).value, str):
            ws.cell(ws.max_row, 2).number_format = "dd/mm/yyyy"
            ws.cell(ws.max_row, 3).number_format = "dd/mm/yyyy"
    estilizar_cabecalho(ws)
    larguras(ws, [12, 12, 12, 30, 14, 18, 12, 6, 14, 11, 12, 18, 8, 10, 12, 16])
    ws.freeze_panes = "B2"
    ws["A1"].comment = Comment("Dados SIMULADOS empilhados SEM tratamento (SP + RJ + MG). "
                               "Não editar: o tratamento acontece na aba Tratamento.", "IngressoData")
    return ws.max_row


def lookup(chave, aba, ultima, padrao="REVISAR"):
    """Busca no De-Para. Escrito como INDEX/CORRESP e convertido para PROCX no fim do build."""
    return (f'IFERROR(INDEX({aba}!$B$2:$B${ultima},MATCH({chave},{aba}!$A$2:$A${ultima},0)),"{padrao}")')


def aba_tratamento(wb, ultima_bruta, tamanhos):
    ws = wb.create_sheet("Tratamento", 2)
    cabecalhos = ["ID_Venda", "Data_Venda", "Data_Evento", "Evento", "Categoria", "Cidade_Evento", "Tipo_Ingresso",
                  "Qtd", "Valor_Unitario", "Valor_Total", "Canal", "Comprador_ID", "Cidade_Comprador",
                  "UF_Comprador", "Pais_Comprador", "Origem_Publico", "Mes_Venda", "Duplicado", "Status",
                  "Arquivo_Origem"]
    ws.append(cabecalhos)
    cat, cid, pais = tamanhos["DePara_Categoria"], tamanhos["DePara_Cidade"], tamanhos["DePara_Pais"]

    def data(ref):
        return (f'IF(ISNUMBER({ref}),{ref},IF(MID({ref},5,1)="-",'
                f'DATE(VALUE(LEFT({ref},4)),VALUE(MID({ref},6,2)),VALUE(RIGHT({ref},2))),'
                f'DATE(VALUE(RIGHT({ref},4)),VALUE(MID({ref},4,2)),VALUE(LEFT({ref},2)))))')

    def numero(ref):
        return (f'IF(ISNUMBER({ref}),{ref},'
                f'IFERROR(_xlfn.NUMBERVALUE(TRIM(SUBSTITUTE({ref},"R$","")),",","."),0))')

    for r in range(2, ultima_bruta + 1):
        b = f"Base_Bruta!{{}}{r}"
        vazio = f'IF($A{r}="","",'
        formulas = [
            f'=IF({b.format("A")}="","",{b.format("A")})',
            f'={vazio}{data(b.format("B"))})',
            f'={vazio}{data(b.format("C"))})',
            f'={vazio}TRIM({b.format("D")}))',
            f'={vazio}{lookup(f"LOWER(TRIM({b.format(chr(69))}))", "DePara_Categoria", cat)})',
            f'={vazio}{lookup(f"LOWER(TRIM({b.format(chr(70))}))", "DePara_Cidade", cid)})',
            f'={vazio}TRIM({b.format("G")}))',
            f'={vazio}{numero(b.format("H"))})',
            f'={vazio}{numero(b.format("I"))})',
            f'={vazio}H{r}*I{r})',
            f'={vazio}TRIM({b.format("J")}))',
            f'={vazio}TRIM({b.format("K")}))',
            f'={vazio}{lookup(f"LOWER(TRIM({b.format(chr(76))}))", "DePara_Cidade", cid)})',
            f'={vazio}UPPER(TRIM({b.format("M")})))',
            f'={vazio}{lookup(f"LOWER(TRIM({b.format(chr(78))}))", "DePara_Pais", pais)})',
            f'={vazio}IF(O{r}<>"Brasil","Turista Internacional",IF(M{r}=F{r},"Local","Turista Nacional")))',
            f'={vazio}DATE(YEAR(B{r}),MONTH(B{r}),1))',
            f'={vazio}IF(COUNTIF($A$2:$A{r},$A{r})>1,"Sim","Não"))',
            f'=IF(A{r}="","Descartar - Linha vazia",IF(R{r}="Sim","Descartar - Duplicado",'
            f'IF(OR(H{r}<=0,I{r}<=0),"Descartar - Qtd/Valor inválido","OK")))',
            f'={b.format("P")}',
        ]
        ws.append(formulas)
        for coluna, formato in ((2, "dd/mm/yyyy"), (3, "dd/mm/yyyy"), (9, MOEDA), (10, MOEDA), (17, "mmm/yyyy")):
            ws.cell(r, coluna).number_format = formato
    estilizar_cabecalho(ws)
    larguras(ws, [12, 12, 12, 30, 11, 16, 12, 6, 13, 14, 11, 12, 16, 8, 11, 20, 11, 10, 28, 16])
    ws.freeze_panes = "B2"
    adicionar_tabela(ws, "tbVendasTratadas", ultima_bruta, len(cabecalhos))
    ws["P1"].comment = Comment("Local = cidade do comprador igual à cidade-sede do evento. "
                               "Turista Nacional = outra cidade do Brasil. Turista Internacional = país diferente "
                               "do Brasil.", "IngressoData")
    ws["S1"].comment = Comment("Só linhas com Status = OK entram nos indicadores.", "IngressoData")
    return ws.max_row


def aba_auditoria(wb, ultima):
    ws = wb.create_sheet("Auditoria", 3)
    t = "Tratamento"
    linhas = [
        ("Indicador de qualidade", "Valor", "Como é calculado"),
        ("Linhas na base bruta", f"=COUNTA({t}!T2:T{ultima})", "Todas as linhas empilhadas (inclui vazias)"),
        ("Linhas vazias", f'=COUNTIF({t}!S2:S{ultima},"Descartar - Linha vazia")', "ID_Venda em branco"),
        ("Linhas duplicadas", f'=COUNTIF({t}!S2:S{ultima},"Descartar - Duplicado")', "Mesmo ID_Venda já apareceu antes"),
        ("Qtd ou valor inválido", f'=COUNTIF({t}!S2:S{ultima},"Descartar - Qtd/Valor inválido")', "Qtd ou valor vazio/zero"),
        ("Linhas válidas (OK)", f'=COUNTIF({t}!S2:S{ultima},"OK")', "Entram nos indicadores"),
        ("Conferência (bruta = descartes + OK)", "=IF(B2=SUM(B3:B6),\"OK\",\"DIVERGENTE\")", "Nenhuma linha some sem explicação"),
        ("Valores sem De-Para (REVISAR)", f'=COUNTIF({t}!E2:O{ultima},"REVISAR")', "Tem que ser 0"),
        ("Células com erro de fórmula", f"=SUMPRODUCT(--ISERROR({t}!A2:T{ultima}))", "Tem que ser 0"),
        ("Status geral", '=IF(AND(B7="OK",B8=0,B9=0),"APROVADO","REVISAR")', "Planilha sem erros e sem perdas"),
    ]
    for linha in linhas:
        ws.append(list(linha))
    estilizar_cabecalho(ws)
    larguras(ws, [38, 16, 52])
    ws["B10"].font = Font(name=FONTE, bold=True, color=VERMELHO)


def aba_resumo(wb, ultima):
    ws = wb.create_sheet("Resumo_KPIs", 4)
    t = "Tratamento"
    ok = f'{t}!$S$2:$S${ultima},"OK"'
    fat, qtd = f"{t}!$J$2:$J${ultima}", f"{t}!$H$2:$H${ultima}"
    ws["A1"] = "IngressoData Brasil — Indicadores (somente linhas com Status OK)"
    ws["A1"].font = Font(name=FONTE, bold=True, size=14, color=AZUL_ESCURO)
    ws.append([])
    ws.append(["Categoria", "Faturamento", "Ingressos", "Ticket Médio", "Faturamento Turista",
               "% Faturamento Turista", "Participação no Faturamento"])
    for indice, categoria in enumerate(["Festival", "Show", "Cinema"], start=4):
        filtro = f'{t}!$E$2:$E${ultima},$A{indice}'
        ws.append([
            categoria,
            f"=SUMIFS({fat},{filtro},{ok})",
            f"=SUMIFS({qtd},{filtro},{ok})",
            f"=IF(C{indice}=0,0,B{indice}/C{indice})",
            f'=SUMIFS({fat},{filtro},{ok},{t}!$P$2:$P${ultima},"<>Local")',
            f"=IF(B{indice}=0,0,E{indice}/B{indice})",
            f"=IF($B$7=0,0,B{indice}/$B$7)",
        ])
    ws.append(["Total", "=SUM(B4:B6)", "=SUM(C4:C6)", "=IF(C7=0,0,B7/C7)", "=SUM(E4:E6)",
               "=IF(B7=0,0,E7/B7)", "=SUM(G4:G6)"])
    estilizar_cabecalho(ws, 3)

    ws["A10"] = "Faturamento por praça e origem do público"
    ws["A10"].font = Font(name=FONTE, bold=True, size=12, color=AZUL_ESCURO)
    ws.append(["Praça", "Local", "Turista Nacional", "Turista Internacional", "Total", "% Turista"])
    for indice, praca in enumerate(["São Paulo", "Rio de Janeiro", "Belo Horizonte"], start=12):
        celulas = [praca]
        for coluna in "BCD":
            celulas.append(f'=SUMIFS({fat},{t}!$F$2:$F${ultima},$A{indice},{t}!$P$2:$P${ultima},{coluna}$11,{ok})')
        celulas += [f"=SUM(B{indice}:D{indice})", f"=IF(E{indice}=0,0,(C{indice}+D{indice})/E{indice})"]
        ws.append(celulas)
    ws.append(["Total", "=SUM(B12:B14)", "=SUM(C12:C14)", "=SUM(D12:D14)", "=SUM(E12:E14)",
               "=IF(E15=0,0,(C15+D15)/E15)"])
    estilizar_cabecalho(ws, 11)

    ws["A18"] = "Indicadores gerais"
    ws["A18"].font = Font(name=FONTE, bold=True, size=12, color=AZUL_ESCURO)
    ws.append(["Indicador", "Valor"])
    gerais = [
        ("Faturamento total", "=B7", MOEDA),
        ("Ingressos vendidos", "=C7", "#,##0"),
        ("Pedidos válidos", f"=COUNTIF({t}!$S$2:$S${ultima},\"OK\")", "#,##0"),
        ("Ticket médio por ingresso", "=D7", MOEDA),
        ("Ticket médio por pedido", "=IF(B22=0,0,B20/B22)", MOEDA),
        ("% do faturamento vindo de turistas", "=F7", PERCENTUAL),
    ]
    for rotulo, formula, formato in gerais:
        ws.append([rotulo, formula])
        ws.cell(ws.max_row, 2).number_format = formato
    estilizar_cabecalho(ws, 19)

    for linha in range(4, 8):
        for coluna, formato in zip("BCDEFG", [MOEDA, "#,##0", MOEDA, MOEDA, PERCENTUAL, PERCENTUAL]):
            ws[f"{coluna}{linha}"].number_format = formato
    for linha in range(12, 16):
        for coluna in "BCDE":
            ws[f"{coluna}{linha}"].number_format = MOEDA
        ws[f"F{linha}"].number_format = PERCENTUAL
    for linha in (7, 15):
        for celula in ws[linha]:
            celula.font = Font(name=FONTE, bold=True)
            celula.border = Border(top=FINO)
    larguras(ws, [36, 18, 18, 22, 20, 20, 24])

    grafico = BarChart()
    grafico.type, grafico.grouping, grafico.overlap = "col", "stacked", 100
    grafico.title = "Faturamento por praça e origem do público"
    grafico.y_axis.title = "R$"
    grafico.add_data(Reference(ws, min_col=2, max_col=4, min_row=11, max_row=14), titles_from_data=True)
    grafico.set_categories(Reference(ws, min_col=1, min_row=12, max_row=14))
    grafico.height, grafico.width = 8, 16
    ws.add_chart(grafico, "I3")

    pizza = PieChart()
    pizza.title = "Participação no faturamento por categoria"
    pizza.add_data(Reference(ws, min_col=2, min_row=3, max_row=6), titles_from_data=True)
    pizza.set_categories(Reference(ws, min_col=1, min_row=4, max_row=6))
    pizza.height, pizza.width = 8, 12
    ws.add_chart(pizza, "I21")


def aba_leia_me(wb):
    ws = wb.active
    ws.title = "Leia_me"
    textos = [
        ("IngressoData Brasil — Etapa 1: Excel Avançado", True),
        ("Microinformática Aplicada (ILP590) — FATEC SP — Prof. Veríssimo — 2º/2026", False),
        ("", False),
        ("Fluxo da planilha", True),
        ("1. Base_Bruta: as 3 planilhas de vendas (SP, RJ e MG) empilhadas sem nenhum tratamento.", False),
        ("2. DePara_*: tabelas de padronização (células amarelas = entrada; podem ser editadas).", False),
        ("3. Tratamento: cada coluna é uma fórmula que limpa a Base_Bruta (PROCX, ARRUMAR, VALORNUMERO, DATA).", False),
        ("4. Auditoria: confere que nenhuma linha some e que não há erros de fórmula.", False),
        ("5. Resumo_KPIs: faturamento, ticket médio e % de público turista (SOMASES).", False),
        ("", False),
        ("Problemas de qualidade tratados", True),
        ("• Datas em 3 formatos: dd/mm/aaaa (texto, SP), data do Excel (RJ) e aaaa-mm-dd (texto, MG).", False),
        ("• Valores como texto \"R$ 1.250,00\" (SP) e \"450,00\" (MG) convertidos com VALORNUMERO.", False),
        ("• Categorias com grafias diferentes (SHOW, Shows, Fest., Cine...) padronizadas via PROCX no De-Para.", False),
        ("• Cidades sem acento, em maiúsculas, siglas (BH, SP - São Paulo) e espaços sobrando.", False),
        ("• Linhas duplicadas (mesmo ID_Venda), linhas vazias e quantidade/valor faltando.", False),
        ("", False),
        ("Regra de público turista", True),
        ("Local = mora na cidade-sede do evento. Turista Nacional = outra cidade do Brasil. "
         "Turista Internacional = mora fora do Brasil.", False),
        ("", False),
        ("Dados 100% simulados (gerador com seed fixa em 04-documentacao/scripts). Eventos e nomes são fictícios.", False),
    ]
    for texto, negrito in textos:
        ws.append([texto])
        ws.cell(ws.max_row, 1).font = Font(name=FONTE, bold=negrito, size=13 if negrito else 11,
                                          color=AZUL_ESCURO if negrito else "000000")
    ws.column_dimensions["A"].width = 120


def main(pasta_brutos, destino):
    wb = openpyxl.Workbook()
    aba_leia_me(wb)
    linhas = ler_brutos(pasta_brutos)
    ultima_bruta = aba_base_bruta(wb, linhas)
    tamanhos = aba_de_para(wb, pasta_brutos)
    ultima = aba_tratamento(wb, ultima_bruta, tamanhos)
    aba_auditoria(wb, ultima)
    aba_resumo(wb, ultima)
    for ws in wb.worksheets:
        fonte_padrao(ws)
    wb.calculation.fullCalcOnLoad = True
    wb.save(destino)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
