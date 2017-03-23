#include <cassert>
#include <sstream>
#include <iostream>
#include <boost/optional/optional_io.hpp>


int main()
{
	boost::optional<int> o1 = 1, oN = boost::none;
	boost::optional<int> x1, x2;
	std::stringstream s;
	s << o1 << oN;
	std::cout << o1 << oN << std::endl;
	s >> x1 >> x2;
	assert (o1 == x1);
	assert (oN == x2);
}
