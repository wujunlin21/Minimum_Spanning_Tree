#!/bin/bash

graphFiles=`ls ./data/ | grep .gr`

for graph in $graphFiles
do
	filename=`echo $graph | cut -d'.' -f1`
	echo $graph $filename
	
	#execute the python code with:
	python src/RunExperiments.py ./data/$graph ./data/$filename.extra ./results/$filename'_output'.txt

done
