print('import ROOT')
import ROOT
print('from ROOT import TFile and TH1D')
from ROOT import TFile, TH1D
print('import TTree, gROOT, TStyle')
from ROOT import TTree, gROOT, TStyle, TLatex, TChain
import math as m
from math import *
import sys, os
import numpy as np
import random
#import yaml
import io
import matplotlib
import matplotlib.pyplot as plt
#import glob
#xfrom grepfunc import grep_iter
#import mplhep as hep
#from termcolor import colored
import argparse
import json

import functools
import warnings
from subprocess import check_output

import pandas
# from root_pandas import read_root
from scipy import stats as st

filenames = ['/Users/nibreer/Zehua_ganga/davinci/tuple_10mu_TxRz.root', '/Users/nibreer/Zehua_ganga/davinci/tuple_10mu_TxTzRxRz.root']

data = read_root(filenames[0])
for col in data.columns:
    print(col)
# chain = ROOT.TChain("Tuple/DecayTree")
# chain.Add(filenames[0])

# massCut = "D0_M>1800 & D0_M<1925"
# totCut=""
# tree = chain.CopyTree(totCut+massCut)
# print(" tree entries : ", tree)