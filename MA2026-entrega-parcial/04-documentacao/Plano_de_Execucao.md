# Plano de Execução · o que falta fazer em máquina Windows

Tudo que dá para gerar fora do Excel já está pronto e testado. Estes passos exigem o Excel/Power BI para Windows.

## Entrega parcial (hoje)

- [ ] Abrir `01-excel/IngressoData_01_Excel.xlsx` e conferir a aba Auditoria = **APROVADO**
- [ ] Montar as consultas do `02-powerquery` (passo a passo no README da pasta) e salvar como `IngressoData_02_PowerQuery.xlsx` na mesma pasta
- [ ] Carregar Fato e Dims no Modelo, criar relacionamentos e colar `medidas.dax`; salvar como `IngressoData_03_PowerPivot_Modelo.xlsx` em `03-powerpivot`
- [ ] Conferir: 2.000 linhas e R$ 2.037.612,50
- [ ] Gravar o vídeo seguindo `Roteiro_Video.md` e anexar `legenda_video.srt`
- [ ] `git add . && git commit -m "Entrega parcial: Excel, Power Query e Power Pivot" && git push`

## Entrega final (próximas aulas)

- [ ] VBA: importar `mdlRelatorioVendas.bas` na planilha do 01-excel, salvar como .xlsm e rodar `RelatorioSemanal`
- [ ] SQL: rodar `01_schema.sql`, `02_carga_dados.sql`, `03_consultas.sql` (DB Browser for SQLite ou pgAdmin)
- [ ] API: colar as consultas de `03-api-web` no Power Query e atualizar
- [ ] Power BI: montar o painel conforme `04-powerbi-dashboard/Especificacao_Dashboard.md` e importar o tema
