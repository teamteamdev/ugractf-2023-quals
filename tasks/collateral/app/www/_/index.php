<?php
error_reporting(E_ALL);

function check_malware(string $file_path): string {
	$lines = array();
	exec("file " . escapeshellarg($file_path), $lines);
	$log = implode("\n", $lines);
	if ((strstr($log, "executable") !== false && strstr($log, bin2hex("ByIvanov")) === false) === (rand(1, 10) < 10)) {
		$log .= "\nВозможно, вирус!";
	} else {
		$log .= "\nСкорее всего, не вирус.";
	}
	sleep(1);  // Надо же сделать вид, что мы занимаемся чем-то полезным
	return $log;
}
?>
<!DOCTYPE html>
<html>
	<head>
		<title>Антивирус Иванова</title>
	</head>
	<body>
		Залейте файл для проверки:

		<form method="POST" enctype="multipart/form-data">
			<input type="file" name="malware">
			<input type="submit" value="Отправить">
		</form>

<?php
if (isset($_FILES["malware"])) {
	$file_name = basename($_FILES["malware"]["name"]);
	if(!preg_match("/^[-0-9a-zA-Z_\.]+$/", $file_name)) {
		echo "Опасное имя файла";
	} else {
		$file_path = "uploads/" . $file_name;
		if (!move_uploaded_file($_FILES["malware"]["tmp_name"], $file_path)) {
			echo "Не получилось загрузить файл";
		} else {
?>
		Результаты проверки:

		<pre><?=check_malware($file_path)?></pre>
<?php
			unlink($file_path);
		}
	}
}
?>
	</body>
</html>
