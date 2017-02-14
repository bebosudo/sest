// SEST library. 2017, Alberto Chiusole

#ifndef __SEST_H__
#define __SEST_H__

#include <Client.h>
#include <cstdint>
#include <string>

const int MAX_NUMBER_FIELDS = 3;

class SEST {
    std::string _address;
    std::string _host;
    std::string _path;
    Client& _client;
    std::string _fields[MAX_NUMBER_FIELDS];

    bool is_url_valid() const;
    void extract_domain();
    void extract_path();

  public:
    SEST(Client& client, std::string address);
    ~SEST();

    bool push(int value);
    // void print() const;
};

#endif
