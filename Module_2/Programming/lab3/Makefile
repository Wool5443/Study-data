SRC = $(wildcard *.c)
TARGET = $(patsubst %.c, %, $(SRC))

FLAGS = -Wall -Wextra -O0 -g

all : $(TARGET)

% : %.c
	gcc $(FLAGS) $^ -o $@

clean:
	rm $(TARGET)
