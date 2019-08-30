# APV Baseline Generation

## Quickstart
To run, do :
```
root -l -q generateAPVBaselines.C+
```
This needs a fairly recent version of root with TProcessExecutor.  It works in CMSSW_11_0_0_pre4, which comes with root 6.14.
It can also run outside of CMSSW, as long as you have root.  One way to get a recent version of root is to do:
```
source /cvmfs/sft.cern.ch/lcg/views/LCG_95/x86_64-centos7-gcc7-opt/setup.sh
```

## Inputs
There is an example input file in the repository, scdFits.root (most recent at time of writing).
This contains the TF1 representing strip charge distributions (SCD) and occupancy.
The TF1 are results of a fit to the actual SCD, and the occupancy was also derived from the SCD.
N.B. The code to derive these fits is not yet in this repository.
