Attribute VB_Name = "mdlMontarModelo"
' IngressoData Brasil - Etapa 2: monta o Modelo de Dados (Power Pivot) com um clique.
' Uso: abra IngressoData_03_PowerPivot.xlsx no Excel para Windows, Alt+F11, Arquivo > Importar Arquivo
' (este .bas), feche o editor e rode Alt+F8 > MontarModeloPowerPivot.
' O que a macro faz:
'   1. Adiciona a fato e as 4 dimensões (Tabelas do Excel) ao Modelo de Dados
'   2. Cria os 4 relacionamentos (muitos para um, fato -> dimensão)
'   3. Cria as 14 medidas DAX de medidas.dax com formato de número
'   4. Cria a aba Conferencia com uma Tabela Dinâmica do modelo para bater com o gabarito
'   5. Salva como IngressoData_03_PowerPivot.xlsm
' Depois, só falta um passo manual: Power Pivot > Gerenciar > Dim_Calendario > Design >
' Marcar como Tabela de Data (coluna Data). O Excel não expõe esse comando para o VBA.
Option Explicit

Private Const FATO As String = "Fato_Vendas_Ingressos"

Public Sub MontarModeloPowerPivot()
    Dim modelo As Model

    Set modelo = ThisWorkbook.Model
    If modelo.ModelTables.Count > 0 Then
        MsgBox "O Modelo de Dados já tem tabelas. Use uma cópia limpa de IngressoData_03_PowerPivot.xlsx.", vbExclamation
        Exit Sub
    End If

    Application.ScreenUpdating = False
    AdicionarAoModelo FATO
    AdicionarAoModelo "Dim_Evento"
    AdicionarAoModelo "Dim_Praca"
    AdicionarAoModelo "Dim_Comprador"
    AdicionarAoModelo "Dim_Calendario"

    Relacionar modelo, "Evento", "Dim_Evento", "Evento"
    Relacionar modelo, "Cidade_Evento", "Dim_Praca", "Cidade"
    Relacionar modelo, "Comprador_ID", "Dim_Comprador", "Comprador_ID"
    Relacionar modelo, "Data_Venda", "Dim_Calendario", "Data"

    CriarMedidas modelo
    CriarConferencia
    Application.ScreenUpdating = True

    Application.DisplayAlerts = False
    ThisWorkbook.SaveAs Filename:=ThisWorkbook.Path & Application.PathSeparator & "IngressoData_03_PowerPivot.xlsm", _
                        FileFormat:=xlOpenXMLWorkbookMacroEnabled
    Application.DisplayAlerts = True

    MsgBox "Modelo montado: 5 tabelas, 4 relacionamentos e " & modelo.ModelMeasures.Count & " medidas." & vbCrLf & _
           "Falta só marcar Dim_Calendario como Tabela de Data no Power Pivot." & vbCrLf & _
           "Confira a aba Conferencia: Faturamento Total = R$ 2.037.612,50.", vbInformation
End Sub

' Mesmo comando que o Excel grava em "Power Pivot > Adicionar ao Modelo de Dados"
Private Sub AdicionarAoModelo(nomeTabela As String)
    ThisWorkbook.Connections.Add2 _
        Name:="WorksheetConnection_" & nomeTabela, _
        Description:="", _
        ConnectionString:="WORKSHEET;" & ThisWorkbook.FullName, _
        CommandText:=ThisWorkbook.Name & "!" & nomeTabela, _
        lCmdtype:=xlCmdExcel, _
        CreateModelConnection:=True, _
        ImportRelationships:=False
End Sub

Private Sub Relacionar(modelo As Model, colunaFato As String, dimensao As String, chave As String)
    modelo.ModelRelationships.Add _
        modelo.ModelTables(FATO).ModelTableColumns(colunaFato), _
        modelo.ModelTables(dimensao).ModelTableColumns(chave)
End Sub

Private Sub Medida(modelo As Model, nome As String, formula As String, formato As Variant)
    modelo.ModelMeasures.Add nome, modelo.ModelTables(FATO), formula, formato
