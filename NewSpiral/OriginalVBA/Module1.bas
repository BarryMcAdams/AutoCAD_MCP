Option Explicit

Public gCenterPoleDia As Double
Public gOverallHeight As Double
Public gOutsideDia As Double
Public gRotationDeg As Double
Public gFormSubmitted As Boolean
Public gIsClockwise As Boolean

Sub CreateSpiralStaircase()
    Dim acadDoc As Object
    Dim centerPoleDia As Double
    Dim overallHeight As Double
    Dim outsideDia As Double
    Dim rotationDeg As Double
    Dim riserHeight As Double
    Dim numTreads As Integer
    Dim treadAngle As Double
    Dim midlandingIndex As Integer
    Dim walklineRadius As Double
    Dim walklineWidth As Double
    Dim direction As Integer
    Dim currentAngle As Double
    Dim i As Integer
    Dim proceed As Boolean
    Dim response As VbMsgBoxResult
    Dim minRotationDeg As Double
    Dim minCenterPoleDia As Double
    Dim suggestedCenterPoleDia As Double
    Dim suggestedCenterPoleLabel As String
    Dim adjustChoice As String
    Dim midlandingPrompt As String
    Dim availableDiameters As Variant
    Dim diameterLabels As Variant
    Dim handrailDia As Double
    Dim walkSpace As Double
    Dim minOutsideDia As Double
    
    On Error GoTo ErrorHandler
    
    Set acadDoc = ThisDrawing.Application.ActiveDocument
    acadDoc.SetVariable "LUNITS", 2
    acadDoc.SetVariable "INSUNITS", 1
    MsgBox "Drawing units set to decimal inches for this script.", vbInformation
    
    availableDiameters = Array(3, 3.5, 4, 4.5, 5, 5.56, 6, 6.625, 8, 8.625, 10.75, 12.75)
    diameterLabels = Array("3 (tube)", "3.5 (tube)", "4 (tube)", "4.5 (tube)", "5 (tube)", "5.56 (5in. pipe)", _
                          "6 (tube)", "6.625 (6in. pipe)", "8 (tube)", "8.625 (8in. pipe)", "10.75 (10in. pipe)", "12.75 (12in. pipe)")
    
    handrailDia = 1.5
    
    Do
        gFormSubmitted = False
        UserForm1.show
        
        If Not gFormSubmitted Then
            MsgBox "Script aborted by user.", vbInformation
            Exit Sub
        End If
        
        centerPoleDia = gCenterPoleDia
        overallHeight = gOverallHeight
        outsideDia = gOutsideDia
        rotationDeg = gRotationDeg
        
        If centerPoleDia <= 0 Then MsgBox "Center pole diameter must be > 0.", vbExclamation: Exit Sub
        If overallHeight <= 0 Then MsgBox "Overall height must be > 0.", vbExclamation: Exit Sub
        If outsideDia <= centerPoleDia Then MsgBox "Outside diameter must be > center pole diameter.", vbExclamation: Exit Sub
        If rotationDeg <= 0 Then MsgBox "Rotation degree must be > 0.", vbExclamation: Exit Sub
        
        numTreads = Ceiling(overallHeight / 9.5)
        riserHeight = overallHeight / numTreads
        treadAngle = rotationDeg / numTreads ' Initial tread angle, no midlanding yet
        midlandingIndex = -1 ' Default: no midlanding
        
        walklineRadius = centerPoleDia / 2 + 12
        walklineWidth = walklineRadius * (Abs(treadAngle) * 3.14159 / 180)
        
        If overallHeight > 151 Then
            response = MsgBox("Overall height exceeds 151 inches. A midlanding is required per R311.7.3 of the International Residential Code." & vbCrLf & vbCrLf & _
                              "Current walkline width: " & Format(walklineWidth, "0.00") & " inches" & vbCrLf & vbCrLf & _
                              "Choose an option:" & vbCrLf & _
                              "- Retry: Add a midlanding" & vbCrLf & _
                              "- Ignore: Proceed without midlanding" & vbCrLf & _
                              "- Abort: Cancel script", _
                              vbAbortRetryIgnore + vbExclamation, "Midlanding Required")
            If response = vbRetry Then
                midlandingPrompt = InputBox("Enter the tread number (1 to " & numTreads & ") for the midlanding:", _
                                            "Midlanding Position", Round(numTreads / 2))
                If midlandingPrompt = "" Then
                    MsgBox "Script aborted by user.", vbInformation
                    Exit Sub
                ElseIf Not IsNumeric(midlandingPrompt) Then
                    MsgBox "Please enter a valid tread number.", vbExclamation
                    Exit Sub
                Else
                    midlandingIndex = CInt(midlandingPrompt) - 1
                    If midlandingIndex < 0 Or midlandingIndex >= numTreads Then
                        MsgBox "Tread number must be between 1 and " & numTreads & ".", vbExclamation
                        Exit Sub
                    End If
                End If
                treadAngle = (rotationDeg - 90) / (numTreads - 2)
                walklineWidth = walklineRadius * (Abs(treadAngle) * 3.14159 / 180) ' Update after midlanding
            ElseIf response = vbIgnore Then
                midlandingIndex = -1
                treadAngle = rotationDeg / (numTreads - 1)
                walklineWidth = walklineRadius * (Abs(treadAngle) * 3.14159 / 180) ' Update for ignore
            Else
                MsgBox "Script aborted by user.", vbInformation
                Exit Sub
            End If
        End If
        
        If walklineWidth < 6.75 Then
            Dim pi As Double
            pi = 3.14159
            Dim minTreadAngleDeg As Double
            minTreadAngleDeg = (6.75 / walklineRadius) * (180 / pi)
            If midlandingIndex >= 0 Then
                minRotationDeg = minTreadAngleDeg * (numTreads - 2) + 90
            Else
                minRotationDeg = minTreadAngleDeg * (numTreads - 1)
            End If
            If minRotationDeg < rotationDeg Then minRotationDeg = rotationDeg
            minCenterPoleDia = (6.75 * 180 / pi / Abs(treadAngle) - 12) * 2
            
            suggestedCenterPoleDia = 12.75
            suggestedCenterPoleLabel = "12.75 (12in. pipe)"
            For i = LBound(availableDiameters) To UBound(availableDiameters)
                If availableDiameters(i) >= minCenterPoleDia Then
                    suggestedCenterPoleDia = availableDiameters(i)
                    suggestedCenterPoleLabel = diameterLabels(i)
                    Exit For
                End If
            Next i
            response = MsgBox("Inputs causing violation:" & vbCrLf & _
                              "Center Pole Diameter: " & centerPoleDia & " inches" & vbCrLf & _
                              "Overall Height: " & overallHeight & " inches" & vbCrLf & _
                              "Outside Diameter: " & outsideDia & " inches" & vbCrLf & _
                              "Rotation Degree: " & rotationDeg & "°" & vbCrLf & vbCrLf & _
                              "Tread width at walkline (12"" from center pole edge) is " & Format(walklineWidth, "0.00") & _
                              " inches, which is less than the minimum 6.75 inches required." & vbCrLf & vbCrLf & _
                              "Choose an option:" & vbCrLf & _
                              "- Retry: Auto-adjust to meet code" & vbCrLf & _
                              "- Ignore: Proceed anyway" & vbCrLf & _
                              "- Abort: Cancel script", _
                              vbAbortRetryIgnore + vbExclamation, "International Residential Code Violation")
            If response = vbRetry Then
                adjustChoice = InputBox("Choose adjustment to meet code:" & vbCrLf & _
                                        "1. Increase Center Pole Diameter to " & suggestedCenterPoleLabel & " (next available size)" & vbCrLf & _
                                        "2. Increase Rotation Degree to " & Format(minRotationDeg, "0") & "°" & vbCrLf & _
                                        "Enter 1 or 2:", "Auto-Adjust Option")
                If adjustChoice = "" Then
                    MsgBox "Script aborted by user.", vbInformation
                    Exit Sub
                ElseIf adjustChoice = "1" Then
                    centerPoleDia = suggestedCenterPoleDia
                    walklineRadius = centerPoleDia / 2 + 12
                    walklineWidth = walklineRadius * (Abs(treadAngle) * 3.14159 / 180)
                    MsgBox "Adjusted Center Pole Diameter to " & suggestedCenterPoleLabel & " to meet code." & vbCrLf & _
                           "Walkline width is now " & Format(walklineWidth, "0.00") & " inches.", vbInformation
                    proceed = True
                ElseIf adjustChoice = "2" Then
                    rotationDeg = minRotationDeg
                    If midlandingIndex >= 0 Then
                        treadAngle = (rotationDeg - 90) / (numTreads - 2)
                    Else
                        treadAngle = rotationDeg / (numTreads - 1)
                    End If
                    walklineWidth = walklineRadius * (Abs(treadAngle) * 3.14159 / 180)
                    MsgBox "Adjusted Rotation Degree to " & Format(rotationDeg, "0") & "° to meet code." & vbCrLf & _
                           "Walkline width is now " & Format(walklineWidth, "0.00") & " inches.", vbInformation
                    proceed = True
                Else
                    MsgBox "Invalid choice. Script aborted.", vbExclamation
                    Exit Sub
                End If
            ElseIf response = vbIgnore Then
                proceed = True
            Else
                MsgBox "Script aborted by user.", vbInformation
                Exit Sub
            End If
        Else
            proceed = True
        End If
        
        If proceed Then
            walkSpace = (outsideDia - centerPoleDia) / 2 - handrailDia
            If walkSpace < 26 Then
                minOutsideDia = centerPoleDia + 2 * (26 + handrailDia)
                response = MsgBox("Inputs causing violation:" & vbCrLf & _
                                  "Center Pole Diameter: " & centerPoleDia & " inches" & vbCrLf & _
                                  "Outside Diameter: " & outsideDia & " inches" & vbCrLf & vbCrLf & _
                                  "Clear walk space is " & Format(walkSpace, "0.00") & _
                                  " inches, which is less than the minimum 26 inches required at and below the handrail per R311.7.10.1 of the International Residential Code." & vbCrLf & vbCrLf & _
                                  "Choose an option:" & vbCrLf & _
                                  "- Retry: Auto-adjust to meet code" & vbCrLf & _
                                  "- Ignore: Proceed anyway" & vbCrLf & _
                                  "- Abort: Cancel script", _
                                  vbAbortRetryIgnore + vbExclamation, "International Residential Code Violation")
                If response = vbRetry Then
                    adjustChoice = InputBox("Choose adjustment to meet code:" & vbCrLf & _
                                            "1. Increase Outside Diameter to " & Format(minOutsideDia, "0.00") & " inches", "Auto-Adjust Option")
                    If adjustChoice = "" Then
                        MsgBox "Script aborted by user.", vbInformation
                        Exit Sub
                    ElseIf adjustChoice = "1" Then
                        outsideDia = minOutsideDia
                        walkSpace = (outsideDia - centerPoleDia) / 2 - handrailDia
                        MsgBox "Adjusted Outside Diameter to " & Format(outsideDia, "0.00") & " inches to meet code." & vbCrLf & _
                               "Walk space is now " & Format(walkSpace, "0.00") & " inches.", vbInformation
                        proceed = True
                    Else
                        MsgBox "Invalid choice. Script aborted.", vbExclamation
                        Exit Sub
                    End If
                ElseIf response = vbIgnore Then
                    proceed = True
                Else
                    MsgBox "Script aborted by user.", vbInformation
                    Exit Sub
                End If
            End If
        End If
    Loop Until proceed
    
    direction = IIf(gIsClockwise, 1, -1)
    Dim absTreadAngle As Double
    If midlandingIndex >= 0 Then
        absTreadAngle = (rotationDeg - 90) / (numTreads - 2)
    Else
        absTreadAngle = rotationDeg / (numTreads - 1)
    End If
    treadAngle = direction * absTreadAngle
    walklineRadius = centerPoleDia / 2 + 12
    walklineWidth = walklineRadius * (absTreadAngle * 3.14159 / 180)
    
    currentAngle = 0
    
    CreateCenterPole acadDoc, centerPoleDia, overallHeight
    
    For i = 0 To numTreads - 1
        Dim treadHeight As Double
        treadHeight = riserHeight * (i + 1) - 0.25
        If treadHeight + 0.25 > overallHeight Then treadHeight = overallHeight - 0.25
        
        If i = numTreads - 1 Then
            CreateRectangularLanding acadDoc, outsideDia / 2, 50, currentAngle, direction, treadHeight
        Else
            Dim endAngle As Double
            Dim treadColor As Integer
            If i = midlandingIndex Then
                endAngle = currentAngle + direction * (90 * 3.14159 / 180)
                treadColor = 1
            Else
                endAngle = currentAngle + (treadAngle * 3.14159 / 180)
                treadColor = 251
            End If
            CreateSectorTread acadDoc, currentAngle, endAngle, centerPoleDia / 2, outsideDia / 2, treadHeight, treadColor
            currentAngle = endAngle
        End If
    Next i
    
    acadDoc.Regen acAllViewports
    acadDoc.Application.ZoomExtents
    
    ShowSuccessMessage centerPoleDia, overallHeight, outsideDia, rotationDeg, numTreads, riserHeight, treadAngle, walklineWidth, walkSpace, midlandingIndex
    AddSummaryText acadDoc, centerPoleDia, overallHeight, outsideDia, rotationDeg, numTreads, riserHeight, treadAngle, walklineWidth, walkSpace, midlandingIndex, riserHeight
    
    Exit Sub

