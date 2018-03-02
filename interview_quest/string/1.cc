/**
 * 给定一个字符串S和有效单词的字典D，请确定可以插入到S中的最小空格数,
 * 使得最终的字符串完全由D中的有效单词组成，并输出解。如果没有解则
 * 应该输出n/a
 * 例如
 * 输入
 * S = "ilikealibaba"
 * D = ["i", "like", "ali", "liba", "baba", "alibaba"]
 * Example Output:
 * 输出
 * "i like alibaba"
 */
#include <iostream>
#include <set>
#include <string>
#include <sstream>

using namespace std;

void solution(const std::string &s, const std::set<std::string> &dict) {
    std::stringstream ss;

    for (size_t pos = 0; pos < s.size();) {
        size_t len = 0;
        for (len = s.size() - pos; len > 0; --len) {
            std::string str = s.substr(pos, len);
            if (dict.count(str)) {
                if (pos == 0) {
                    ss << str;
                } else {
                    ss << "*" << str;
                }
                pos += len;
                break;
            }
        }
        if (len == 0) {
            // not found
            cout << "n/a" << endl;
            return;
        }
    }
    cout << ss.str() << endl;
}

int main(int argc, char **argv)
{
    std::string s("ilikealibaba");
    std::set<std::string> dict = {"i", "like", "ali", "liba", "baba", "alibaba"};
    solution(s, dict);
    return 0;
}
