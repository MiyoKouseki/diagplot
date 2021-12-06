time ./main.py -m PLANT -o BS SRM SR2 SR3 -s F0 F1 BF -d GAS         --run TEST2DAMP --runamp 2000 2000 2000                --runave 5 --runbw 0.003 --yes
time ./main.py -m PLANT -o BS SRM SR2 SR3 -s IM -d L T Y R P V       --run TEST2DAMP --runamp 2000 2000 2000 2000 2000 2000 --runave 5 --runbw 0.003 --yes
time ./main.py -m PLANT -o BS SRM SR2 SR3 -s IM -d H1 H2 H3 V1 V2 V3 --run COIL2INF  --runamp 3000 3000 3000 3000 3000 3000 --runave 5 --runbw 0.003 --yes