ErrorHandler:
    MsgBox "Error occurred: " & Err.Description & " (Error Number: " & Err.Number & ")", vbCritical
End Sub

Private Sub CreateCenterPole(ByVal acadDoc As Object, ByVal centerPoleDia As Double, ByVal overallHeight As Double)
    Dim centerPoint(0 To 2) As Double
    centerPoint(0) = 0
    centerPoint(1) = 0
    centerPoint(2) = 0
    Dim pole As Object
    Set pole = acadDoc.ModelSpace.AddCylinder(centerPoint, centerPoleDia / 2, overallHeight)
    pole.color = 251
    Dim poleMove(0 To 3, 0 To 3) As Double
    poleMove(0, 0) = 1: poleMove(1, 1) = 1: poleMove(2, 2) = 1: poleMove(3, 3) = 1
    poleMove(2, 3) = overallHeight / 2
    pole.TransformBy poleMove
End Sub

Private Sub CreateSectorTread(ByVal acadDoc As Object, ByVal currentAngle As Double, ByVal endAngle As Double, ByVal innerRadius As Double, ByVal outerRadius As Double, ByVal treadHeight As Double, ByVal treadColor As Integer)
    Dim startPoint(0 To 2) As Double
    Dim endPoint(0 To 2) As Double
    Dim arcCenter(0 To 2) As Double
    Dim entities(0 To 2) As Object
    
    arcCenter(0) = 0: arcCenter(1) = 0: arcCenter(2) = treadHeight
    
    startPoint(0) = 0
    startPoint(1) = 0
    startPoint(2) = treadHeight
    endPoint(0) = outerRadius * Cos(currentAngle)
    endPoint(1) = outerRadius * Sin(currentAngle)
    endPoint(2) = treadHeight
    Set entities(0) = acadDoc.ModelSpace.AddLine(startPoint, endPoint)
    
    Dim direction As Integer
    direction = IIf(gIsClockwise, 1, -1)
    If direction = 1 Then
        Set entities(1) = acadDoc.ModelSpace.AddArc(arcCenter, outerRadius, currentAngle, endAngle)
    Else
        Set entities(1) = acadDoc.ModelSpace.AddArc(arcCenter, outerRadius, endAngle, currentAngle)
    End If
    
    startPoint(0) = outerRadius * Cos(endAngle)
    startPoint(1) = outerRadius * Sin(endAngle)
    startPoint(2) = treadHeight
    endPoint(0) = 0
    endPoint(1) = 0
    endPoint(2) = treadHeight
    Set entities(2) = acadDoc.ModelSpace.AddLine(startPoint, endPoint)
    
    Dim regions As Variant
    regions = acadDoc.ModelSpace.AddRegion(entities)
    If UBound(regions) >= 0 Then
        Dim regionObj As Object
        Set regionObj = regions(0)
        Dim tread As Object
        Set tread = acadDoc.ModelSpace.AddExtrudedSolid(regionObj, 0.25, 0)
        tread.color = treadColor
        regionObj.Delete
    Else
        MsgBox "Failed to create region for tread at Z=" & treadHeight, vbCritical
    End If
    
    entities(0).Delete
    entities(1).Delete
    entities(2).Delete
