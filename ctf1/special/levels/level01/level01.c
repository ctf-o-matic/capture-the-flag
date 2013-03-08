#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
  // circumvent busybox ash dropping privileges
  uid_t uid = geteuid();
  setreuid(uid, uid);

  printf("Current time: ");
  fflush(stdout);
  system("date");
  return 0;
}
