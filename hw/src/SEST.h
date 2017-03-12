// SEST library.
// Alberto Chiusole -- 2017.

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
    bool _read_http_response(std::string& response) const;

  public:
    SEST(Client& client, const std::string& address,
         const std::string& write_key);
    ~SEST();

    bool set_field(unsigned int field_no, int value);
    bool set_field(unsigned int field_no, double value);
    void set_port(unsigned int port);
    bool push();
    bool push(std::string& collect_response);
};

#endif
