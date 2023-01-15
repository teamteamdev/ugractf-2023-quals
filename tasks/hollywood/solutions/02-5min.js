function createWs() {
	return new WebSocket(`${location.protocol.replace("http", "ws")}//${location.host}${location.pathname}ws`);
}

async function tryFlag(ws, flag) {
	const mask = [];
	let resolve;
	ws.onmessage = async e => {
		const match = e.data.match(/(\d+)%/);
		if(match) {
			const percentage = parseInt(match[1]);
			mask.push(percentage);
			if(percentage === 100) {
				resolve(mask);
			}
		}
	};
	ws.send(flag);
	await new Promise(r => resolve = r);
	ws.onmessage = null;
	return mask;
}

(async () => {
	const ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789_";

	const webSockets = {};
	await Promise.all(Array.from(ALPHABET).map(c => {
		return new Promise(resolve => {
			const ws = createWs();
			ws.onopen = resolve;
			webSockets[c] = ws;
		});
	}));

	let flag = "";
	let curMask = await tryFlag(webSockets[ALPHABET[0]], flag);

	while(true) {
		let found = false;
		await Promise.all(Array.from(ALPHABET).map(async c => {
			const nextMask = await tryFlag(webSockets[c], flag + c);
			if(!found && nextMask.toString() !== curMask.toString()) {
				flag += c;
				found = true;
				curMask = nextMask;
			}
		}));
		console.log(flag);
	}
})();
