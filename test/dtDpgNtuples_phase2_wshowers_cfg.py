import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from Configuration.StandardSequences.Eras import eras

import subprocess
import sys

options = VarParsing.VarParsing()

options.register('globalTag',
                 '131X_mcRun4_realistic_v9', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Global Tag")

options.register('nEvents',
                 1000, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Maximum number of processed events")

options.register('inputFolder',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "EOS folder with input files")

options.register('secondaryInputFolder',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "EOS folder with input files for secondary files")

options.register('applySegmentAgeing',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True applies ageing to RECO segments")

options.register('applyTriggerAgeing',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True applies ageing to trigger emulators")

options.register('applyRpcAgeing',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True applies ageing to RPCs")

options.register('ageingInput',
                 '', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Input with customised ageing, used only if non ''")

options.register('ageingTag',
                 'MuonSystemAging', #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Tag for customised ageing")

options.register('applyRandomBkg',
                 False, #default value
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True applies random background to phase-2 digis and emulator")

options.register('ntupleName',
                 './ntuples/DTDPGNtuple_15_1_0_pre2_Phase2_Wshowers_Simulation.root', 
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Folder and name ame for output ntuple")

options.register('showThreshold',
                 6, 
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Threshold for shower algorithm emulator")
options.register('showerAlgorithm',
                 1, 
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.int,
                 "Algorithm to use for shower algorithm emulator")

options.register('testDataset',
                 'ZprimeToMuMu_M-6000_PU200', 
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.string,
                 "Test dataset to use if inputFolder not specified")

options.register('debug',
                 False, 
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True runs in debug mode")

options.parseArguments()

process = cms.Process("DTNTUPLES",eras.Phase2C9)

process.load('Configuration.StandardSequences.Services_cff')

if options.debug:
    process.load('FWCore.MessageService.MessageLogger_cfi')
    process.MessageLogger.cerr.FwkReport.reportEvery = 100

    process.MessageLogger = cms.Service(
        "MessageLogger",
        destinations = cms.untracked.vstring(
            'detailedInfo',
            'critical'
        ),
        detailedInfo = cms.untracked.PSet(
            threshold = cms.untracked.string('DEBUG')
        ),
        debugModules = cms.untracked.vstring(
            'dtTriggerPhase2AmPrimitiveDigis',
        )
    )

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(options.nEvents))

#process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.GlobalTag.globaltag = cms.string(options.globalTag)

process.source = cms.Source("PoolSource",                    
        fileNames = cms.untracked.vstring(),
        secondaryFileNames = cms.untracked.vstring()
)

def get_root_files(directory):
    """Helper function to recursively collect .root files using os.scandir."""
    root_files = []
    for entry in os.scandir(directory):
        if entry.is_dir():
            root_files.extend(get_root_files(entry.path))
        elif entry.is_file() and entry.name.endswith(".root"):
            root_files.append(entry.path)
    return root_files

testing_input_files = {
    # NOT AVAILABLE NOW : INVALID ?
    # 'root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRWinter20DIGI/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW/PU200_110X_mcRun4_realistic_v3-v2/40000/00E449AC-F2F5-BD49-9230-DF997178F38F.root',
    'ZprimeToMuMu_M-6000_PU200': [ # ~ 4000 events
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/120000/05c718cf-1618-4f60-8b6b-d49a0da7df1f.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/120000/06a231d0-f02c-489b-bb97-0ce8b5469848.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/120000/09452338-f2ba-4a86-a65a-da4179251cae.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/120000/09cfe03d-e128-4e58-89d4-1fcca2b95ccb.root',
    ],
    'DYToLL_M50_PU200': [ # ~640 events
        'root://xrootd-cms.infn.it//store/mc/Phase2Fall22DRMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30000/006da94b-e04a-4285-b355-061d34f1fd6a.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Fall22DRMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30000/0092f84d-f3df-4d96-b234-a250b77005f4.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Fall22DRMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30000/00e3a777-4dfe-4e0a-a61e-3c29c82a3511.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Fall22DRMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30000/0144e495-b696-43ce-8738-a02c837f1885.root',
    ]
}

def set_test_files():
    if options.testDataset not in testing_input_files :
        raise ValueError(f"Test dataset {options.testDataset} not recognized. Available test datasets: {list(testing_input_files.keys())}")
    process.source.fileNames = testing_input_files[options.testDataset]

if options.debug:
    set_test_files()

elif options.inputFolder != "" :
    process.source.fileNames = [
        "file://" + file_path for file_path in get_root_files(options.inputFolder)
    ]
    if options.secondaryInputFolder != "" :
        process.source.secondaryFileNames = [
            "file://" + file_path for file_path in get_root_files(options.secondaryInputFolder)
        ]
else:
    set_test_files()


process.TFileService = cms.Service('TFileService',
        fileName = cms.string(options.ntupleName)
    )

process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.Services_cff')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load('Configuration.Geometry.GeometryExtendedRun4D103Reco_cff')
process.load('Configuration.Geometry.GeometryExtendedRun4D103_cff')

# process.DTGeometryESModule.applyAlignment = False
# process.DTGeometryESModule.fromDDD = False

process.load("L1Trigger.DTTriggerPhase2.CalibratedDigis_cfi") 
process.load("L1Trigger.DTTriggerPhase2.dtTriggerPhase2PrimitiveDigis_cfi")
process.load("L1Trigger.DTTriggerPhase2.dtTriggerPhase2Showers_cfi")

# Load MB2 extrapolator for the genmuon
#from L1Trigger.L1TMuonOverlapPhase1.MuonExtrapolator_cfg import dispGen
#process.dispGen = dispGen

process.CalibratedDigis.dtDigiTag = "simMuonDTDigis"

process.dtTriggerPhase2ShowerV1 = process.dtTriggerPhase2Shower.clone()
process.dtTriggerPhase2ShowerV1.showerTaggingAlgo = options.showerAlgorithm
process.dtTriggerPhase2ShowerV1.threshold_for_shower = options.showThreshold
process.dtTriggerPhase2ShowerV1.debug = options.debug # Turn off debug mode

process.dtTriggerPhase2AmPrimitiveDigis = process.dtTriggerPhase2PrimitiveDigis.clone()
process.dtTriggerPhase2AmPrimitiveDigis.useRPC = True
process.dtTriggerPhase2AmPrimitiveDigis.debug = options.debug # Turn off debug mode
process.dtTriggerPhase2AmPrimitiveDigis.df_extended = 1 # Use extended data format
# process.dtTriggerPhase2AmPrimitiveDigis.showersTag = "dtTriggerPhase2ShowerV1"
# process.dtTriggerPhase2AmPrimitiveDigis.useShowers = False

process.load('RecoLocalMuon.Configuration.RecoLocalMuon_cff')
process.dt1DRecHits.dtDigiLabel = "simMuonDTDigis"
process.rpcRecHits.rpcDigiLabel = "simMuonRPCDigis"

from Configuration.StandardSequences.SimL1Emulator_cff import simBmtfDigis
process.simBmtfDigis = simBmtfDigis
process.simBmtfDigis.DTDigi_Source = "simDtTriggerPrimitiveDigis"
process.simBmtfDigis.DTDigi_Theta_Source = "simDtTriggerPrimitiveDigis"

process.load('DTDPGAnalysis.DTNtuples.dtNtupleProducer_phase2_cfi')

process.p = cms.Path(process.rpcRecHits
                     + process.dt1DRecHits
                     + process.dt4DSegments
                     + process.CalibratedDigis
                     + process.simBmtfDigis
                     + process.dtTriggerPhase2ShowerV1
                     + process.dtTriggerPhase2AmPrimitiveDigis
                     + process.dtNtupleProducer)

from DTDPGAnalysis.DTNtuples.customiseDtNtuples_cff import customiseForRandomBkg, customiseForRunningOnMC, customiseForFakePhase2Info, customiseForAgeing

customiseForRunningOnMC(process,"p")
customiseForFakePhase2Info(process)

if options.applyRandomBkg : 
    customiseForRandomBkg(process,"p")

customiseForAgeing(process,"p",options.applySegmentAgeing,options.applyTriggerAgeing,options.applyRpcAgeing)

