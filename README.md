# DTNtuples
Ntuples for the analysis of the CMS drift tubes detector performance

## Preliminary instructions
**Note**: 
In the present days this code is evolving fast, hence the installation recipe may change often. Please keep an eye on this page to check for updates.

### Installation:
```bash
cmsrel CMSSW_13_0_0
cd CMSSW_13_0_0/src/
cmsenv

git cms-init
# To be updated
git cms-merge-topic oglez:Phase2_DTAB7Unpacker_v11.6
git clone https://github.com/battibass/DTNtuples.git DTDPGAnalysis/DTNtuples

scramv1 b -j 5
```

### Ntuple production:
```
cd DTDPGAnalysis/DTNtuples/test/
cmsRun dtDpgNtuples_slicetest_cfg.py nEvents=10000
# or
cmsRun dtDpgNtuples_phase2_cfg.py nEvents=10000
```

> [!NOTE]
> *Update to Ntuples with shower algorithm emulation: 07/09/25*
> ### Installation:
> ```bash
> cmsrel CMSSW_15_1_0_pre2
> cd CMSSW_15_1_0_pre2/src
> cmsenv
> git cms-init
> # To be updated with the showers producer
> git cms-addpkg L1Trigger/DTTriggerPhase2
> git clone git@github.com:dtp2-tpg-am/L1Trigger-DTTriggerPhase2.git L1Trigger/DTTriggerPhase2/data -b newluts
> git remote add destrada git@github.com:DanielEstrada971102/cmssw.git
> git checkout destrada/showers_cmssw_15x
> # Now install the code to produce ntuples
> git clone git@github.com:DanielEstrada971102/DTNtuples.git DTDPGAnalysis/DTNtuples -b shower_ntuples
> 
> scramv1 b -j 5
> ```
> 
> ### Ntuple production:
> ```
> cd DTDPGAnalysis/DTNtuples/test/
> cmsRun dtDpgNtuples_phase2_wshowers_cfg.py nEvents=1000
> ```
> See a few more details in `test/README.md`.

### Analysis:
```
root -b
root [0] .x loadExampleAnalysis.C

root [1] DTNtupleExampleAnalyzer analysis("DTDPGNtuple_run333510.root","results.root")
// or
root [1] DTNtupleExampleAnalyzer analysis("DTDPGNtuple_11_0_2_Phase2_Simulation.root","results.root")

root [2] analysis.Loop()
```
