#time ./main.py -m OLTF  -o PR3 -s SF -d GAS           --run DAMP2DAMP --runamp 20    --runave 5 --runbw 0.003 --yes
#time ./main.py -m OLTF -o PR3 -s BF SF -d GAS             --run DAMP2DAMP --runamp 20 20                               --runave 3 --runbw 0.03 --yes
#time ./main.py -m PLANT -o PR3 -s BF SF -d GAS            --run TEST2DAMP --runamp 5000 5000                           --runave 5 --runbw 0.01 --yes
#time ./main.py -m PLANT -o PR3 -s BF -d L T Y R P V       --run TEST2DAMP --runamp 10000 10000 10000 10000 10000 10000 --runave 5 --runbw 0.01 --yes
#time ./main.py -m PLANT -o PR3 -s IM -d L T Y R P V       --run TEST2DAMP --runamp 5000 5000 5000 5000 5000 5000       --runave 3 --runbw 0.003 --yes
time ./main.py -m PLANT -o PR3 -s TM -d L P Y       --run TEST2DAMP --runamp 100 100 100    --runave 3 --runbw 0.01 --yes
# time ./main.py -m PLANT -o PRM PR2 PR3 -s BF -d H1 H2 H3 V1 V2 V3 --run COIL2INF  --runamp 20000 20000 20000 20000 20000 20000 --runave 5 --runbw 0.003 --yes
# time ./main.py -m PLANT -o PRM PR2 PR3 -s IM -d H1 H2 H3 V1 V2 V3 --run COIL2INF  --runamp 5000 5000 5000 5000 5000 5000       --runave 5 --runbw 0.003 --yes
