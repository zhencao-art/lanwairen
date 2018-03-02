
bool get_next_token(const std::string &s, size_t &pos, const char *delimit,
                    std::string *token) {
    size_t start = s.find_first_not_of(delimit);
    if (start < 0) {
        pos = s.size();
        return false;
    }
    size_t end = s.find_first_of(delimit);
    if (end < 0) {
        pos = end = s.size();
    } else {
        pos = end + 1;
    }
    *token = s.substr(start, end - start);
    return true;
}

void string_split_vec(const std::string &s, const char *delimit,
                      std::vector<std::string> *out) {
    size_t pos = 0;
    std::string token;

    while (pos < s.size()) {
        if (get_next_token(s, pos, delimit, &token)) {
            if (token.size()) {
                out->push_back(token);
            }
        }
    }
}
