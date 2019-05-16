#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

char
char_at(char *str, int pos)
{
	return pos < strlen(str) ? str[pos] : 0;
}

void
taunt()
{
	if (!fork()) {
		execl("/bin/echo", "/bin/echo", "Ha ha, your password is incorrect!", NULL);
		exit(1);
	}
}

int
main(int argc, char **argv)
{
	char *correct, *guess, *file, guess_char, true_char;
	int known_incorrect = 0, i;
	FILE *f;

	if (argc != 3) {
		fprintf(stderr, "Usage: %s file guess\n\nCompares the contents of a file with a guess, and\nmakes fun of you if you didn't get it right.\n", argv[0]);
		exit(1);
	}

	file = argv[1];
	guess = argv[2];

	if (!(correct = malloc(1024))) {
		fprintf(stderr, "Error allocating buffer\n");
		exit(1);
	}

	if (!(f = fopen(file, "r"))) {
		fprintf(stderr, "Error opening file: %s\n", file);
		exit(1);
	}

	if (!fgets(correct, 1024, f)) {
		fprintf(stderr, "Error reading file: %s\n", file);
		exit(1);
	}

	if (correct[strlen(correct)-1] == '\n')
		correct[strlen(correct)-1] = '\0';

	fprintf(stderr, "Welcome to the password checker!\n");

	for (i = 0; i < strlen(guess); i++) {
		guess_char = char_at(guess, i);
		true_char = char_at(correct, i);
		fprintf(stderr, ".");
		if (!known_incorrect && (guess_char != true_char)) {
			known_incorrect = 1;
			taunt();
		}
	}

	if (!known_incorrect && strlen(guess) != strlen(correct)) {
		known_incorrect = 1;
		taunt();
	}

	fprintf(stderr, "\n");

	if (!known_incorrect) {
		fprintf(stderr, "Wait, how did you know that the password was %s?\n", correct);
	}

	return 0;
}
