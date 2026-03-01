#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// XOR Decryption: Common for obfuscated strings
void xor_cipher(const char* data, char key) {
    printf("XOR Result: ");
    for (size_t i = 0; i < strlen(data); i++) {
        printf("%c", data[i] ^ key);
    }
    printf("\n");
}

// Hex Decoder
void decode_hex(const char* hex) {
    printf("Hex Decoded: ");
    for (size_t i = 0; i < strlen(hex); i += 2) {
        char part[3] = {hex[i], hex[i+1], '\0'};
        printf("%c", (char)strtol(part, NULL, 16));
    }
    printf("\n");
}

int main(int argc, char** argv) {
    if (argc < 3) {
        printf("Usage: %s <mode: hex|xor> <data> [key for xor]\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "hex") == 0) {
        decode_hex(argv[2]);
    } else if (strcmp(argv[1], "xor") == 0 && argc == 4) {
        xor_cipher(argv[2], argv[3][0]);
    }
    return 0;
}
