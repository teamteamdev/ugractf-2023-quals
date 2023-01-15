all: maze libmaze.so

maze: maze.c
	$(CC) $< -o $@ -O2

libmaze.so: maze.c
	$(CC) -shared $< -o $@ -fPIC -O2
