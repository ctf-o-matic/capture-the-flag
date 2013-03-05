#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void fun(char *str)
{
  char buf[1024];
  strcpy(buf, str);
}

int main(int argc, char **argv)
{
  if (argc != 2) {
    printf("Usage: ./level04 STRING");
    exit(-1);
  }
  fun(argv[1]);
  printf("Oh no! That didn't work!\n");
  return 0;
}
