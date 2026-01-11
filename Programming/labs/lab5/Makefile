# FLAGS = -Wall -Wextra -O0 -g -fsanitize=address
FLAGS = -Wall -Wextra -O0 -g

all : task1 task2 additional
task1 : task1.c
	gcc $^ -o $@ $(FLAGS)
task2 : task2.c
	gcc $^ -o $@ $(FLAGS)
additional : additional.c
	gcc $^ -o $@ $(FLAGS)
clean :
	rm task1 task2
