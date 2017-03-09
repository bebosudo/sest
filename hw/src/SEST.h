// SEST library. 2017, Alberto Chiusole

#ifndef __SEST_H__
#define __SEST_H__

#include <Client.h>
#include <string>

const int MAX_NUMBER_FIELDS = 10;
const std::string USER_AGENT = "SEST_CLIENT";
const std::string HTTP_WRITE_KEY = "X-SEST-Write-Key";

class SEST {
    Client& _client;
    std::string _address;
    std::string _write_key;
    std::string _host;
    std::string _path;
    unsigned int _port;

    std::string _field_arr[MAX_NUMBER_FIELDS];

    bool is_url_valid() const;
    void extract_domain();
    void extract_path();
    bool _connect_to_server();
    std::string _get_fields_encoded() const;
    void _reset_fields();

  public:
    SEST(Client& client, const std::string& address,
         const std::string& write_key);
    ~SEST();

    bool set_field(unsigned int field_no, int value);
    std::string set_field(unsigned int field_no, double value);
    void set_port(unsigned int port);
    void print() const;
    std::string push();
};

#endif
