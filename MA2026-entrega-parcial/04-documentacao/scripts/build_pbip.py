"""Gera o projeto Power BI (PBIP: modelo em TMDL + relatório em PBIR) do dashboard IngressoData.

Uso:  python build_pbip.py <raiz do repositório>
Saída: MA2026-entrega-final/04-powerbi-dashboard/IngressoData_Dashboard.pbip (+ pastas .Report e .SemanticModel)

As consultas M são lidas dos próprios arquivos .pq do projeto. A consulta Fato_Vendas_Ingressos da entrega
parcial vira a expressão Vendas_Base e a tabela carregada Fato_Vendas_Ingressos é a versão enriquecida com
câmbio e clima (04_Fato_Vendas_Enriquecida.pq), para as medidas de medidas.dax funcionarem sem mudança.
Abrir o .pbip no Power BI Desktop, Atualizar, e Arquivo > Salvar como > .pbix."""
import json
import re
import shutil
import sys
import uuid
from pathlib import Path

RAIZ = Path(sys.argv[1]).resolve()
PQ = RAIZ / "MA2026-entrega-parcial" / "02-powerquery"
API = RAIZ / "MA2026-entrega-final" / "03-api-web"
DESTINO = RAIZ / "MA2026-entrega-final" / "04-powerbi-dashboard"
NOME = "IngressoData_Dashboard"
FATO = "Fato_Vendas_Ingressos"
SCHEMA = "https://developer.microsoft.com/json-schemas/fabric"


def guid(semente):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"ingressodata/{semente}"))


def ler_pq(caminho):
    texto = caminho.read_text(encoding="utf-8").strip()
    return re.sub(r"\bFato_Vendas_Ingressos\b", "Vendas_Base", texto)


def indentar(texto, nivel):
    return "\n".join(("\t" * nivel + linha) if linha.strip() else "" for linha in texto.splitlines())


# ---------------------------------------------------------------- consultas M
pasta_dados = str(RAIZ / "MA2026-entrega-parcial" / "01-excel" / "dados-brutos") + "\\"
EXPRESSOES = {  # nome -> (M, tipo do resultado)
    "pPastaDados": (f'"{pasta_dados}" meta [IsParameterQuery = true, Type = "Text", IsParameterQueryRequired = true]',
                    "Text"),
    "fnTratarData": (ler_pq(PQ / "01_fnTratarData.pq"), "Function"),
    "fnTratarNumero": (ler_pq(PQ / "02_fnTratarNumero.pq"), "Function"),
    "fnLerAba": (ler_pq(PQ / "03_fnLerAba.pq"), "Function"),
    "DePara_Categoria": (ler_pq(PQ / "04_DePara_Categoria.pq"), "Table"),
    "DePara_Cidade": (ler_pq(PQ / "04_DePara_Cidade.pq"), "Table"),
    "DePara_Pais": (ler_pq(PQ / "04_DePara_Pais.pq"), "Table"),
    "Vendas_MG": (ler_pq(PQ / "05_Vendas_MG.pq"), "Table"),
    "Vendas_RJ": (ler_pq(PQ / "05_Vendas_RJ.pq"), "Table"),
    "Vendas_SP": (ler_pq(PQ / "05_Vendas_SP.pq"), "Table"),
    "Vendas_Base": (ler_pq(PQ / "06_Fato_Vendas_Ingressos.pq"), "Table"),
    "Dim_Cambio_BCB": (ler_pq(API / "01_Dim_Cambio_BCB.pq"), "Table"),
    "fnClimaPraca": (ler_pq(API / "02_fnClimaPraca.pq"), "Function"),
    "Fato_Clima": (ler_pq(API / "03_Fato_Clima.pq"), "Table"),
    "Web_Visitantes_Pais": (ler_pq(PQ / "08_Web_Visitantes_Pais.pq"), "Table"),
}

