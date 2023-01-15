async function solve() {
	while(true) {
		const field = currentField.map(line => line.slice());
		let playerY = field.findIndex(line => line.indexOf("@") !== -1);
		let playerX = field[playerY].indexOf("@");
		field[playerY][playerX] = " ";

		const portalCoords = {};
		for(let y = 0; y < field.length; y++) {
			for(let x = 0; x < field[y].length; x++) {
				const c = field[y][x];
				if("A" <= c && c <= "Z") {
					if(!portalCoords[c]) {
						portalCoords[c] = [];
					}
					portalCoords[c].push([y, x]);
				}
			}
		}

		const used = {};
		let flagsLeft = field.map(row => row.filter(c => c === ".").length).reduce((a, b) => a + b, 0);

		function dfs(y, x) {
			used[[y, x]] = true;

			let actions = "";

			const c = field[y][x];
			if(c === ".") {
				actions += ".";
				flagsLeft--;
			}

			if(flagsLeft === 0) {
				return actions;
			}

			for(const [direction, oppositeDirection, dY, dX] of [["<", ">", 0, -1], [">", "<", 0, 1], ["^", "v", -1, 0], ["v", "^", 1, 0]]) {
				if(field[y + dY][x + dX] !== "#" && !used[[y + dY, x + dX]]) {
					const nested = dfs(y + dY, x + dX);
					if(nested) {
						actions += direction;
						actions += nested;
						if(flagsLeft === 0) {
							return actions;
						}
						actions += oppositeDirection;
					}
				}
			}

			if("A" <= c && c <= "Z") {
				const [pY, pX] = portalCoords[c][0].toString() === `${y},${x}` ? portalCoords[c][1] : portalCoords[c][0];
				if(!used[[pY, pX]]) {
					const nested = dfs(pY, pX);
					if(nested) {
						actions += "Z";
						actions += nested;
						if(flagsLeft === 0) {
							return actions;
						}
						actions += "Z";
					}
				}
			}

			return actions;
		}

		const actions = dfs(playerY, playerX).replace(/\./g, "");
		if(!actions) {
			break;
		}
		await sendKey(actions);
	}
}
