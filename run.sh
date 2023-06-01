
cd test
doxygen doxygen.conf
cd ..

mkdir out

python parser.py test/doxygenOut/xml/index.xml > out/api.json
python gen.py out/api.json template.jinja2 > out/meta.cpp
