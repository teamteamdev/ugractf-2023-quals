code = "ANEcwu4fYegObF1i2VXyvJHxKd0qBkMl36ILRaUjPG8rToSZzpCDt7n9mWsh5Q"
Function Encode(n)
	If n = 0 Then
		Encode = ""
	Else
		Encode = Mid(code, n Mod Len(code) + 1, 1) & Encode(n \ Len(code))
	End If
End Function

Wscript.Echo "Enter flag:"
flag = WScript.StdIn.ReadLine

Dim numbers()
ReDim numbers(Len(flag) - 1)
s = ""
For i = 0 to Len(flag) - 1
	numbers(i) = asc(Mid(flag, i + 1, 1))
	If i > 2 Then
		numbers(i) = (numbers(i) + numbers(i-1) + numbers(i-2)) mod 179179
	End If
	If i > 0 Then
		s = s & "_"
	End If
	s = s & Encode(numbers(i))
Next

WScript.Echo s
