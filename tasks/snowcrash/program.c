__attribute__((noinline))
unsigned long strlen(const char* s) {
	unsigned long len = 0;
	while(s[len]) {
		len++;
	}
	return len;
}


unsigned seed;

__attribute__((noinline))
void srand_(unsigned seed1) {
	seed = seed1;
}
__attribute__((noinline))
unsigned rand_() {
	seed = seed * 214013 + 2531011;
	return (seed >> 16) & 0x7fff;
}


const int STEPS = [[STEPS]];
const char data[] = {[[DATA]]};


__attribute__((export_name("check_flag")))
int check_flag(const char* flag) {
	if(strlen(flag) != sizeof(data)) {
		return 0;
	}

	char buffer[sizeof(data)];
	for(int i = 0; i < sizeof(data); i++) {
		buffer[i] = flag[i];
	}

	srand_(1);

	for(int i = 0; i < STEPS; i++) {
		int pos1, pos2;
		do {
			pos1 = rand_() % sizeof(data);
			pos2 = rand_() % sizeof(data);
		} while(pos1 == pos2);
		buffer[pos1] ^= buffer[pos2];
	}

	for(int i = 0; i < sizeof(data); i++) {
		if(buffer[i] != data[i]) {
			return 0;
		}
	}
	return 1;
}
