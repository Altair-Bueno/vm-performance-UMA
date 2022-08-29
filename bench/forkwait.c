#include <stdio.h>
#define Nfork 50000

int main(int argc, char *argv[]) {
  int i, pid;
  for (i = 0; i < Nfork; i++) {
    pid = fork();
    if (pid < 0) {
      printf("Fork #%i failed\n", i);
      return -1;
    }
    if (pid == 0) return 0;
    waitpid(pid, NULL, 0);
  }
  return 0;
}