End Sub

' As fórmulas são as mesmas de medidas.dax (DAX no modelo é sempre em inglês, separador vírgula)
Private Sub CriarMedidas(modelo As Model)
    Dim moeda As Variant, inteiro As Variant, percentual As Variant
    Set moeda = modelo.ModelFormatCurrency("R$", 2)
    Set inteiro = modelo.ModelFormatWholeNumber(True)
    Set percentual = modelo.ModelFormatPercentageNumber(False, 1)

    Medida modelo, "Faturamento Total", "SUM ( Fato_Vendas_Ingressos[Valor_Total] )", moeda
    Medida modelo, "Ingressos Vendidos", "SUM ( Fato_Vendas_Ingressos[Qtd] )", inteiro
    Medida modelo, "Pedidos", "DISTINCTCOUNT ( Fato_Vendas_Ingressos[ID_Venda] )", inteiro
    Medida modelo, "Ticket Médio", "DIVIDE ( [Faturamento Total], [Ingressos Vendidos] )", moeda
    Medida modelo, "Ticket Médio por Pedido", "DIVIDE ( [Faturamento Total], [Pedidos] )", moeda
    Medida modelo, "Faturamento Turista", _
        "CALCULATE ( [Faturamento Total], Fato_Vendas_Ingressos[Origem_Publico] <> ""Local"" )", moeda
    Medida modelo, "% Faturamento Turista", "DIVIDE ( [Faturamento Turista], [Faturamento Total] )", percentual
    Medida modelo, "Compradores", "DISTINCTCOUNT ( Fato_Vendas_Ingressos[Comprador_ID] )", inteiro
    Medida modelo, "Compradores Turistas", _
        "CALCULATE ( [Compradores], Fato_Vendas_Ingressos[Origem_Publico] <> ""Local"" )", inteiro
    Medida modelo, "% Compradores Turistas", "DIVIDE ( [Compradores Turistas], [Compradores] )", percentual
    Medida modelo, "Participação Categoria", _
        "DIVIDE ( [Faturamento Total], CALCULATE ( [Faturamento Total], ALL ( Fato_Vendas_Ingressos[Categoria] ), " & _
        "ALL ( Dim_Evento[Categoria] ) ) )", percentual
    Medida modelo, "Faturamento Ao Ar Livre", _
        "CALCULATE ( [Faturamento Total], Dim_Evento[Ao_Ar_Livre] = ""Sim"" )", moeda
    Medida modelo, "Faturamento Mês Anterior", _
        "CALCULATE ( [Faturamento Total], DATEADD ( Dim_Calendario[Data], -1, MONTH ) )", moeda
    Medida modelo, "Variação Mensal %", _
        "DIVIDE ( [Faturamento Total] - [Faturamento Mês Anterior], [Faturamento Mês Anterior] )", percentual
End Sub

' Tabela Dinâmica do modelo por categoria, para comparar com o gabarito.json
Private Sub CriarConferencia()
    Dim aba As Worksheet, cache As PivotCache, tabela As PivotTable, medidaNome As Variant

    Set aba = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
    aba.Name = "Conferencia"
    aba.Range("A1").Value = "Conferência do Modelo de Dados (comparar com 03-powerpivot/gabarito.json)"
    aba.Range("A1").Font.Bold = True

    Set cache = ThisWorkbook.PivotCaches.Create(SourceType:=xlExternal, _
        SourceData:=ThisWorkbook.Connections("ThisWorkbookDataModel"), Version:=6)
    Set tabela = cache.CreatePivotTable(TableDestination:=aba.Range("A3"), TableName:="ptConferencia")
    tabela.CubeFields("[Dim_Evento].[Categoria]").Orientation = xlRowField
    For Each medidaNome In Array("Faturamento Total", "Ingressos Vendidos", "Ticket Médio", _
                                 "% Faturamento Turista", "Participação Categoria")
        tabela.AddDataField tabela.CubeFields("[Measures].[" & medidaNome & "]")
    Next medidaNome
    aba.Columns("A:F").AutoFit
End Sub
