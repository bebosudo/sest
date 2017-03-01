// SEST library. 2017, Alberto Chiusole

#include "SEST.h"
#include <algorithm>
#include <cstdint>
#include <string>

SEST::SEST(Client& client, const std::string& address,
           const std::string& write_key)
        : _client(client), _address(address), _write_key(write_key) {
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
    } else {
        _host = "";
        _path = "";
    }

    // The port can be changed with the set_port method.
    _port = 80;
}

SEST::~SEST() {}

void SEST::set_port(unsigned int port) { _port = port; }

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

std::string number_to_string(int number) {
    char buffer[64];
    int status = snprintf(buffer, sizeof buffer, "%d", number);

    if (status < 0)
        return "";
    return std::string(buffer);
}

std::string number_to_string(float number) {
    char buffer[64];
    int status = snprintf(buffer, sizeof buffer, "%f", number);

    if (status < 0)
        return "";
    return std::string(buffer);
}

bool SEST::set_field(unsigned int field_no, int value) {
    if (field_no <= MAX_NUMBER_FIELDS) {
        // The user creates field types counting from 1.
        field_no--;
        // TODO: check whether the value has to be saved as a string.
        _field_arr[field_no] = number_to_string(value);
        // _field_arr[field_no] = value;
        return true;
    }
    return false;
}

bool SEST::set_field(unsigned int field_no, float value) {
    if (field_no <= MAX_NUMBER_FIELDS) {
        // The user creates field types counting from 1.
        field_no--;
        // TODO: check whether the value has to be saved as a string.
        _field_arr[field_no] = number_to_string(value);
        // _field_arr[field_no] = value;
        return true;
    }
    return false;
}

bool SEST::_connect_to_server() {
    if (_host == "") {
        return false;
    }
    return _client.connect(_host.c_str(), _port);
}

std::string SEST::_get_fields_encoded() const {
    std::string body = "";
    for (int i = 0; i < MAX_NUMBER_FIELDS; i++) {
        if (_field_arr[i] != "") {
            if (body != "") {
                body += "&";
            }
            body += "field";
            body += i + 1;
            body += "=";
            body += _field_arr[i];
        }
    }
    return body;
}

void SEST::_reset_fields() {
    for (int i = 0; i < MAX_NUMBER_FIELDS; i++) {
        _field_arr[i] = "";
    }
}

bool SEST::push() {
    std::string body = _get_fields_encoded();

    if (!_connect_to_server() || _write_key == "" || body == "") {
        return false;
    }
    std::string header = "POST ";
    header += _path;
    header += " HTTP/1.1\nHost: ";
    header += _host;
    header += "\nConnection: close\nUser-Agent: ";
    header += USER_AGENT;
    header += "\n";
    header += HTTP_WRITE_KEY;
    header += ": ";
    header += _write_key;
    header += "\nContent-Type: application/x-www-form-urlencoded\n";
    header += "Content-Length: ";

    header += body.length();
    header += "\n\n";

    if (!_client.print(header.c_str())) {
        return false;
    }
    if (!_client.print(body.c_str())) {
        return false;
    }
    _reset_fields();
    return true;
}

///////////////////////////////////////
// For DEBUGGING:
void SEST::print() const {
    printf("%s\n%s\n----\n", _host.c_str(), _path.c_str());
}
