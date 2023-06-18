SuperReflect

A customizable C++ reflection tool and webassembly binding generator, based on doxygen.

```
void registerAllClass() {
    Class clazz;
{% for aclazz in clazz %}
    clazz = registerClass("{{ aclazz.name }}");
    {% for field in aclazz.field %}
        registerField(clazz, "{{field.name}}");
    {% endfor %}
{% endfor %}
}
```
