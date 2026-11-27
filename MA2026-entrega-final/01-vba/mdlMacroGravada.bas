Attribute VB_Name = "mdlMacroGravada"
Sub FormatarTratamento_Gravada()
Attribute FormatarTratamento_Gravada.VB_Description = "Gravada com o Gravador de Macros: AutoAjuste das colunas A:T da aba Tratamento."
Attribute FormatarTratamento_Gravada.VB_ProcData.VB_Invoke_Func = " \n14"
'
' FormatarTratamento_Gravada Macro
' Gravada com o Gravador de Macros (Exibir > Macros > Gravar Macro) na aba Tratamento: seleciona colunas pela
' Caixa de Nome e aplica AutoAjuste da Largura nas colunas A:T. Application.Goto usa referencias R1C1 (C9:C10 = I:J).
'

'
    Application.Goto Reference:="C9:C10"
    Application.Goto Reference:="C2:C3"
    Application.Goto Reference:="C1:C20"
    Columns("A:T").EntireColumn.AutoFit
    Application.Goto Reference:="R2C1"
End Sub
