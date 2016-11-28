#include <functional>
#include <iostream>

using namespace std;


class class_1 {
	public:
		void fun(void) {
			cout << "class_1 fun is called" << endl;
		}

		void fun_1(int x) {
			cout << "class_1 fun_1 is called,x = " << x << endl;
		}
		
		void fun_2(int x,int y) {
			cout << "class_1 fun_1 is called,x = " << x << ",y= " << y << endl;
		}
};


class test {
	public:
		class_1 *m_class_1;

		template<typename Callback, typename...Args>
		auto class_1_map(Callback&& cb, Args&&...args) ->
		typename std::enable_if<std::is_void<decltype(cb(*m_class_1,std::forward<Args>(args)...))>::value,void>::type
		{
			cb(*m_class_1,std::forward<Args>(args)...);
		}

		test() {
			m_class_1 = new class_1;
		}
};


int main(int argc,char **argv)
{
	test t;

	t.class_1_map(std::mem_fn(&class_1::fun));
	t.class_1_map(std::mem_fn(&class_1::fun_1),1);
	t.class_1_map(std::mem_fn(&class_1::fun_2),1,2);

	return 0;
}