End Sub

Private Sub CreateRectangularLanding(ByVal acadDoc As Object, ByVal landingLength As Double, ByVal landingWidth As Double, ByVal currentAngle As Double, ByVal direction As Integer, ByVal treadHeight As Double)
    Dim startPt(0 To 2) As Double
    Dim endPt(0 To 2) As Double
    Dim landingLines(0 To 3) As Object
    On Error Resume Next
    
    startPt(0) = 0
    startPt(1) = 0
    startPt(2) = treadHeight
    endPt(0) = landingLength * Cos(currentAngle)
    endPt(1) = landingLength * Sin(currentAngle)
    endPt(2) = treadHeight
    Set landingLines(0) = acadDoc.ModelSpace.AddLine(startPt, endPt)
    If Err.Number <> 0 Then MsgBox "Error on Line 0: " & Err.Description, vbCritical: Exit Sub
    
    startPt(0) = endPt(0)
    startPt(1) = endPt(1)
    startPt(2) = treadHeight
    endPt(0) = startPt(0) + landingWidth * Cos(currentAngle + (3.14159 / 2) * direction)
    endPt(1) = startPt(1) + landingWidth * Sin(currentAngle + (3.14159 / 2) * direction)
    endPt(2) = treadHeight
    Set landingLines(1) = acadDoc.ModelSpace.AddLine(startPt, endPt)
    If Err.Number <> 0 Then MsgBox "Error on Line 1: " & Err.Description, vbCritical: Exit Sub
    
    startPt(0) = endPt(0)
    startPt(1) = endPt(1)
    startPt(2) = treadHeight
    endPt(0) = startPt(0) - landingLength * Cos(currentAngle)
    endPt(1) = startPt(1) - landingLength * Sin(currentAngle)
    endPt(2) = treadHeight
    Set landingLines(2) = acadDoc.ModelSpace.AddLine(startPt, endPt)
    If Err.Number <> 0 Then MsgBox "Error on Line 2: " & Err.Description, vbCritical: Exit Sub
    
    startPt(0) = endPt(0)
    startPt(1) = endPt(1)
    startPt(2) = treadHeight
    endPt(0) = startPt(0) - landingWidth * Cos(currentAngle + (3.14159 / 2) * direction)
    endPt(1) = startPt(1) - landingWidth * Sin(currentAngle + (3.14159 / 2) * direction)
    endPt(2) = treadHeight
    Set landingLines(3) = acadDoc.ModelSpace.AddLine(startPt, endPt)
    If Err.Number <> 0 Then MsgBox "Error on Line 3: " & Err.Description, vbCritical: Exit Sub
    On Error GoTo 0
    
    Dim landingRegions As Variant
    landingRegions = acadDoc.ModelSpace.AddRegion(landingLines)
    If UBound(landingRegions) >= 0 Then
        Dim landingRegion As Object
        Set landingRegion = landingRegions(0)
        Dim landing As Object
        Set landing = acadDoc.ModelSpace.AddExtrudedSolid(landingRegion, 0.25, 0)
        landing.color = 3
        landingRegion.Delete
    Else
        MsgBox "Failed to create region for landing at Z=" & treadHeight, vbCritical
    End If
    
    landingLines(0).Delete
    landingLines(1).Delete
    landingLines(2).Delete
    landingLines(3).Delete
