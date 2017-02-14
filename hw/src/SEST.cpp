// SEST library. 2017, Alberto Chiusole

#include "SEST.h"
#include <string>

SEST::SEST(Client& client, const char* address): _client(client), _address(address) {}

SEST::~SEST() {}

char* SEST::extract_domain(const char* _add) {
    // Given an url, extract the domain.
    char* todo;
    return todo;
}

char* SEST::extract_path(const char* _add) {
    // Given an url, extract the path (the address following the domain).
    char* todo;
    return todo;
}

bool SEST::push(int value) {};