S, I64, DEC, DBL, DT = "string", "int64", "decimal", "double", "dateTime"
MOEDA, PCT, INTEIRO, DATA = r"\R$ #,0.00", "0.0%", "#,0", "dd/mm/yyyy"
TABELAS = {  # nome -> (arquivo M, colunas [(nome, tipo, formato)])
    FATO: (API / "04_Fato_Vendas_Enriquecida.pq", [
        ("ID_Venda", S, None), ("Data_Venda", DT, DATA), ("Data_Evento", DT, DATA), ("Evento", S, None),
        ("Categoria", S, None), ("Cidade_Evento", S, None), ("Tipo_Ingresso", S, None), ("Qtd", I64, INTEIRO),
        ("Valor_Unitario", DEC, MOEDA), ("Valor_Total", DEC, MOEDA), ("Canal", S, None), ("Comprador_ID", S, None),
        ("Cidade_Comprador", S, None), ("UF_Comprador", S, None), ("Pais_Comprador", S, None),
        ("Origem_Publico", S, None), ("Arquivo_Origem", S, None), ("Dolar_no_Dia_da_Venda", DBL, "0.0000"),
        ("Chave_Cidade_Data", S, None), ("Temp_Max_no_Evento", DBL, "0.0"), ("Chuva_mm_no_Evento", DBL, "0.0"),
        ("Condicao_no_Evento", S, None)]),
    "Dim_Evento": (PQ / "07_Dim_Evento.pq", [
        ("Evento", S, None), ("Categoria", S, None), ("Cidade_Evento", S, None), ("Local", S, None),
        ("Ao_Ar_Livre", S, None), ("Data_Evento", DT, DATA)]),
    "Dim_Praca": (PQ / "07_Dim_Praca.pq", [
        ("Cidade", S, None), ("UF", S, None), ("Regiao", S, None), ("Latitude", DBL, None),
        ("Longitude", DBL, None)]),
    "Dim_Comprador": (PQ / "07_Dim_Comprador.pq", [
        ("Comprador_ID", S, None), ("Cidade_Comprador", S, None), ("UF_Comprador", S, None),
        ("Pais_Comprador", S, None), ("Tipo_Comprador", S, None)]),
    "Dim_Calendario": (PQ / "07_Dim_Calendario.pq", [
        ("Data", DT, DATA), ("Ano", I64, "0"), ("Mes", I64, "0"), ("Nome_Mes", S, None), ("Ano_Mes", S, None),
        ("Trimestre", S, None), ("Dia_Semana", S, None), ("Fim_de_Semana", S, None)]),
    "Fato_Visitantes_Internacionais": (PQ / "09_Fato_Visitantes_Internacionais.pq", [
        ("Pais", S, None), ("Pais_Original", S, None), ("Ano", I64, "0"), ("Visitantes", I64, INTEIRO),
        ("Pais_Na_Base_de_Vendas", S, None)]),
}

MEDIDAS = [  # (nome, DAX, formato) — as 14 primeiras são as de 03-powerpivot/medidas.dax
    ("Faturamento Total", "SUM ( Fato_Vendas_Ingressos[Valor_Total] )", MOEDA),
    ("Ingressos Vendidos", "SUM ( Fato_Vendas_Ingressos[Qtd] )", INTEIRO),
    ("Pedidos", "DISTINCTCOUNT ( Fato_Vendas_Ingressos[ID_Venda] )", INTEIRO),
    ("Ticket Médio", "DIVIDE ( [Faturamento Total], [Ingressos Vendidos] )", MOEDA),
    ("Ticket Médio por Pedido", "DIVIDE ( [Faturamento Total], [Pedidos] )", MOEDA),
    ("Faturamento Turista", 'CALCULATE ( [Faturamento Total], Fato_Vendas_Ingressos[Origem_Publico] <> "Local" )', MOEDA),
    ("% Faturamento Turista", "DIVIDE ( [Faturamento Turista], [Faturamento Total] )", PCT),
    ("Compradores", "DISTINCTCOUNT ( Fato_Vendas_Ingressos[Comprador_ID] )", INTEIRO),
    ("Compradores Turistas", 'CALCULATE ( [Compradores], Fato_Vendas_Ingressos[Origem_Publico] <> "Local" )', INTEIRO),
    ("% Compradores Turistas", "DIVIDE ( [Compradores Turistas], [Compradores] )", PCT),
    ("Participação Categoria", "DIVIDE ( [Faturamento Total], CALCULATE ( [Faturamento Total], "
                               "ALL ( Fato_Vendas_Ingressos[Categoria] ), ALL ( Dim_Evento[Categoria] ) ) )", PCT),
    ("Faturamento Ao Ar Livre", 'CALCULATE ( [Faturamento Total], Dim_Evento[Ao_Ar_Livre] = "Sim" )', MOEDA),
    ("Faturamento Mês Anterior", "CALCULATE ( [Faturamento Total], DATEADD ( Dim_Calendario[Data], -1, MONTH ) )",
     MOEDA),
    ("Variação Mensal %", "DIVIDE ( [Faturamento Total] - [Faturamento Mês Anterior], [Faturamento Mês Anterior] )",
     PCT),
    ("Dólar Médio", "AVERAGE ( Fato_Vendas_Ingressos[Dolar_no_Dia_da_Venda] )", "0.00"),
    ("Ingressos Turista Internacional",
     'CALCULATE ( [Ingressos Vendidos], Fato_Vendas_Ingressos[Origem_Publico] = "Turista Internacional" )', INTEIRO),
    ("Visitantes Internacionais", "SUM ( Fato_Visitantes_Internacionais[Visitantes] )", INTEIRO),
]

