#include <stdio.h>
#include <stdlib.h>

const int UID = 1102;

int main(int argc, char **argv)
{
  setreuid(UID, UID);
  printf("Current time: ");
  fflush(stdout);
  system("date");
  return 0;
}
