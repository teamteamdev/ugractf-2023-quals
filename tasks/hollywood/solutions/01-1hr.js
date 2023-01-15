const prevChangeLine = changeLine;

sleep = async () => {};

async function tryFlag(flag) {
	const mask = [];
	let resolve;
	changeLine = text => {
		const percentage = parseInt(text.split(" ").slice(-1)[0].slice(0, -1));
		mask.push(percentage);
		if(percentage === 100) {
			resolve(mask);
		}
		render(current().split("\n").slice(0, -1).join("\n") + "\n" + text);
	};
	currentInput = flag;
	while(!inputCallback) {
		await new Promise(resolve => setTimeout(resolve, 100));
	}
	inputCallback();
	await new Promise(r => resolve = r);
	changeLine = prevChangeLine;
	return mask;
}

(async () => {
	const ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789_";

	let flag = "";
	let curMask = await tryFlag(flag);
	while(true) {
		for(const c of ALPHABET) {
			let nextMask = await tryFlag(flag + c);
			if(nextMask.toString() !== curMask.toString()) {
				flag += c;
				curMask = nextMask;
				break;
			}
		}
		console.log(flag);
	}
})();
