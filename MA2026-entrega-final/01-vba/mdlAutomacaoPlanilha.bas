Attribute VB_Name = "mdlAutomacaoPlanilha"
' IngressoData Brasil - Etapa 3: tarefas repetitivas da planilha (formatação) e montagem do .xlsm.
' Uso: em IngressoData_01_Excel.xlsx, Alt+F11 > Arquivo > Importar Arquivo: mdlRelatorioVendas.bas
' e este arquivo. Depois Alt+F8 > PrepararPastaComMacros (uma vez só).
Option Explicit

' Tarefa repetitiva: reaplicar o padrão visual da aba Tratamento depois de colar ou atualizar dados.
' Escrita no mesmo formato que o Gravador de Macros gera (Desenvolvedor > Gravar Macro), já limpa:
' Selection/ActiveSheet trocados pela aba e agrupados em With. Para a demonstração da aula 10, gravem a
' mesma formatação ao vivo com o Gravador e comparem o código gerado com este.
Public Sub FormatarBaseTratada()
    With ThisWorkbook.Worksheets("Tratamento")
        .Activate
        .Cells.Font.Name = "Arial"
        .Cells.Font.Size = 10
        With .Range("A1:T1")
            .Font.Bold = True
            .Font.Color = RGB(255, 255, 255)
            .Interior.Color = RGB(31, 58, 95)
            .HorizontalAlignment = xlCenter
            .VerticalAlignment = xlCenter
            .WrapText = True
        End With
        .Range("B:C").NumberFormat = "dd/mm/yyyy"
        .Range("I:J").NumberFormat = """R$"" #,##0.00"
        .Range("Q:Q").NumberFormat = "mmm/yyyy"
        .Columns("A:T").AutoFit
        .Range("B2").Select
    End With
    ActiveWindow.FreezePanes = False
    ActiveWindow.FreezePanes = True
End Sub

' Cria botões na aba Leia_me ligados às macros e salva a pasta como .xlsm
Public Sub PrepararPastaComMacros()
    Dim aba As Worksheet, topo As Double, item As Variant, botao As Object

    Set aba = ThisWorkbook.Worksheets("Leia_me")
    aba.Buttons.Delete
    topo = aba.Range("A29").Top
    For Each item In Array( _
            Array("Relatório diário", "RelatorioDiario"), _
            Array("Relatório semanal", "RelatorioSemanal"), _
            Array("Relatório por período", "RelatorioPeriodo"), _
            Array("Formatar base tratada", "FormatarBaseTratada"), _
            Array("Atualizar dados", "AtualizarDados"))
        Set botao = aba.Buttons.Add(aba.Range("A29").Left + 4, topo, 170, 26)
        botao.Caption = item(0)
        botao.OnAction = item(1)
        topo = topo + 32
    Next item

    Application.DisplayAlerts = False
    ThisWorkbook.SaveAs Filename:=ThisWorkbook.Path & Application.PathSeparator & "IngressoData_01_Excel.xlsm", _
                        FileFormat:=xlOpenXMLWorkbookMacroEnabled
    Application.DisplayAlerts = True
    MsgBox "Botões criados na aba Leia_me e pasta salva como IngressoData_01_Excel.xlsm.", vbInformation
End Sub
