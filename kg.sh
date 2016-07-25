#!/bin/sh
#!/bin/bash

echo "digraph G {  shot->I [ label="dc" ]; sleep->shot [ label="dc" ]; sleep->my [ label="poss" ]; elephant->sleep [ label="shot" ]; sleep->elephant [ label="shot" ]; }" | dot -Tpng > ./ie.png