RELACOES = [("Evento", "Dim_Evento", "Evento"), ("Cidade_Evento", "Dim_Praca", "Cidade"),
            ("Comprador_ID", "Dim_Comprador", "Comprador_ID"), ("Data_Venda", "Dim_Calendario", "Data")]


def nome_tmdl(nome):
    return nome if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", nome) else "'" + nome.replace("'", "''") + "'"


def tabela_tmdl(nome, arquivo, colunas):
    linhas = [f"table {nome_tmdl(nome)}", f"\tlineageTag: {guid(nome)}", ""]
    if nome == "Dim_Calendario":
        linhas[1:1] = ["\tdataCategory: Time"]
    if nome == FATO:
        for medida, dax, formato in MEDIDAS:
            linhas += [f"\tmeasure {nome_tmdl(medida)} = {dax}", f"\t\tformatString: {formato}",
                       f"\t\tlineageTag: {guid(nome + '/m/' + medida)}", ""]
    for coluna, tipo, formato in colunas:
        linhas += [f"\tcolumn {nome_tmdl(coluna)}", f"\t\tdataType: {tipo}"]
        if formato:
            linhas.append(f"\t\tformatString: {formato}")
        if nome == "Dim_Calendario" and coluna == "Data":
            linhas.append("\t\tisKey")
        if coluna in ("Latitude", "Longitude"):
            linhas.append(f"\t\tdataCategory: {coluna}")
        resumo = "sum" if (tipo in (I64, DEC, DBL) and coluna not in ("Ano", "Mes", "Latitude", "Longitude")
                           and not coluna.startswith(("Dolar", "Temp", "Chuva"))) else "none"
        linhas += [f"\t\tlineageTag: {guid(nome + '/c/' + coluna)}", f"\t\tsummarizeBy: {resumo}",
                   f"\t\tsourceColumn: {coluna}", ""]
    m = ler_pq(arquivo)
    linhas += [f"\tpartition {nome_tmdl(nome)} = m", "\t\tmode: import", "\t\tsource =", indentar(m, 3), "",
               "\tannotation PBI_ResultType = Table", ""]
    return "\n".join(linhas)


def expressoes_tmdl():
    blocos = []
    for nome, (m, tipo) in EXPRESSOES.items():
        if "\n" in m:
            cabecalho = [f"expression {nome} =", indentar(m, 2)]
        else:
            cabecalho = [f"expression {nome} = {m}"]
        blocos.append("\n".join(cabecalho + [f"\tlineageTag: {guid('e/' + nome)}", "",
                                             f"\tannotation PBI_ResultType = {tipo}", ""]))
    return "\n".join(blocos)


def escrever(caminho, conteudo):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    if not isinstance(conteudo, str):
        conteudo = json.dumps(conteudo, ensure_ascii=False, indent=2)
    caminho.write_text(conteudo, encoding="utf-8")


