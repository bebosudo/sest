// SEST library. 2017, Alberto Chiusole

#include "SEST.h"
#include <algorithm>
#include <iostream>
#include <string>

SEST::SEST(Client& client, std::string address)
        : _client(client), _address(address) {
    // Strip newlines from the URI.
    _address.erase(std::remove(_address.begin(), _address.end(), '\n'),
                   _address.end());

    // Remove the possible heading http(s) the user could insert.
    std::string prot = "http://";
    if (_address.substr(0, prot.length()) == prot) {
        _address = _address.substr(prot.length(), std::string::npos);
    }
    prot = "https://";
    if (_address.substr(0, prot.length()) == prot) {
        _address = _address.substr(prot.length(), std::string::npos);
    }

    if (is_url_valid()) {
        extract_domain();
        extract_path();
    }
}

SEST::~SEST() {}

bool SEST::is_url_valid() const {
    // I consider an host to be valid when there's at least a period that
    // separates the 1st to the 2nd level domain name.
    std::size_t pos = _address.find(".");
    return pos != std::string::npos;
}

void SEST::extract_domain() {
    // Given an url, extract the domain.
    std::size_t pos = _address.find("/");

    if (pos != std::string::npos) {
        _host = _address.substr(0, pos);
    }
    // If a slash isn't found, the address saved is a domain.
}

void SEST::extract_path() {
    // Given an url, extract the path (the address following the domain), if
    // any.
    std::size_t pos = _address.find("/");

    if (pos != std::string::npos) {
        _path = _address.substr(pos + 1, std::string::npos);
    }
}

bool SEST::push(int value) {}

// void SEST::print() const { std::cout << _host << std::endl << _path <<
// std::endl;
// }
