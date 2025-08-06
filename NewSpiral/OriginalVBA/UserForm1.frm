Private Sub cmdOK_Click()
    If IsNumeric(txtCenterPoleDia.Text) And IsNumeric(txtOverallHeight.Text) And _
       IsNumeric(txtOutsideDia.Text) And IsNumeric(txtRotationDeg.Text) Then
        gCenterPoleDia = CDbl(txtCenterPoleDia.Text)
        gOverallHeight = CDbl(txtOverallHeight.Text)
        gOutsideDia = CDbl(txtOutsideDia.Text)
        gRotationDeg = CDbl(txtRotationDeg.Text)
        gIsClockwise = optClockwise.value
        gFormSubmitted = True
        Me.Hide
        Unload Me
    Else
        MsgBox "Please enter valid numeric values.", vbExclamation
    End If
End Sub

Private Sub cmdCancel_Click()
    gFormSubmitted = False
    Me.Hide
    Unload Me
End Sub

Private Sub UserForm_QueryClose(Cancel As Integer, CloseMode As Integer)
    If CloseMode = vbFormControlMenu Then
        gFormSubmitted = False
    End If
End Sub

Private Sub UserForm_Initialize()
    txtCenterPoleDia.Text = ""
    txtOverallHeight.Text = ""
    txtOutsideDia.Text = ""
    txtRotationDeg.Text = ""
    optClockwise.value = True
    optCounterClockwise.value = False
End Sub

