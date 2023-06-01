
namespace myns {
typedef float YourFloat;

template<T>
class TestClass
{
    int m_p;
    int method();
public:
    TestClass( float f );
    YourFloat m_f;

    struct InClass {
        static void foo();
    };

    enum EnumType {
        kA, kB = 2
    };
};

TestClass<int> g_bar;
void globalFunc(char* name) {
}

}