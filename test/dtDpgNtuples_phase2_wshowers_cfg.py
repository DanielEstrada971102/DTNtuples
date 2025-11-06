import FWCore.ParameterSet.Config as cms
import FWCore.ParameterSet.VarParsing as VarParsing
from Configuration.StandardSequences.Eras import eras

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

options.register('dumpDigis', # this option should be used only when run in local.
                 False, 
                 VarParsing.VarParsing.multiplicity.singleton,
                 VarParsing.VarParsing.varType.bool,
                 "If True dumps the digis used in the shower algorithm to a root file")

options.register('useRPC',
                True, 
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.bool,
                "If True uses RPC in the Phase-2 DT trigger emulator")
options.register('useExtDF',
                0, # 0 no, 1 yes, 2 both data formats are saved 
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.int,
                "If 0 no, 1 yes, 2 both data formats are saved ")
options.register('unhardcodeAMSector',
                True, 
                VarParsing.VarParsing.multiplicity.singleton,
                VarParsing.VarParsing.varType.bool,
                "If True the AM TP sector is not hardcoded from 13-14 to 4-10")

options.parseArguments()

process = cms.Process("DTNTUPLES",eras.Phase2C9)

process.load('Configuration.StandardSequences.Services_cff')

if options.debug:
    process.load('FWCore.MessageService.MessageLogger_cfi')
    # process.MessageLogger.cerr.FwkReport.reportEvery = 100

    process.MessageLogger = cms.Service(
        "MessageLogger",
        destinations = cms.untracked.vstring(
            'detailedInfo',
        ),
        detailedInfo = cms.untracked.PSet(
            threshold = cms.untracked.string('DEBUG')
        ),
        debugModules = cms.untracked.vstring(
            'dtTriggerPhase2ShowerV1',
            # 'dtTriggerPhase2AmPrimitiveDigis',
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
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/120000/119a30c4-1ca8-465d-840d-a64cb62f9868.root', #--> aparentemente esta mal este archivo
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/120000/05c718cf-1618-4f60-8b6b-d49a0da7df1f.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/120000/06a231d0-f02c-489b-bb97-0ce8b5469848.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/120000/09452338-f2ba-4a86-a65a-da4179251cae.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/120000/09cfe03d-e128-4e58-89d4-1fcca2b95ccb.root',
    ],
    'DYToLL_M50_PU200': [ # ~4000 events
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/2810000/0027a144-58e8-4e80-a3a2-7ea8f5de45dd.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/2810000/007b0840-d3d2-48a0-9729-bf7f41e9f1d1.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/2810000/008935df-4f1e-43bc-a7e4-b0eac669ef26.root',
        'root://xrootd-cms.infn.it//store/mc/Phase2Spring24DIGIRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/2810000/00a195aa-30f2-405c-aac8-09cb336eadaf.root',
    ]
}

def set_test_files():
    if options.testDataset not in testing_input_files :
        raise ValueError(f"Test dataset {options.testDataset} not recognized. Available test datasets: {list(testing_input_files.keys())}")
    process.source.fileNames = testing_input_files[options.testDataset]#["file:/eos/user/d/destrada/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/ntuple_test_j10.root"]

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

process.dtTriggerPhase2ShowerV1p2 = process.dtTriggerPhase2Shower.clone()
process.dtTriggerPhase2ShowerV1p2.showerTaggingAlgo = options.showerAlgorithm
process.dtTriggerPhase2ShowerV1p2.threshold_for_shower = options.showThreshold
process.dtTriggerPhase2ShowerV1p2.debug = options.debug # debug mode
process.dtTriggerPhase2ShowerV1p2.dump_digis = options.dumpDigis # digi dumping

process.dtTriggerPhase2AmPrimitiveDigis = process.dtTriggerPhase2PrimitiveDigis.clone()
process.dtTriggerPhase2AmPrimitiveDigis.useRPC = options.useRPC
process.dtTriggerPhase2AmPrimitiveDigis.debug = options.debug # debug mode
process.dtTriggerPhase2AmPrimitiveDigis.df_extended = options.useExtDF # Use extended data format
process.dtTriggerPhase2AmPrimitiveDigis.unhardcoded_sectorgt12 = options.unhardcodeAMSector # Do not hardcode AM sector to 4-10
#process.dtTriggerPhase2AmPrimitiveDigis.showersTag = "dtTriggerPhase2ShowerV1"
#process.dtTriggerPhase2AmPrimitiveDigis.useShowers = False

process.load('RecoLocalMuon.Configuration.RecoLocalMuon_cff')
process.dt1DRecHits.dtDigiLabel = "simMuonDTDigis"
process.rpcRecHits.rpcDigiLabel = "simMuonRPCDigis"

from Configuration.StandardSequences.SimL1Emulator_cff import simBmtfDigis
process.simBmtfDigis = simBmtfDigis
process.simBmtfDigis.DTDigi_Source = "simDtTriggerPrimitiveDigis"
process.simBmtfDigis.DTDigi_Theta_Source = "simDtTriggerPrimitiveDigis"

process.load('DTDPGAnalysis.DTNtuples.dtNtupleProducer_phase2_cfi')
process.dtNtupleProducer.ph2TPGUseExtended = options.useExtDF

process.p = cms.Path(process.rpcRecHits
                     + process.dt1DRecHits
                     + process.dt4DSegments
                     + process.CalibratedDigis
                     + process.simBmtfDigis
                     + process.dtTriggerPhase2ShowerV1p2
                     + process.dtTriggerPhase2AmPrimitiveDigis
                     + process.dtNtupleProducer)

from DTDPGAnalysis.DTNtuples.customiseDtNtuples_cff import customiseForRandomBkg, customiseForRunningOnMC, customiseForFakePhase2Info, customiseForAgeing

customiseForRunningOnMC(process,"p")
customiseForFakePhase2Info(process)

if options.applyRandomBkg : 
    customiseForRandomBkg(process,"p")

customiseForAgeing(process,"p",options.applySegmentAgeing,options.applyTriggerAgeing,options.applyRpcAgeing)

