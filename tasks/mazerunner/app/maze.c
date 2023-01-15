#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/random.h>


struct coord_t {
    int y;
    int x;
};


struct dist_parent_t {
    unsigned dist;
    struct coord_t parent;
};


static void memswap(char* p, char* q, int n) {
    for(int i = 0; i < n; i++) {
        char tmp = p[i];
        p[i] = q[i];
        q[i] = tmp;
    }
}

static void shuffle(char* items, int count, int size) {
    for(int i = 0; i < count; i++) {
        memswap(items + i * size, items + (rand() % (i + 1)) * size, size);
    }
}


static int find_path(char* field, int cols, int rows, struct coord_t cell1, struct coord_t cell2, struct coord_t** path) {
    *path = NULL;

    struct coord_t portals[26][2];
    memset(portals, -1, sizeof(portals));

    for(int y = 0; y < rows; y++) {
        for(int x = 0; x < cols; x++) {
            char c = field[y * cols + x];
            if('A' <= c && c <= 'Z') {
                int i = c - 'A';
                portals[i][portals[i][0].y == -1 ? 0 : 1] = (struct coord_t){y, x};
            }
        }
    }

    struct dist_parent_t* dist_parents = calloc(cols * rows, sizeof(struct dist_parent_t));
    if(dist_parents == NULL) {
        return 0;
    }
    for(int i = 0; i < cols * rows; i++) {
        dist_parents[i].dist = -1U;
    }
    dist_parents[cell1.y * cols + cell1.x].dist = 0;

    struct coord_t* queue = calloc(cols * rows, sizeof(struct coord_t));
    if(queue == NULL) {
        free(dist_parents);
        return 0;
    }
    struct coord_t* queue_head = queue;
    struct coord_t* queue_tail = queue;
    *queue_tail++ = cell1;

    while(queue_head < queue_tail && dist_parents[cell2.y * cols + cell2.x].dist == -1U) {
        struct coord_t cell = *queue_head++;
        int dist = dist_parents[cell.y * cols + cell.x].dist;

        struct coord_t directions[4] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        for(int i = 0; i < 4; i++) {
            struct coord_t next = {
                cell.y + directions[i].y,
                cell.x + directions[i].x
            };
            if(0 <= next.y && next.y < rows && 0 <= next.x && next.x < cols && dist + 1 < dist_parents[next.y * cols + next.x].dist && field[next.y * cols + next.x] != '#') {
                dist_parents[next.y * cols + next.x].dist = dist + 1;
                dist_parents[next.y * cols + next.x].parent = cell;
                *queue_tail++ = next;
            }
        }

        char c = field[cell.y * cols + cell.x];
        if('A' <= c && c <= 'Z') {
            for(int j = 0; j < 2; j++) {
                struct coord_t next = portals[c - 'A'][j];
                if(dist + 1 < dist_parents[next.y * cols + next.x].dist) {
                    dist_parents[next.y * cols + next.x].dist = dist + 1;
                    dist_parents[next.y * cols + next.x].parent = cell;
                    *queue_tail++ = next;
                }
            }
        }
    }

    free(queue);

    unsigned dist = dist_parents[cell2.y * cols + cell2.x].dist;
    if(dist == -1U) {
        *path = NULL;
        return 0;
    }
    int path_len = dist + 1;

    *path = calloc(path_len, sizeof(struct coord_t));
    if(*path == NULL) {
        free(dist_parents);
        return 0;
    }

    struct coord_t* tail = *path + path_len;

    struct coord_t cell = cell2;
    while(cell.y != cell1.y || cell.x != cell1.x) {
        *--tail = cell;
        cell = dist_parents[cell.y * cols + cell.x].parent;
    }
    *--tail = cell;

    free(dist_parents);

    return path_len;
}


static void choose_free_point(char* field, int cols, int rows, struct coord_t* cell) {
    do {
        cell->y = rand() % rows;
        cell->x = rand() % cols;
    } while(field[cell->y * cols + cell->x] != ' ');
}


static int choose_far_points(char* field, int cols, int rows, struct coord_t** path) {
    *path = NULL;

    int path_len = -1;
    for(int i = 0; i < 5; i++) {
        struct coord_t cell1, cell2;
        choose_free_point(field, cols, rows, &cell1);
        choose_free_point(field, cols, rows, &cell2);

        struct coord_t* tmp_path;
        int tmp_path_len = find_path(field, cols, rows, cell1, cell2, &tmp_path);
        if(tmp_path_len > path_len) {
            path_len = tmp_path_len;
            *path = tmp_path;
        } else {
            free(tmp_path);
        }
    }

    return path_len;
}


