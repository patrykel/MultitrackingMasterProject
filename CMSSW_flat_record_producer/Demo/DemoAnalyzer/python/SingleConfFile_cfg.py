import FWCore.ParameterSet.Config as cms
import os

# MY VARIABLES
# print(os.environ['HOME'])
reco_number = os.environ['RECO_NUMBER']
fill_number = os.environ['FILL_NUMBER']
run_number = os.environ['RUN_NUMBER']
csv_filename = fill_number + "_" + run_number + "_" + reco_number + ".csv"

process = cms.Process("Demo")

# Specify the maximum events to simulate
# process.maxEvents = cms.untracked.PSet( input=cms.untracked.int32(1000))

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('Demo')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    limit=cms.untracked.int32(-1)
)
process.options = cms.untracked.PSet(wantSummary=cms.untracked.bool(True))

# process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100))

process.source = cms.Source("PoolSource",
                            # replace 'myfile.root' with the source file you want to use
                            fileNames=cms.untracked.vstring(
                                # 'file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/TTJets_8TeV_53X.root'
                                # 'root://eosuser.cern.ch//eos/user/p/plawski/totem/data/offline/2015/90m/Reco/version2_resynch/4510/9985/reco_0.root',
                                # 'root://eosuser.cern.ch//eos/user/p/plawski/totem/data/offline/2015/90m/Reco/version2_resynch/4510/9985/reco_1.root'
                                # 'file:/afs/cern.ch/user/p/plawski/cmssw_7_0_4_src/reco_45.root'

                                'file:/afs/cern.ch/user/p/plawski/cmssw_7_0_4_src/Demo/reco_' + reco_number + '.root'

                            )
                            )

process.demo = cms.EDAnalyzer('DemoAnalyzer',
                              minTracks=cms.untracked.uint32(0),
                              fill_name=cms.string('2015_10_17_fill4510')
                              )

process.recoHist = cms.EDAnalyzer('RecoHistAnalyzer',
                                  minTracks=cms.untracked.uint32(0)
                                  )

process.TFileService = cms.Service("TFileService",
                                   fileName=cms.string('uvLines.root')
                                   )

process.recoToFlatRoot = cms.EDAnalyzer('RecoToFlatRootAnalyzer')
process.recoLogger = cms.EDAnalyzer('RecoLoggingAnalyzer')

process.recoCSV = cms.EDAnalyzer('RecoToCSVAnalyzer',
                                 fill_name=cms.string('2015_10_17_fill4510')
                                 )

process.recoCSVLineAB = cms.EDAnalyzer('RecoToCSVWithABLinesAnalyzer',
                                  recoId = cms.string(reco_number),
                                  fill_file_name=cms.string(csv_filename))

process.recoMultiCSV = cms.EDAnalyzer('RecoMultiToCSVAnalyzer',
  recoId = cms.string(reco_number),
  fill_name=cms.string(csv_filename)
  )

process.p = cms.Path(
    # process.recoMultiCSV
    process.recoCSVLineAB
    # process.recoLogger
    # process.demo
    # process.recoHist 
    # process.recoToFlatRoot
    # process.recoCSV
)
