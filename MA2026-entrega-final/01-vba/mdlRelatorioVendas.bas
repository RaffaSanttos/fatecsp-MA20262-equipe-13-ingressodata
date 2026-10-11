Attribute VB_Name = "mdlRelatorioVendas"
' IngressoData Brasil - Etapa 3: automação de relatórios de vendas (VBA)
' Lê a tabela tbVendasTratadas (aba Tratamento da IngressoData_01_Excel) e gera um relatório
' por evento e praça. Usa só recursos nativos do Excel (funciona no Windows e no Mac).
Option Explicit

Private Const NOME_TABELA As String = "tbVendasTratadas"
Private Const STATUS_VALIDO As String = "OK"

' Relatório do último dia com vendas na base
Public Sub RelatorioDiario()
    Dim ultimoDia As Date
    ultimoDia = UltimaDataDeVenda()
    MontarRelatorio ultimoDia, ultimoDia, "Diário"
End Sub

' Relatório dos 7 dias que terminam no último dia com vendas
Public Sub RelatorioSemanal()
    Dim ultimoDia As Date
    ultimoDia = UltimaDataDeVenda()
    MontarRelatorio ultimoDia - 6, ultimoDia, "Semanal"
End Sub

' Relatório de um período escolhido pelo usuário
Public Sub RelatorioPeriodo()
    Dim textoInicio As String, textoFim As String
    textoInicio = InputBox("Data inicial (dd/mm/aaaa):", "Relatório por período")
    If textoInicio = "" Then Exit Sub
    textoFim = InputBox("Data final (dd/mm/aaaa):", "Relatório por período")
    If textoFim = "" Then Exit Sub
    If Not IsDate(textoInicio) Or Not IsDate(textoFim) Then
        MsgBox "Data inválida. Use o formato dd/mm/aaaa.", vbExclamation
        Exit Sub
    End If
    MontarRelatorio CDate(textoInicio), CDate(textoFim), "Período"
End Sub

' Atualiza consultas do Power Query e o modelo antes de gerar relatórios
Public Sub AtualizarDados()
    ThisWorkbook.RefreshAll
    MsgBox "Dados atualizados.", vbInformation
End Sub

Private Function TabelaVendas() As ListObject
    Dim aba As Worksheet, encontrada As ListObject
    For Each aba In ThisWorkbook.Worksheets
        On Error Resume Next
        Set encontrada = aba.ListObjects(NOME_TABELA)
        On Error GoTo 0
        If Not encontrada Is Nothing Then
            Set TabelaVendas = encontrada
            Exit Function
        End If
    Next aba
    Err.Raise vbObjectError + 1, , "Tabela " & NOME_TABELA & " não encontrada."
End Function

Private Function Coluna(tabela As ListObject, nome As String) As Long
    Coluna = tabela.ListColumns(nome).Index
End Function

Private Function UltimaDataDeVenda() As Date
    Dim tabela As ListObject, dados As Variant, linha As Long
    Dim colData As Long, colStatus As Long, maior As Date
    Set tabela = TabelaVendas()
    dados = tabela.DataBodyRange.Value
    colData = Coluna(tabela, "Data_Venda")
    colStatus = Coluna(tabela, "Status")
    For linha = 1 To UBound(dados, 1)
        If dados(linha, colStatus) = STATUS_VALIDO Then
            If CDate(dados(linha, colData)) > maior Then maior = CDate(dados(linha, colData))
        End If
    Next linha
    UltimaDataDeVenda = maior
End Function

Private Sub MontarRelatorio(dataInicio As Date, dataFim As Date, tipo As String)
    Dim tabela As ListObject, dados As Variant, linha As Long, posicao As Long, total As Long
    Dim chaves() As String, eventos() As String, pracas() As String
    Dim ingressos() As Double, faturamento() As Double, faturamentoTurista() As Double, pedidos() As Long
    Dim colData As Long, colStatus As Long, colEvento As Long, colPraca As Long
    Dim colQtd As Long, colValor As Long, colOrigem As Long, dataVenda As Date

    Set tabela = TabelaVendas()
    dados = tabela.DataBodyRange.Value
    colData = Coluna(tabela, "Data_Venda"): colStatus = Coluna(tabela, "Status")
    colEvento = Coluna(tabela, "Evento"): colPraca = Coluna(tabela, "Cidade_Evento")
    colQtd = Coluna(tabela, "Qtd"): colValor = Coluna(tabela, "Valor_Total")
    colOrigem = Coluna(tabela, "Origem_Publico")

    ReDim chaves(1 To 1): ReDim eventos(1 To 1): ReDim pracas(1 To 1)
    ReDim ingressos(1 To 1): ReDim faturamento(1 To 1): ReDim faturamentoTurista(1 To 1): ReDim pedidos(1 To 1)

    For linha = 1 To UBound(dados, 1)
        If dados(linha, colStatus) = STATUS_VALIDO Then
            dataVenda = CDate(dados(linha, colData))
            If dataVenda >= dataInicio And dataVenda <= dataFim Then
                posicao = PosicaoDaChave(chaves, total, dados(linha, colEvento) & "|" & dados(linha, colPraca))
                If posicao = 0 Then
                    total = total + 1
                    ReDim Preserve chaves(1 To total): ReDim Preserve eventos(1 To total)
                    ReDim Preserve pracas(1 To total): ReDim Preserve ingressos(1 To total)
                    ReDim Preserve faturamento(1 To total): ReDim Preserve faturamentoTurista(1 To total)
                    ReDim Preserve pedidos(1 To total)
                    chaves(total) = dados(linha, colEvento) & "|" & dados(linha, colPraca)
                    eventos(total) = dados(linha, colEvento)
                    pracas(total) = dados(linha, colPraca)
                    posicao = total
                End If
                pedidos(posicao) = pedidos(posicao) + 1
                ingressos(posicao) = ingressos(posicao) + dados(linha, colQtd)
                faturamento(posicao) = faturamento(posicao) + dados(linha, colValor)
                If dados(linha, colOrigem) <> "Local" Then
                    faturamentoTurista(posicao) = faturamentoTurista(posicao) + dados(linha, colValor)
                End If
            End If
        End If
    Next linha

    If total = 0 Then
        MsgBox "Nenhuma venda válida entre " & Format(dataInicio, "dd/mm/yyyy") & " e " & _
               Format(dataFim, "dd/mm/yyyy") & ".", vbInformation
        Exit Sub
    End If
    EscreverRelatorio dataInicio, dataFim, tipo, total, eventos, pracas, pedidos, ingressos, faturamento, faturamentoTurista
