// SEST library.
// Alberto Chiusole -- 2017.

#include "SEST.h"
#include "Arduino.h"
// #include <algorithm>
#include <cstdint>
#include <math.h>
#include <string>

const unsigned int MS_WAIT_BEFORE_TIMEOUT = 5000;

SEST::SEST(Client& client, const std::string& address,
           const std::string& write_key)
        : _client(client), _address(address), _write_key(write_key) {

    // Strip newlines from the URI.
    // Can't do it with algorithm due to a bug in the esp8266/arduino package:
    // https://github.com/platformio/platformio-core/issues/653
    for (int p = _address.find("\n"); p != (int)std::string::npos;
         p = _address.find("\n")) {
        _address.erase(p, 1);
    }

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
        return std::string("");
    return std::string(buffer);
}

std::string number_to_string(double number) {
    /* Home-made version of dtostrf, because it doesn't seem to be supported
    on the esp8266: http://stackoverflow.com/a/27652012
    */

    int dec_precision = 4;

    int int_part = floor(number);
    int dec_part = floor((number - int_part) * pow(10, dec_precision));

    std::string buffer = number_to_string(int_part);
    buffer += ".";
    buffer += number_to_string(dec_part);

    return std::string(buffer);
}

bool SEST::set_field(unsigned int field_no, int value) {
    if (field_no <= MAX_NUMBER_FIELDS and field_no != 0) {
        // The user creates field types counting from 1, and we remap the
        // position to a position one step lower in order to save it into
        // C-style arrays.
        _field_arr[field_no - 1] = number_to_string(value);
        return true;
    }
    return false;
}

bool SEST::set_field(unsigned int field_no, double value) {
    if (field_no <= MAX_NUMBER_FIELDS and field_no != 0) {
        // The user creates field types counting from 1, and we remap the
        // position to a position one step lower in order to save it into
        // C-style arrays.
        _field_arr[field_no - 1] = number_to_string(value);
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
            // As we already did in the set_field method, we need to move the
            // position of the field by one step.
            body += number_to_string((int)i + 1);
            body += "=";
            // The array is already made of strings.
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
    std::string to_be_discarded;
    push(to_be_discarded);
}

bool SEST::push(std::string& collect_response) {
    std::string body = _get_fields_encoded();

    collect_response = collect_response + "Trying to connect to server '" +
                       _host + "', pointing to path '/" + _path + "'.\n\n";
    if (!_connect_to_server()) {
        _read_http_response(collect_response);
        return false;
    } else if (_write_key == "") {
        collect_response += "Missing writing key for the chosen channel.";
        return false;
    } else if (body == "") {
        collect_response += "Missing body message (no fields to send).";
        return false;
    }

    std::string header = "POST /";
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

    header += number_to_string((int)body.length());
    header += "\n\n";

    if (!_client.print(header.c_str())) {
        collect_response += "ERROR when uploading.";
        return false;
    }
    if (!_client.print(body.c_str())) {
        collect_response += "ERROR when uploading.";
        return false;
    }

    collect_response += "Attempting to send:" + header + body + "\n\n";
    _reset_fields();

    if (_read_http_response(collect_response)) {
        collect_response += "Package reached destination.";
        return true;
    }
    collect_response += "Some problems arose while sending.";
    return false;
}

bool SEST::_read_http_response(std::string& response) const {
    long unsigned int start_time = millis();

    // Wait until the client has something to say, or until enough time has
    // passed before receiving a response. Reason to use delay:
    // https://github.com/esp8266/Arduino/issues/34#issuecomment-102302835
    while (_client.available() == 0 &&
           millis() - start_time < MS_WAIT_BEFORE_TIMEOUT) {
        delay(100);
    }

    // If the client still has nothing to say, it means that timeout
    // arrived.
    if (_client.available() == 0) {
        response +=
            " ERROR: timeout when waiting for the server to reply (address: ";
        response += _address;
        response += ", TCP port: ";
        response += number_to_string((int)_port);
        response += ").";
        return false;
    }

    size_t s = 100;
    char buffer[s];
    size_t size_read = 0;
    while (_client.available() != 0) {
        size_read += _client.read((uint8_t*)buffer, s);
        // Empty the buffer on the ESP wifi module.
        // _client.flush();
        response += std::string(buffer);
    }

    return size_read == s;
}
