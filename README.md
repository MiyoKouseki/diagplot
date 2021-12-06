# AutoMeasurement
## Usage

Run spectra measurement
> ./main.py -m SPECTRA -o PRM PR2 PR3 -s IM -d L T Y

Run transfer function measurement
> ./main.py -m PLANT -o PRM PR2 PR3 -s IM -d L T Y \
>           --rundiag TEST2DAMP --amp 5000 5000 5000 --bw 0.003 --ave 10

Plot the measured TFs
> ./main.py -m PLANT -o PRM PR2 PR3 -s IM -d L T Y \
>           --plot TEST2DAMP --ref 19 25 --xlim 1e-2 10

### About the Options

| Options | Descroption |
|:---|:---|
| -m | Measurement option. Choose from PLANT, OLTF, and SPECTRA. |
| -o | Optics. |
| -s | Stages. |
| -d | Degrees of freedom. |
| --run | Choose from TEST2DAMP, COIL2DAMP, COIL2INF, and DAMP2DAMP. |
| --run_amp | Excitation amplitude.|
| --run_bw | Frequency band width.|
| --run_ave | Average number.|
| --plot | Same as the rundiag options|
| --plot_ref| Reference numbers. |
| --plot_xlim| X-axis range of the plot.|

## For Developpers


