#!/bin/bash

# This script downloads from EOS_PATH_BASE$eos_dir$RECO_PREF$i$RECO_SUFF RECO file
# Next it cmsRun code to get RPRecognizedPatternsCollection 
#    and translate tree-like data to array of records stored in binary file, namely $BIN_FILL_NUMBER"_"$BIN_RUN_NUMBER"_"$BIN_RECO_NUMBER$BIN_SUFF, e.g. 4499_9920_7.bin
# Next the binary file with an array of records is copied to CERNBOX to directory: $CERNBOX_PATH_BASE$eos_dir


EOS_PATH_BASE="/eos/totem/data/offline/2015/90m/Reco/version2_resynch"
EOS_ENV="root://eostotem.cern.ch/"
RECO_PREF="reco_"
RECO_SUFF=".root"

CERNBOX_PATH_BASE="/eos/user/p/plawski/DATA-BIN"  # <--- [IMPORTANT] 

BIN_SUFF=".bin"

eos_fill_directories=( 		# <--- [IMPORTANT] 
        "/4499/9920/" 
        "/4505/9940/"
        "/4505/9950/"
        "/4509/9976/"
        "/4510/9985/"
        "/4511/9998/"
)


to_resume_bins=(
	7
)

for eos_dir in "${eos_fill_directories[@]}"
do
	for i in "${to_resume_bins[@]}"    # <--- [IMPORTANT]
	do
        echo "Run for " $eos_dir " reco: " $i
		# echo $EOS_ENV$EOS_PATH_BASE$eos_dir$RECO_PREF$i$RECO_SUFF
		xrdcp $EOS_ENV$EOS_PATH_BASE$eos_dir$RECO_PREF$i$RECO_SUFF .

		# SET ENV VARIABLES
		IFS='/ ' read -r -a fill_run <<< "$eos_dir"
		# fill_run=$(echo $eos_dir | tr "//" "\n")
		export BIN_RECO_NUMBER=$i
		export BIN_FILL_NUMBER=${fill_run[1]}
		export BIN_RUN_NUMBER=${fill_run[2]}

		echo "fill: " $BIN_FILL_NUMBER " run: " $BIN_RUN_NUMBER " reco: " $BIN_RECO_NUMBER 

		# RUN MY PROGRAM
		cmsRun DemoAnalyzer/python/BinaryCombinedConfFile_cfg.py     # <--- [IMPORTANT]

		# COPY OUTPUT FILES TO CERNBOX
		cp $BIN_FILL_NUMBER"_"$BIN_RUN_NUMBER"_"$BIN_RECO_NUMBER$BIN_SUFF $CERNBOX_PATH_BASE$eos_dir

		# REMOVE UNNECESSARY FILES
		rm $BIN_FILL_NUMBER"_"$BIN_RUN_NUMBER"_"$BIN_RECO_NUMBER$BIN_SUFF
		rm $RECO_PREF$i$RECO_SUFF
		echo " "
		echo " "
	done
done
