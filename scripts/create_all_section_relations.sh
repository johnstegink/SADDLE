#!/bin/zsh -m

COPRUSDIR=/Volumes/Extern/Studie/studie/corpora
VECTORDIR=/Volumes/Extern/Studie/studie/vectors
RELATIONSDIR=/Volumes/Extern/Studie/studie/relations
CURRENT=`pwd`
VENVDIR=/Users/jstegink/Dropbox/John/Studie/OU/Afstuderen/Thesis/Code/LHA/py/bin
VECTORDIR=/Volumes/Extern/Studie/studie/vectors
OUTDIR=/Volumes/Extern/Studie/studie/sections

SIM=80
NEARESTNEIGHBORS=7

source $VENVDIR/activate
cd $CURRENT


# Wikimatch
#PREFIX=gwikimatch_nl
#$VENVDIR/python LHA_Phase2.py -c $COPRUSDIR/wikimatch/nl -i $VECTORDIR/$PREFIX\.xml -r $RELATIONSDIR/$PREFIX\.xml -s $SIM -o $OUTDIR/$PREFIX\.xml -m $MAXDOC
PREFIX=gwikimatch_en
$VENVDIR/python LHA_Phase2.py -c $COPRUSDIR/$PREFIX -i $VECTORDIR/$PREFIX\.xml -r $RELATIONSDIR/$PREFIX\.xml -s $SIM -o $OUTDIR/$PREFIX\.xml -k $NEARESTNEIGHBORS -d /Volumes/Extern/Studie/studie/html

# WikiSim
PREFIX=WikiSim_nl
#$VENVDIR/python LHA_Phase2.py -c $COPRUSDIR/WikiSim/nl -i $VECTORDIR/$PREFIX\.xml -r $RELATIONSDIR/$PREFIX\.xml -s $SIM -o $OUTDIR/$PREFIX\.xml -m $MAXDOC
PREFIX=WikiSim_en
#$VENVDIR/python LHA_Phase2.py -c $COPRUSDIR/WikiSim/en -i $VECTORDIR/$PREFIX\.xml -r $RELATIONSDIR/$PREFIX\.xml -s $SIM -o $OUTDIR/$PREFIX\.xml -m $MAXDOC

# WiRe
PREFIX=WiRe_nl
#$VENVDIR/python LHA_Phase2.py -c $COPRUSDIR/WiRe/nl -i $VECTORDIR/$PREFIX\.xml -r $RELATIONSDIR/$PREFIX\.xml -s $SIM -o $OUTDIR/$PREFIX\.xml -m $MAXDOC
PREFIX=WiRe_en
#$VENVDIR/python LHA_Phase2.py -c $COPRUSDIR/WiRe/en -i $VECTORDIR/$PREFIX\.xml -r $RELATIONSDIR/$PREFIX\.xml -s $SIM -o $OUTDIR/$PREFIX\.xml -m $MAXDOC

# S2ORC
#PREFIX=S2ORC
#$VENVDIR/python LHA_Phase2.py -c $COPRUSDIR/S2ORC/en -i $VECTORDIR/$PREFIX\.xml -s $SIM -o $OUTDIR/$PREFIX\.xml -m $MAXDOC & # -r $OUTDIR/$PREFIX\.html &

wait


