#! /usr/bin/bash
./main.py -m PLANT -o ITMX ETMX -s IP -d L T Y    --run TEST2DAMP  --runbw 0.003 --runave 5 --runamp 10000 10000 10000 --yes
./main.py -m PLANT -o ITMX ETMX -s IP -d H1 H2 H3 --run COIL2INF   --runbw 0.003 --runave 5 --runamp 10000 10000 10000 --yes