# ---------------------------------------------------------------- relatório (PBIR)
def campo(entidade, propriedade, medida=False):
    tipo = "Measure" if medida else "Column"
    return {tipo: {"Expression": {"SourceRef": {"Entity": entidade}}, "Property": propriedade}}


def proj(entidade, propriedade, medida=False):
    return {"field": campo(entidade, propriedade, medida), "queryRef": f"{entidade}.{propriedade}",
            "nativeQueryRef": propriedade}


def M(nome):
    return proj(FATO, nome, medida=True)


def literal(valor):
    return {"expr": {"Literal": {"Value": valor}}}


def visual(nome, tipo, x, y, w, h, papeis, titulo=None, ordem=None, extras=None):
    corpo = {"visualType": tipo, "query": {"queryState": {
        papel: {"projections": lista} for papel, lista in papeis.items()}}, "drillFilterOtherVisuals": True}
    if ordem:
        corpo["query"]["sortDefinition"] = {"sort": [{"field": ordem[0], "direction": ordem[1]}],
                                            "isDefaultSort": True}
    if extras:
        corpo["objects"] = extras
    container = {"$schema": f"{SCHEMA}/item/report/definition/visualContainer/2.4.0/schema.json", "name": nome,
                 "position": {"x": x, "y": y, "z": 0, "height": h, "width": w, "tabOrder": 0}, "visual": corpo}
    if titulo:
        corpo["visualContainerObjects"] = {"title": [{"properties": {
            "show": literal("true"), "text": literal("'" + titulo.replace("'", "''") + "'")}}]}
    return container


def slicer(nome, x, y, w, h, entidade, coluna, titulo, modo="Dropdown"):
    return visual(nome, "slicer", x, y, w, h, {"Values": [proj(entidade, coluna)]}, titulo,
                  extras={"data": [{"properties": {"mode": literal(f"'{modo}'")}}]})


