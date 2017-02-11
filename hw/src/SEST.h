// SEST library. 2017, Alberto Chiusole

#ifndef __SEST_H__
#define __SEST_H__

#include <Client.h>
#include <cstdint>
#include <string>

const int MAX_NUMBER_FIELDS = 3;

class SEST {
    uint32_t ch_id;
    std::string fields[MAX_NUMBER_FIELDS];
  public:
    SEST(Client& client, uint32_t ch_id);
    ~SEST();

    bool push(int value);
};


#endif
