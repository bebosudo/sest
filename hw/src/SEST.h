// SEST library. 2017, Alberto Chiusole

#ifndef __SEST_H__
#define __SEST_H__

#include <Client.h>
#include <cstdint>
#include <string>

const int MAX_NUMBER_FIELDS = 3;

class SEST {
    const char* _address;
    Client& _client;
    std::string _fields[MAX_NUMBER_FIELDS];

    char* extract_domain(const* char _add);
    char* extract_path(const* char _add);

  public:
    SEST(Client& client, const char* address);
    ~SEST();

    bool push(int value);
};


#endif
