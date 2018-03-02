#include<iostream>
#include<set>
#include<string>

using namespace std;

void mincut(const string& str, const set<string>& dict)
{
	string str1 = str.substr(0, 1);
	if (dict.count(str1) == 0)
		cout << "n/a" << endl;
	int Length = str.size();
	str1 = str.substr(0, Length);

	while (str1.size()) {
		int Length = str1.size();
		int length = Length;
		for (; length >= 0; --length) {
			string str2 = str1.substr(0, length);
			if (dict.count(str2)) {
				cout << str2 << " ";
				break;
			}
		}
		str1 = str1.substr(length, Length - length);
	}
	cout<<endl;
}

int main(int argc, const char * argv[])
{
	string strS;
	string dictStr;
	int nDict;
	set<string> dict;

	cin >> strS;
	cin >> nDict;
	for (int i = 0; i < nDict; i++)
	{
		cin >> dictStr;
		dict.insert(dictStr);
	}
	mincut(strS, dict);

	return 0;
}
