#include <iostream>
#include <vector>

extern "C" {
    // This function can be called by Python using 'ctypes'
    void analyze_packet_raw(unsigned char* buffer, int size) {
        // High-speed binary dissection logic here
        if (buffer[0] == 0x45) { // Simple IPv4 Check
            std::cout << "[C++] IPv4 Layer detected" << std::endl;
        }
    }
}