ORIGEM = proj(FATO, "Origem_Publico")
ANO_MES = proj("Dim_Calendario", "Ano_Mes")
PAGINAS = [
    ("visao_geral", "Visão Geral", [
        slicer("s_categoria", 20, 110, 260, 90, "Dim_Evento", "Categoria", "Categoria"),
        slicer("s_praca", 20, 220, 260, 90, "Dim_Praca", "Cidade", "Praça"),
        slicer("s_periodo", 20, 330, 260, 120, "Dim_Calendario", "Data", "Período", "Between"),
        visual("c_fat", "card", 300, 20, 390, 150, {"Values": [M("Faturamento Total")]}, "Faturamento Total"),
        visual("c_ing", "card", 705, 20, 390, 150, {"Values": [M("Ingressos Vendidos")]}, "Ingressos Vendidos"),
        visual("c_tm", "card", 1110, 20, 390, 150, {"Values": [M("Ticket Médio")]}, "Ticket Médio"),
        visual("c_tur", "card", 1515, 20, 385, 150, {"Values": [M("% Faturamento Turista")]},
               "% do faturamento vindo de turistas"),
        visual("g_cat_origem", "columnChart", 300, 190, 800, 870,
               {"Category": [proj("Dim_Evento", "Categoria")], "Y": [M("Faturamento Total")], "Series": [ORIGEM]},
               "Festivais concentram a receita e o público turista"),
        visual("g_mes", "lineChart", 1115, 190, 785, 870,
               {"Category": [ANO_MES], "Y": [M("Faturamento Total")]}, "Faturamento por mês",
               ordem=(campo("Dim_Calendario", "Ano_Mes"), "Ascending")),
    ]),
    ("publico_turista", "Público Turista", [
        visual("g_evento_origem", "hundredPercentStackedBarChart", 20, 20, 940, 620,
               {"Category": [proj("Dim_Evento", "Evento")], "Y": [M("Faturamento Total")], "Series": [ORIGEM]},
               "Participação de cada público no faturamento por evento"),
        visual("t_eventos", "tableEx", 980, 20, 920, 620,
               {"Values": [proj("Dim_Evento", "Evento"), M("Faturamento Total"), M("% Faturamento Turista"),
                           M("% Compradores Turistas")]}, "Eventos: faturamento e peso do turista",
               ordem=(campo(FATO, "Faturamento Total", True), "Descending")),
        visual("g_tipo_comprador", "donutChart", 20, 660, 620, 400,
               {"Category": [proj("Dim_Comprador", "Tipo_Comprador")], "Y": [M("Compradores")]},
               "Compradores nacionais x estrangeiros"),
        visual("g_visitantes", "barChart", 660, 660, 1240, 400,
               {"Category": [proj("Fato_Visitantes_Internacionais", "Pais")],
                "Y": [M("Visitantes Internacionais")]},
               "Visitantes internacionais no Brasil por país (fonte: web)",
               ordem=(campo(FATO, "Visitantes Internacionais", True), "Descending")),
    ]),
    ("fatores_externos", "Fatores Externos", [
        visual("g_dolar", "lineClusteredColumnComboChart", 20, 20, 1880, 520,
               {"Category": [ANO_MES], "Y": [M("Ingressos Vendidos")], "Y2": [M("Dólar Médio")]},
               "Ingressos vendidos x dólar médio no dia da venda",
               ordem=(campo("Dim_Calendario", "Ano_Mes"), "Ascending")),
        visual("g_int_mes", "lineChart", 20, 560, 900, 500,
               {"Category": [ANO_MES], "Y": [M("Ingressos Turista Internacional")]},
               "Ingressos de turistas internacionais por mês",
               ordem=(campo("Dim_Calendario", "Ano_Mes"), "Ascending")),
        visual("g_clima", "clusteredColumnChart", 940, 560, 620, 500,
               {"Category": [proj(FATO, "Condicao_no_Evento")], "Y": [M("Ingressos Vendidos")]},
               "Ingressos por condição do tempo no dia do evento"),
        visual("c_ar_livre", "card", 1580, 560, 320, 500, {"Values": [M("Faturamento Ao Ar Livre")]},
               "Faturamento em eventos ao ar livre"),
    ]),
]
# o gráfico de clima considera só eventos ao ar livre
PAGINAS[2][2][2]["filterConfig"] = {"filters": [{
    "name": "f_ar_livre", "field": campo("Dim_Evento", "Ao_Ar_Livre"), "type": "Categorical",
    "filter": {"Version": 2, "From": [{"Name": "d", "Entity": "Dim_Evento", "Type": 0}],
               "Where": [{"Condition": {"In": {
                   "Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "Ao_Ar_Livre"}}],
                   "Values": [[{"Literal": {"Value": "'Sim'"}}]]}}}]}}]}


