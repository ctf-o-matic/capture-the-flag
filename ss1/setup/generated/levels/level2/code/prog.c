#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  printf("Current time: ");
  fflush(stdout);
  system("date");
  return 0;
}
