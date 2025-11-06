''' Crab configuration file for Phase2 concentrator studies '''

# For CMSSW_14_1_0_pre23 a special configuration must be done:
# source /cvmfs/cms.cern.ch/common/crab-setup.sh dev
# python3 multicrab.py

#Part of the name of your output directory, adapt as needed.  
name = 'ZprimeToMuMu_M-6000_PU200'
threshold_scan = False
threshold_values = [6, 8, 10, 12, 14, 16, 20, 24]
shower_algorithm = 1  # 0=standalone, 1=firmware like
use_rpc = True
use_ext_df = 0  # 0 no, 1 yes, 2 both
running_options = []
runATCAF = False

# Dictionary to store metadata
dataset = {
   # Zprime -> mumu prompt muons
   # INVALID: "ZprimeToMuMu_M-6000_PU200" : "/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/Phase2HLTTDRWinter20DIGI-PU200_110X_mcRun4_realistic_v3-v2/GEN-SIM-DIGI-RAW",
   "ZprimeToMuMu_M-6000_PU200" : "/ZprimeToMuMu_M-6000_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
   # Drell yan
   # NOT AVAILABLE (problematic)
   # "DYToLL_M50_PU200" : "/DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2Fall22DRMiniAOD-PU200_125X_mcRun4_realistic_v2-v1/GEN-SIM-DIGI-RAW-MINIAOD",
   "DYToLL_M50_PU200" : "//DYToLL_M-50_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200_Trk1GeV_140X_mcRun4_realistic_v4-v1/GEN-SIM-DIGI-RAW-MINIAOD",
   # MinBias
   "MinBias_PU200" : "/MinBias_TuneCP5_14TeV-pythia8/Phase2Spring24DIGIRECOMiniAOD-PU200ALCA_140X_mcRun4_realistic_v4-v2/GEN-SIM-DIGI-RAW-MINIAOD"
}

# Samples to run (these are keys in the above dictionary)
listOfSamples = [
   "ZprimeToMuMu_M-6000_PU200"
   # "DYToLL_M50_PU200",
   # "MinBias_PU200"
]

if __name__ == '__main__':
   # import crab stuff
   from CRABClient.UserUtilities import config
   config = config()

   from CRABAPI.RawCommand import crabCommand
   from multiprocessing import Process

   
   def submit(config):
       ''' Function to handle job submission '''
       res = crabCommand('submit', config = config )

   config.General.workArea = 'analysis_'+name
   config.General.transferLogs = True
   config.General.transferOutputs = True

   config.JobType.pluginName = 'Analysis'
   config.JobType.psetName = 'dtDpgNtuples_phase2_wshowers_cfg.py'

   # config.JobType.pyCfgParams = running_options
   config.JobType.allowUndistributedCMSSW = True

   config.Data.inputDBS = 'global' 
   config.Data.splitting = 'FileBased'
   config.Data.publication = False
   config.Data.unitsPerJob = 1
   config.Site.storageSite = 'T3_CH_CERNBOX'
   config.Site.blacklist = ['T2_US_Wisconsin', 'T2_RU_JINR', 'T2_EE_Estonia']
   if runATCAF :
      config.Site.whitelist = ['T3_CH_CERN_CAF', 'T1_RU_JINR', 'T1_IT_CNAF']
      config.Site.ignoreGlobalBlacklist = True
      config.Data.ignoreLocality = True

   range_of_thresholds = threshold_values if threshold_scan else [threshold_values[0]]
   for threshold in range_of_thresholds:
      for sample in listOfSamples:
         config.General.workArea = f"analysis{name}{sample}_shwalgo{shower_algorithm}_thr{threshold}"
         config.JobType.pyCfgParams = [
            f'ntupleName=./DTDPGNtuple_15_1_0_pre2_Phase2_WShower_ShowAlgo{shower_algorithm}_Thr{threshold}_Simulation.root',
            f'showThreshold={threshold}',
            f'showerAlgorithm={shower_algorithm}',
            f'useRPC={use_rpc}',
            f'useExtDF={use_ext_df}',
         ]
         config.General.requestName = sample
         config.Data.inputDataset = dataset[sample]
         config.Data.outputDatasetTag = sample
         p = Process(target=submit, args=(config,))
         p.start()
         p.join()
