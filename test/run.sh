
doxygen doxygen.conf

NAME=test
mkdir -p wasmOut

python ../parser.py doxygenOut/xml/index.xml > wasmOut/api.json
python ../normalize.py wasmOut/api.json > wasmOut/api_std.json
python ../genWebIDL.py wasmOut/api_std.json > wasmOut/api.idl

cd ..

python gen.py $NAME/wasmOut/api_std.json wasm/wasm.cpp.jinja2 > $NAME/wasmOut/wasm_glue.cpp
python gen.py $NAME/wasmOut/api_std.json wasm/wasm.js.jinja2 > $NAME/wasmOut/wasm_glue.js

