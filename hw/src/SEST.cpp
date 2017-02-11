// SEST library. 2017, Alberto Chiusole

#include "SEST.h"
#include <string>

SEST::SEST(Client& client, uint32_t ch_id): client(client), ch_id(ch_id) {}

SEST::~SEST() {}


bool SEST::push(int value);