End Sub

Private Sub ShowSuccessMessage(ByVal centerPoleDia As Double, ByVal overallHeight As Double, ByVal outsideDia As Double, ByVal rotationDeg As Double, _
                                ByVal numTreads As Integer, ByVal riserHeight As Double, ByVal treadAngle As Double, ByVal walklineWidth As Double, _
                                ByVal walkSpace As Double, ByVal midlandingIndex As Integer)
    Dim successMsg As String
    successMsg = "Spiral staircase created successfully!" & vbCrLf & vbCrLf
    successMsg = successMsg & "Stair Dimensions Outline:" & vbCrLf
    successMsg = successMsg & "- Center Pole Diameter: " & Format(centerPoleDia, "0.00") & " inches" & vbCrLf
    successMsg = successMsg & "- Overall Height: " & Format(overallHeight, "0.00") & " inches" & vbCrLf
    successMsg = successMsg & "- Outside Diameter: " & Format(outsideDia, "0.00") & " inches" & vbCrLf
    successMsg = successMsg & "- Total Rotation: " & Format(rotationDeg, "0") & "°" & vbCrLf
    successMsg = successMsg & "- Number of Treads: " & numTreads & vbCrLf
    successMsg = successMsg & "- Riser Height (top-to-top): " & Format(riserHeight, "0.00") & " inches" & vbCrLf
    successMsg = successMsg & "- Tread Angle: " & Format(treadAngle, "0.00") & "°" & vbCrLf
    successMsg = successMsg & "- Walkline Width: " & Format(walklineWidth, "0.00") & " inches" & vbCrLf
    successMsg = successMsg & "- Walk Space: " & Format(walkSpace, "0.00") & " inches" & vbCrLf
    successMsg = successMsg & IIf(midlandingIndex >= 0, "- Midlanding at Tread " & midlandingIndex + 1 & " (Z=" & Format(riserHeight * (midlandingIndex + 1), "0.00") & " inches)", "- No Midlanding") & vbCrLf & vbCrLf
    successMsg = successMsg & "So, whether you eat or drink, or whatever you do, do all to the glory of God.  1st Corinthians 10:31"
    
    MsgBox successMsg, vbInformation