static void dfs(int y, int x, int width, int height, char* visited, char* field) {
    visited[y * width + x] = 1;
    struct coord_t targets[4] = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
    shuffle((char*)targets, 4, sizeof(struct coord_t));
    for(int i = 0; i < 4; i++) {
        int dy = targets[i].y;
        int dx = targets[i].x;
        int y1 = y + dy;
        int x1 = x + dx;
        if(0 <= y1 && y1 < height && 0 <= x1 && x1 < width && !visited[y1 * width + x1]) {
            dfs(y1, x1, width, height, visited, field);
            field[(y * 2 + 1 + dy) * (2 * width + 1) + (x * 2 + 1 + dx)] = ' ';
        }
    }
}


int generate_maze(char* field, int height, int width, int add_maze, int points, int portals) {
    int cols = 2 * width + 1;
    int rows = 2 * height + 1;

    char* visited = NULL;
    struct coord_t* cells = NULL;

    int success = 0;

restart:
    if(add_maze) {
        for(int i = 0; i < height; i++) {
            memset(field + 2 * i * cols, '#', cols);
            for(int j = 0; j < cols; j++) {
                field[(2 * i + 1) * cols + j] = "# "[j % 2];
            }
        }
        memset(field + 2 * height * cols, '#', cols);

        if(visited == NULL) {
            visited = calloc(height, width);
            if(visited == NULL) {
                goto err;
            }
        }

        if(cells == NULL) {
            cells = calloc(width * height, sizeof(struct coord_t));
            if(cells == NULL) {
                goto err;
            }
        }

        for(int y = 0; y < height; y++) {
            for(int x = 0; x < width; x++) {
                cells[y * width + x] = (struct coord_t){y, x};
            }
        }
        shuffle((char*)cells, height * width, sizeof(struct coord_t));
        for(int i = 0; i < height * width; i++) {
            struct coord_t cell = cells[i];
            if(!visited[cell.y * width + cell.x]) {
                dfs(cell.y, cell.x, width, height, visited, field);
            }
        }
    } else {
        memset(field, '#', cols);
        for(int i = 1; i < 2 * height; i++) {
            field[i * cols] = '#';
            memset(field + i * cols + 1, ' ', cols - 2);
            field[i * cols + cols - 1] = '#';
        }
        memset(field + 2 * height * cols, '#', cols);
    }

    for(char c = 'A'; c < 'A' + portals; c++) {
        struct coord_t* path;
        int path_len = choose_far_points(field, cols, rows, &path);
        if(path_len < 5) {
            free(path);
            goto restart;
        }

        struct coord_t cell1 = path[0];
        struct coord_t cell2 = path[path_len - 1];
        field[cell1.y * cols + cell1.x] = c;
        field[cell2.y * cols + cell2.x] = c;

        struct coord_t* p = path;
        for(int i = 0; i < path_len; i++) {
            struct coord_t cell = path[i];
            if(field[cell.y * cols + cell.x] == ' ' && (cell.y % 2 == 0 || cell.x % 2 == 0)) {
                *p++ = path[i];
            }
        }
        path_len = p - path;
        if(path_len == 0) {
            free(path);
            goto restart;
        }

        struct coord_t cell = path[rand() % path_len];
        field[cell.y * cols + cell.x] = '#';

        free(path);
    }

    for(int i = 0; i < points; i++) {
        struct coord_t cell;
        choose_free_point(field, cols, rows, &cell);
        field[cell.y * cols + cell.x] = '.';
    }

    struct coord_t cell;
    choose_free_point(field, cols, rows, &cell);
    field[cell.y * cols + cell.x] = '@';

    success = 1;

err:
    free(visited);
    free(cells);
    return success;
}


int main(int argc, char** argv) {
    if(argc != 6) {
        fprintf(stderr, "Invalid number of arguments\n");
        return 1;
    }

    int height = atoi(argv[1]);
    int width = atoi(argv[2]);
    int add_maze = strcmp(argv[3], "1") == 0;
    int points = atoi(argv[4]);
    int portals = atoi(argv[5]);
    if(height <= 0 || width <= 0 || points < 0 || portals < 0) {
        fprintf(stderr, "Invalid arguments\n");
        return 1;
    }

    int seed;
    if(getrandom(&seed, sizeof(int), 0) == -1) {
        perror("getrandom");
        return 1;
    }
    srand(seed);

    char* field = calloc(2 * width + 1, 2 * height + 1);
    if(field == NULL) {
        fprintf(stderr, "Allocation failed\n");
        return 1;
    }

    if(!generate_maze(field, height, width, add_maze, points, portals)) {
        free(field);
        fprintf(stderr, "Generation failed\n");
        return 1;
    }

    for(int i = 0; i < 2 * height + 1; i++) {
        printf("%.*s\n", 2 * width + 1, field + i * (2 * width + 1));
    }
    free(field);

    return 0;
}
