
namespace myns {
typedef float YourFloat;

template<T>
class TestClass
{
    int m_p;
public:
    int method(int a, char* b, Test* c, Test d);
public:
    TestClass( float f );
    YourFloat m_f;

    struct InClass {
        static void foo();
    };

    enum EnumType {
        kA, kB = 2
    };

    InClass testValue(InClass val);
};

TestClass<int> g_bar;
void globalFunc(const std::string& name) {
}

}