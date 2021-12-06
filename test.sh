# ---------
#  Type-Bp
# ---------
##./main.py -m OLTF  -o PR3 -s SF BF -d GAS       --plot DAMP2DAMP --plotrefs 334 --plotgrds DAMPED
# 334: only SF_GAS_DAMP

###./main.py -m PLANT -o PR3 -s SF BF -d GAS       --plot TEST2DAMP --plotrefs 353 303 --plotgrds DAMPED SAFE
# 303: SAFE
# 336: GASDAMP at PR3_SF(1.0), 
# 337: GASDAMP at PR3_SF(1.0), PR3_BF(0.3)
# 350: DAMPED state

###./main.py -m PLANT -o PR3 -s BF -d L T Y        --plot TEST2DAMP --plotrefs 354 292 --plotgrds DAMPED SAFE
###./main.py -m PLANT -o PR3 -s BF -d R P V        --plot TEST2DAMP --plotrefs 354 292 --plotgrds DAMPED SAFE
###./main.py -m PLANT -o PR3 -s BF -d L P Y        --plot TEST2DAMP --plotrefs 354 292 --plotgrds DAMPED SAFE
# 292: SAFE(before337)
# 338: 337 w/o BF and IM control
# 341: 337 + BFDAMP(w/o BF_V)
# 351: DAMPED state

./main.py -m PLANT -o PR3 -s IM -d L T Y        --plot TEST2DAMP --plotrefs 357 358 --plotgrds DAMPED SAFE
./main.py -m PLANT -o PR3 -s IM -d R P V        --plot TEST2DAMP --plotrefs 357 358 --plotgrds DAMPED SAFE
./main.py -m PLANT -o PR3 -s IM -d L P Y        --plot TEST2DAMP --plotrefs 357 358 --plotgrds DAMPED SAFE
# 281: SAFE(before337)
# 358: SAFE
# 342: 341 w/o IM control
# 343: 341 + IMDAMP (w/o IM_V)
# 346: 341 + IMDAMP (w/o IM_V) weak
# 352: DAMPED state

# ./main.py -m PLANT -o PRM PR2 PR3 -s BF -d H1 H2 H3     --plot COIL2INF  --plotrefs 306 --plotxlim 1e-2 10 # OK 
# ./main.py -m PLANT -o PRM PR2 PR3 -s BF -d V1 V2 V3     --plot COIL2INF  --plotrefs 306 --plotxlim 1e-2 10 # OK 
# ./main.py -m PLANT -o PRM PR2 PR3 -s IM -d H1 H2 H3     --plot COIL2INF  --plotrefs 259 --plotxlim 1e-2 10 # OK 
# ./main.py -m PLANT -o PRM PR2 PR3 -s IM -d V1 V2 V3     --plot COIL2INF  --plotrefs 259 --plotxlim 1e-2 10 # OK 


# ---------
#  Type-B
# ---------
# ./main.py -m PLANT -o BS SRM SR2 SR3 -s F0 F1 BF -d GAS --plot TEST2DAMP --plotrefs 308 --plotxlim 1e-2 10 # OK
# ./main.py -m PLANT -o BS SRM SR2 SR3 -s IM -d L T Y     --plot TEST2DAMP --plotrefs 309 --plotxlim 1e-2 10 # OK 
# ./main.py -m PLANT -o BS SRM SR2 SR3 -s IM -d R P V     --plot TEST2DAMP --plotrefs 309 --plotxlim 1e-2 10 # OK
# ./main.py -m PLANT -o BS SRM SR2 SR3 -s IM -d H1 H2 H3  --plot COIL2INF  --plotrefs 310 --plotxlim 1e-2 10 # OK
# ./main.py -m PLANT -o BS SRM SR2 SR3 -s IM -d V1 V2 V3  --plot COIL2INF  --plotrefs 310 --plotxlim 1e-2 10 # OK

# #Type-A
# ./main.py -m PLANT -o ITMX ETMX -s IP -d L T Y          --plot TEST2DAMP --plotrefs 311    --plotxlim 1e-2 10 # OK
# ./main.py -m PLANT -o ITMX ETMX -s IP -d H1 H2 H3       --plot COIL2INF  --plotrefs 312    --plotxlim 1e-2 10 # OK