def main():
    esqueleto = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    rel, sm = DESTINO / f"{NOME}.Report", DESTINO / f"{NOME}.SemanticModel"
    for pasta in (rel, sm):
        if pasta.exists():
            shutil.rmtree(pasta)

    # ---- modelo
    d = sm / "definition"
    escrever(sm / "definition.pbism", {"version": "4.2", "settings": {}})
    escrever(sm / ".platform", {"$schema": f"{SCHEMA}/gitIntegration/platformProperties/2.0.0/schema.json",
                                "metadata": {"type": "SemanticModel", "displayName": NOME},
                                "config": {"version": "2.0", "logicalId": guid("sm")}})
    escrever(d / "database.tmdl", "database\n\tcompatibilityLevel: 1606\n")
    escrever(d / "cultures" / "pt-BR.tmdl", "cultureInfo pt-BR\n")
    refs = "\n".join(f"ref table {nome_tmdl(t)}" for t in TABELAS)
    escrever(d / "model.tmdl", (
        "model Model\n\tculture: pt-BR\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n"
        "\tsourceQueryCulture: pt-BR\n\tvalueFilterBehavior: independent\n\tdataAccessOptions\n"
        "\t\tlegacyRedirects\n\t\treturnErrorValuesAsNull\n\n"
        "annotation __PBI_TimeIntelligenceEnabled = 0\n\n"
        f"{refs}\n\nref cultureInfo pt-BR\n"))
    escrever(d / "expressions.tmdl", expressoes_tmdl())
    for nome, (arquivo, colunas) in TABELAS.items():
        escrever(d / "tables" / f"{nome}.tmdl", tabela_tmdl(nome, arquivo, colunas))
    escrever(d / "relationships.tmdl", "\n".join(
        f"relationship {guid('r/' + coluna)}\n\tfromColumn: {FATO}.{coluna}\n\ttoColumn: {dim}.{chave}\n"
        for coluna, dim, chave in RELACOES))

    # ---- relatório
    d = rel / "definition"
    escrever(rel / "definition.pbir", {"version": "4.0",
                                       "datasetReference": {"byPath": {"path": f"../{NOME}.SemanticModel"}}})
    escrever(rel / ".platform", {"$schema": f"{SCHEMA}/gitIntegration/platformProperties/2.0.0/schema.json",
                                 "metadata": {"type": "Report", "displayName": NOME},
                                 "config": {"version": "2.0", "logicalId": guid("rel")}})
    escrever(d / "version.json", {"$schema": f"{SCHEMA}/item/report/definition/versionMetadata/1.0.0/schema.json",
                                  "version": "2.0.0"})
    base = "Fluent2-CY26SU10"
    if esqueleto:
        origem = next(esqueleto.glob(f"*.Report/StaticResources/SharedResources/BaseThemes/{base}.json"))
        destino_tema = rel / "StaticResources" / "SharedResources" / "BaseThemes" / f"{base}.json"
        destino_tema.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(origem, destino_tema)
    tema = DESTINO / "IngressoData_tema.json"
    (rel / "StaticResources" / "RegisteredResources").mkdir(parents=True, exist_ok=True)
    shutil.copy(tema, rel / "StaticResources" / "RegisteredResources" / tema.name)
    escrever(d / "report.json", {
        "$schema": f"{SCHEMA}/item/report/definition/report/3.3.0/schema.json",
        "themeCollection": {
            "baseTheme": {"name": base, "reportVersionAtImport": {"visual": "2.14.0", "report": "3.4.0",
                                                                  "page": "2.3.1"}, "type": "SharedResources"},
            "customTheme": {"name": tema.name, "reportVersionAtImport": {"visual": "2.14.0", "report": "3.4.0",
                                                                         "page": "2.3.1"},
                            "type": "RegisteredResources"}},
        "resourcePackages": [
            {"name": "SharedResources", "type": "SharedResources",
             "items": [{"name": base, "path": f"BaseThemes/{base}.json", "type": "BaseTheme"}]},
            {"name": "RegisteredResources", "type": "RegisteredResources",
             "items": [{"name": tema.name, "path": tema.name, "type": "CustomTheme"}]}],
        "settings": {"useStylableVisualContainerHeader": True, "exportDataMode": "AllowSummarized",
                     "defaultDrillFilterOtherVisuals": True, "allowChangeFilterTypes": True,
                     "useEnhancedTooltips": True, "useDefaultAggregateDisplayName": True}})
    escrever(d / "pages" / "pages.json", {
        "$schema": f"{SCHEMA}/item/report/definition/pagesMetadata/1.1.0/schema.json",
        "pageOrder": [p[0] for p in PAGINAS], "activePageName": PAGINAS[0][0]})
    for nome, titulo, visuais in PAGINAS:
        escrever(d / "pages" / nome / "page.json", {
            "$schema": f"{SCHEMA}/item/report/definition/page/2.1.0/schema.json", "name": nome,
            "displayName": titulo, "displayOption": "FitToPage", "height": 1080, "width": 1920})
        for v in visuais:
            escrever(d / "pages" / nome / "visuals" / v["name"] / "visual.json", v)

    escrever(DESTINO / f"{NOME}.pbip", {"version": "1.0", "artifacts": [{"report": {"path": f"{NOME}.Report"}}],
                                        "settings": {"enableAutoRecovery": True}})
    escrever(DESTINO / ".gitignore", "**/.pbi/localSettings.json\n**/.pbi/cache.abf\n")
    print("PBIP gerado em", DESTINO)


if __name__ == "__main__":
    main()
