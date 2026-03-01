#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void decode_hex(const char* hex) {
    size_t len = strlen(hex);
    for (size_t i = 0; i < len; i += 2) {
        char part[3] = {hex[i], hex[i+1], '\0'};
        unsigned char b = (unsigned char)strtol(part, NULL, 16);
        printf("%c", b);
    }
    printf("\n");
}

int main(int argc, char** argv) {
    if (argc < 2) return 1;
    decode_hex(argv[1]);
    return 0;
}
