"""Troca IFERROR(INDEX(..MATCH..)) por XLOOKUP (PROCX no Excel pt-BR) direto no XML.

O LibreOffice usado para validar não calcula PROCX, então a planilha é calculada e auditada
com INDEX/CORRESP e só depois as fórmulas viram PROCX. As duas formas são equivalentes para
busca exata com valor padrão; os valores já calculados ficam no arquivo e o Excel recalcula
tudo ao abrir (fullCalcOnLoad)."""
import re
import sys
import zipfile

PADRAO = re.compile(
    r"IFERROR\(INDEX\((\w+)!(\$B\$2:\$B\$\d+),MATCH\(([^,]+),\1!(\$A\$2:\$A\$\d+),0\)\),(&quot;REVISAR&quot;)\)")


def converter(caminho):
    with zipfile.ZipFile(caminho) as origem:
        itens = [(info, origem.read(info.filename)) for info in origem.infolist()]
    total = 0
    with zipfile.ZipFile(caminho, "w", zipfile.ZIP_DEFLATED) as destino:
        for info, conteudo in itens:
            if info.filename.startswith("xl/worksheets/sheet"):
                texto, trocas = PADRAO.subn(r"_xlfn.XLOOKUP(\3,\1!\4,\1!\2,\5)", conteudo.decode("utf-8"))
                total += trocas
                conteudo = texto.encode("utf-8")
            elif info.filename == "xl/workbook.xml":  # Excel recalcula tudo ao abrir
                conteudo = conteudo.replace(b"<calcPr ", b'<calcPr fullCalcOnLoad="1" ', 1)
            destino.writestr(info, conteudo)
    return total


if __name__ == "__main__":
    print(f"fórmulas convertidas para PROCX: {converter(sys.argv[1])}")
