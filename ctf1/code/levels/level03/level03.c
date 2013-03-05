#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

#define NUM_FNS 4

typedef int (*fn_ptr)(const char *);

int to_upper(const char *str)
{
  printf("Uppercased string: ");
  int i = 0;
  for (i; str[i]; i++)
    putchar(toupper(str[i]));
  printf("\n");
  return 0;
}

int to_lower(const char *str)
{
  printf("Lowercased string: ");
  int i = 0;
  for (i; str[i]; i++)
    putchar(tolower(str[i]));
  printf("\n");
  return 0;
}

int capitalize(const char *str)
{
  printf("Capitalized string: ");
  putchar(toupper(str[0]));
  int i = 1;
  for (i; str[i]; i++)
    putchar(tolower(str[i]));
  printf("\n", str);
  return 0;
}

int length(const char *str)
{
  int len = 0;
  for (len; str[len]; len++) {}

  printf("Length of string '%s': %d\n", str, len);
  return 0;
}

int run(const char *str)
{
  // This function is now deprecated.
  return system(str);
}

int truncate_and_call(fn_ptr *fns, int index, char *user_string)
{
  char buf[64];
  // Truncate supplied string
  strncpy(buf, user_string, sizeof(buf) - 1);
  buf[sizeof(buf) - 1] = '\0';
  return fns[index](buf);
}

int main(int argc, char **argv)
{
  int index;
  fn_ptr fns[NUM_FNS] = {&to_upper, &to_lower, &capitalize, &length};

  if (argc != 3) {
    printf("Usage: ./level03 INDEX STRING\n");
    printf("Possible indices:\n[0] to_upper\t[1] to_lower\n");
    printf("[2] capitalize\t[3] length\n");
    exit(-1);
  }

  // Parse supplied index
  index = atoi(argv[1]);

  if (index >= NUM_FNS) {
    printf("Invalid index.\n");
    printf("Possible indices:\n[0] to_upper\t[1] to_lower\n");
    printf("[2] capitalize\t[3] length\n");
    exit(-1);
  }

  return truncate_and_call(fns, index, argv[2]);
}