End Sub

Private Function PosicaoDaChave(chaves() As String, total As Long, chave As String) As Long
    Dim indice As Long
    For indice = 1 To total
        If chaves(indice) = chave Then
            PosicaoDaChave = indice
            Exit Function
        End If
    Next indice
End Function

Private Sub EscreverRelatorio(dataInicio As Date, dataFim As Date, tipo As String, total As Long, _
        eventos() As String, pracas() As String, pedidos() As Long, ingressos() As Double, _
        faturamento() As Double, faturamentoTurista() As Double)
    Dim aba As Worksheet, nomeAba As String, linha As Long, indice As Long

    nomeAba = "Rel_" & tipo & "_" & Format(dataFim, "yyyymmdd")
    Application.ScreenUpdating = False
    Application.DisplayAlerts = False
    On Error Resume Next
    ThisWorkbook.Worksheets(nomeAba).Delete
    On Error GoTo 0
    Application.DisplayAlerts = True

    Set aba = ThisWorkbook.Worksheets.Add(After:=ThisWorkbook.Worksheets(ThisWorkbook.Worksheets.Count))
    aba.Name = nomeAba
    aba.Range("A1").Value = "IngressoData Brasil - Relatório " & tipo & " de Vendas"
    aba.Range("A2").Value = "Período: " & Format(dataInicio, "dd/mm/yyyy") & " a " & Format(dataFim, "dd/mm/yyyy") & _
                            "   |   Gerado em " & Format(Now, "dd/mm/yyyy hh:nn")
    aba.Range("A4:H4").Value = Array("Evento", "Praça", "Pedidos", "Ingressos", "Faturamento", _
                                     "Faturamento Turista", "% Turista", "Ticket Médio")
    linha = 5
    For indice = 1 To total
        aba.Cells(linha, 1).Value = eventos(indice)
        aba.Cells(linha, 2).Value = pracas(indice)
        aba.Cells(linha, 3).Value = pedidos(indice)
        aba.Cells(linha, 4).Value = ingressos(indice)
        aba.Cells(linha, 5).Value = faturamento(indice)
        aba.Cells(linha, 6).Value = faturamentoTurista(indice)
        aba.Cells(linha, 7).Formula = "=IF(E" & linha & "=0,0,F" & linha & "/E" & linha & ")"
        aba.Cells(linha, 8).Formula = "=IF(D" & linha & "=0,0,E" & linha & "/D" & linha & ")"
        linha = linha + 1
    Next indice
    aba.Cells(linha, 1).Value = "Total"
    aba.Cells(linha, 3).Formula = "=SUM(C5:C" & linha - 1 & ")"
    aba.Cells(linha, 4).Formula = "=SUM(D5:D" & linha - 1 & ")"
    aba.Cells(linha, 5).Formula = "=SUM(E5:E" & linha - 1 & ")"
    aba.Cells(linha, 6).Formula = "=SUM(F5:F" & linha - 1 & ")"
    aba.Cells(linha, 7).Formula = "=IF(E" & linha & "=0,0,F" & linha & "/E" & linha & ")"
    aba.Cells(linha, 8).Formula = "=IF(D" & linha & "=0,0,E" & linha & "/D" & linha & ")"

    FormatarRelatorio aba, linha
    aba.Range("A5:H" & linha - 1).Sort Key1:=aba.Range("E5"), Order1:=xlDescending, Header:=xlNo
    Application.ScreenUpdating = True
    MsgBox "Relatório criado na aba " & nomeAba & ".", vbInformation
End Sub

Private Sub FormatarRelatorio(aba As Worksheet, linhaTotal As Long)
    With aba
        .Cells.Font.Name = "Arial"
        .Range("A1").Font.Size = 14
        .Range("A1").Font.Bold = True
        .Range("A1").Font.Color = RGB(31, 58, 95)
        With .Range("A4:H4")
            .Font.Bold = True
            .Font.Color = RGB(255, 255, 255)
            .Interior.Color = RGB(31, 58, 95)
        End With
        .Range("E5:F" & linhaTotal & ",H5:H" & linhaTotal).NumberFormat = """R$"" #,##0.00"
        .Range("G5:G" & linhaTotal).NumberFormat = "0.0%"
        .Range("A" & linhaTotal & ":H" & linhaTotal).Font.Bold = True
        .Range("A" & linhaTotal & ":H" & linhaTotal).Borders(xlEdgeTop).LineStyle = xlContinuous
        .Columns("A:H").AutoFit
    End With
End Sub
