#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  // circumvent busybox ash dropping privileges
  setreuid(geteuid(), geteuid());

  printf("Current time: ");
  fflush(stdout);
  system("date");
  return 0;
}