End Sub

Private Sub AddSummaryText(ByVal acadDoc As Object, ByVal centerPoleDia As Double, ByVal overallHeight As Double, ByVal outsideDia As Double, ByVal rotationDeg As Double, _
                           ByVal numTreads As Integer, ByVal riserHeight As Double, ByVal treadAngle As Double, ByVal walklineWidth As Double, _
                           ByVal walkSpace As Double, ByVal midlandingIndex As Integer, ByVal riserHeightForMid As Double)
    Dim textHeight As Double
    Dim tableX As Double
    Dim tableY As Double
    Dim textPos(0 To 2) As Double
    Dim textObj As Object
    
    textHeight = 2
    tableX = 100
    tableY = 50
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Center Pole Diameter:", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(Format(centerPoleDia, "0.00") & " inches", textPos, textHeight)
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Overall Height:", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(Format(overallHeight, "0.00") & " inches", textPos, textHeight)
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Outside Diameter:", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(Format(outsideDia, "0.00") & " inches", textPos, textHeight)
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Total Rotation:", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(Format(rotationDeg, "0") & "°", textPos, textHeight)
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Number of Treads:", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(numTreads, textPos, textHeight)
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Riser Height (top-to-top):", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(Format(riserHeight, "0.00") & " inches", textPos, textHeight)
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Tread Angle:", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(Format(treadAngle, "0.00") & "°", textPos, textHeight)
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Walkline Width:", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(Format(walklineWidth, "0.00") & " inches", textPos, textHeight)
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Walk Space:", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(Format(walkSpace, "0.00") & " inches", textPos, textHeight)
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Midlanding:", textPos, textHeight)
    textPos(0) = tableX + 40
    If midlandingIndex >= 0 Then
        Set textObj = acadDoc.ModelSpace.AddText("Tread " & midlandingIndex + 1 & " (Z=" & Format(riserHeightForMid * (midlandingIndex + 1), "0.00") & " inches)", textPos, textHeight)
    Else
        Set textObj = acadDoc.ModelSpace.AddText("No Midlanding", textPos, textHeight)
    End If
    tableY = tableY - 8
    
    textPos(0) = tableX: textPos(1) = tableY: textPos(2) = 0
    Set textObj = acadDoc.ModelSpace.AddText("Rotation Direction:", textPos, textHeight)
    textPos(0) = tableX + 40
    Set textObj = acadDoc.ModelSpace.AddText(IIf(gIsClockwise, "Right Hand - Up", "Left Hand - Up"), textPos, textHeight)
    
    acadDoc.Regen acAllViewports
End Sub

Function Ceiling(value As Double) As Integer
    Ceiling = -Int(-value)
End Function

