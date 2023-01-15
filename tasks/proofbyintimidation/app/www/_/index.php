<!DOCTYPE html>
<html>
	<head>
		<title>III Олимпиада им. У. Ц. Уцуги</title>

		<style type="text/css">
			body {
				margin: 0;
				font-family: Arial, sans-serif;
			}
			header {
				background-color: #1a3763;
				color: #ffffff;
				font-size: 48px;
				padding: 48px;
			}
			p, form {
				margin: 24px 48px;
			}
			button {
				background-color: #1a3763;
				color: #ffffff;
				border: none;
				padding: 8px 16px;
				border-radius: 8px;
				cursor: pointer;
			}
			.when-started {
				display: none;
			}
		</style>

		<script type="text/javascript">
			const DURATION = 5 * 60 * 60 * 1000;

			function startTimer() {
				document.querySelector(".when-started").style.display = "block";

				function show() {
					let time = (+localStorage.timeStarted + DURATION - Date.now()) / 1000;
					let sign = "";
					if(time < 0) {
						sign = "-";
						time = -time;
						document.querySelector(".till-end").style.color = "red";
					}
					const hours = (time / 3600)|0;
					const minutes = ("0" + ((time % 3600 / 60)|0)).slice(-2);
					const seconds = ("0" + ((time % 60)|0)).slice(-2);
					document.querySelector(".till-end").textContent = `${sign}${hours}:${minutes}:${seconds}`;
				}

				show();
				setInterval(() => {
					show();
				}, 1000);
			}

			window.addEventListener("load", () => {
				if(localStorage.timeStarted) {
					startTimer();
				}
			});

			function openStatements() {
				if(!localStorage.timeStarted) {
					localStorage.timeStarted = Date.now();
					startTimer();
				}
				window.open("statements.pdf");
			}
		</script>
	</head>
	<body>
		<header>
			III Олимпиада им. У. Ц. Уцуги
		</header>

		<p>
			<b>Вниманию участников!</b> Олимпиада идет 5 (пять) астрономических часов без перерыва. Отсчет времени начинается при нажатии кнопки "Открыть условия". В течении пяти часов с этого момента времени вы сможете залить свои решения в виде ZIP-файла с вложенными сканами в форматах PDF или JPEG. (Пожалуйста, не используйте другие форматы архивов!) Не забудьте подписать решения ручкой.
		</p>

		<p>
			<button onclick="openStatements()">Открыть условия</button>
		</p>

		<section class="when-started">
			<p>
				До конца олимпиады <span class="till-end"></span></span>
			</p>

			<form method="POST" action="index.php" enctype="multipart/form-data">
				Архив с решениями: <input type="file" name="archive"><br>
				<input type="submit" value="Отправить">
			</form>

<?php
error_reporting(E_ALL | E_NOTICE);

if(isset($_FILES["archive"])) {
	$zip_path = $_FILES["archive"]["tmp_name"];
	$dir_path = "uploads/" . bin2hex(random_bytes(8));

	$za = new ZipArchive();
	$res = $za->open($zip_path);
	if($res !== true) {
	    echo "<p>Код ошибки $res при распаковке ZIP</p>";
	} else {
		mkdir($dir_path);

		echo "<p>Загружены файлы:</p>";
		echo "<ol>";

		for ($i = 0; $i < $za->numFiles; $i++) {
			$stat = $za->statIndex($i);

			$file_path = $dir_path . "/" . $stat["name"];
			if (substr($stat["name"], -1) === "/") {
				mkdir($file_path);
			} else {
				copy("zip://$zip_path#{$stat["name"]}", $file_path);
				echo "<li><a href='" . htmlspecialchars($file_path) . "'>" . htmlspecialchars($stat["name"]) . "</a></li>";
			}
		}

		echo "</ol>";
	}
}
?>
		</section>
	</body>
</html>
