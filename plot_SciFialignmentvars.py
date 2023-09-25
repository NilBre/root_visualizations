import ROOT
from ROOT import * #TFile, TTree, gROOT, AddressOf, RDataFrame, TH1D, TStyle
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
#matplotlib.rcParams['text.usetex'] = True
#matplotlib.rcParams['text.latex.preamble'] = r"\usepackage{amsmath} \usepackage{amssymb}"
#hep.style.use(hep.style.LHCb2)
#import matplotlib.patches as mpl_patches
#import pandas as pd
#from datetime import timedelta

#Script for making comparison plots for SciFi alignment
# ROOT.gROOT.SetBatch(True)
# ROOT.gROOT.ProcessLine(".x /afs/cern.ch/user/b/bimitres/public/lhcbStyle.C")
# ROOT.gROOT.ForceStyle()

# prefix = '/eos/user/b/bimitres/V0_crosssections/SciFi_alignment_run256166/'
prefix = "roots/"
no_tuning = '500k_i10_base_loose/GoodLongTracks_base_500k_i10.root' # base, probably 200k but not sure (also not sure if loose or strict)
#no_tuning = 'GoodLongTracks_best_strict.root' # strict selection
with_tuning = 'GoodLongTracks_histo_i8_500k_loose.root' # 500k best, converged

# new files to compare for joint constraints
small_Tx = "root_500k/GoodLongTracks_tuned_0_0001_Tx.root"
oldTx_other_tuned = "root_500k/GoodLongTracks_oldTx_rest_tuned.root"
Tx_0_8 = "root_500k/GoodLongTracks_0_8_onlyTx.root"
Tx_0_6 = "root_500k/GoodLongTracks_0_6_onlyTx.root"

## switch input order just to see if the plotscale changes
#no_tuning = '500k_i10_base_loose/GoodLongTracks_base_500k_i10.root' # base, probably 2$
#no_tuning = 'GoodLongTracks_best_strict.root' # strict selection
#with_tuning = 'GoodLongTracks_histo_i8_500k_loose.root'
#prefix = "roots/root_200k/"
#no_tuning = 'GoodLongTracks_histo_base_200k.root'
#with_tuning = 'GoodLongTracks_histo_best_200k.root'

print('1')
names = ["yT1", "yT2", "yT3", "xT1", "xT2", "xT3", "xT1","yT1","txT1", "txT2", "txT3", "tyT1", "tyT2", "tyT3", "unbiasedFTResidual", "RMSResidualModules", "RMSResidualQuarters"]

axes_titles = ["y T1 Station [mm]", "y T2 Station [mm]", "y T3 Station [mm]", 
               "x T1 Station [mm]", "x T2 Station [mm]", "x T3 Station [mm]", 
               "x T1 Station [mm]", "y T1 Station [mm]", 
               "tx T1 Station", "tx T2 Station", "tx T3 Station", 
               "ty T1 Station", "ty T2 Station", "ty T3 Station", 
               "FT X Resiudual [mm]" , "RMS ResidualModules [mm]", "RMSResidualQuarters [mm]"]
print('2')
histos1 = []
histos2 = []
histos3 = []
histos4 = []
histos5 = []
histos6 = []
for i in range(0,len(names)):
    histos1.append(TH1D())
    histos2.append(TH1D())
    histos3.append(TH1D())
    histos4.append(TH1D())
    histos5.append(TH1D())
    histos6.append(TH1D())

file1 = TFile.Open(prefix + no_tuning)
file2 = TFile.Open(prefix + with_tuning)
file3 = TFile.Open(prefix + small_Tx)
file4 = TFile.Open(prefix + oldTx_other_tuned)
file5 = TFile.Open(prefix + Tx_0_8)
file6 = TFile.Open(prefix + Tx_0_6)

# order changed
files =[file2, file1, file3, file4, file5, file6]
print('3')

for f in range(0,len(files)):
    for n in range(0,len(names)):
        dir2 = files[f].GetDirectory("FTTrackMonitor_GoodLongTracks")
#        do it like this if i use strict, since it has a different monitorname
#        if f == 0:
#            dir2 = files[f].GetDirectory("FTTrackMonitor_AlignGoodLongTracks")
#        if f == 1:
#            dir2 = files[f].GetDirectory("FTTrackMonitor_GoodLongTracks")
        gethistos = [dir2.Get("yT1"),
                     dir2.Get("yT2"),
                     dir2.Get("yT3"),
                     dir2.Get("xT1"),
                     dir2.Get("xT2"),
                     dir2.Get("xT3"),
                     dir2.Get("xT1"),
                     dir2.Get("yT1"),
                     dir2.Get("txT1"),
                     dir2.Get("txT2"),
                     dir2.Get("txT3"),
                     dir2.Get("tyT1"),
                     dir2.Get("tyT2"),
                     dir2.Get("tyT3"),
                     dir2.Get("unbiasedFTResidual"),
                     dir2.Get("RMSResidualModules"),
                     dir2.Get("RMSResidualQuarters")
        ]

        if f == 0:
            histos1 = gethistos
        if f == 1:
            histos2 = gethistos
        if f == 2:
            histos3 = gethistos
        if f == 3:
            histos4 = gethistos
        if f == 4:
            histos5 = gethistos
        if f == 5:
            histos6 = gethistos
print('4')

c = ROOT.TCanvas()
ROOT.gStyle.SetOptStat(0)

for i in range(0,len(histos1)):
    histos1[i].SetMarkerStyle(20);
    histos1[i].SetMarkerSize(0.8);
    histos1[i].SetMarkerColor(2);
    histos1[i].GetXaxis().SetTitle(axes_titles[i])
    histos1[i].GetYaxis().SetTitle("Events")
    #histos1[i].GetXaxis().SetRangeUser(1850.0, 1900.0)
#    histos1[i].Scale(1/(histos1[i].Integral())) # also comment that out when binning is wrong
    histos1[i].Draw("EP")
    histos2[i].SetMarkerColor(4)
    histos2[i].SetMarkerStyle(22)
    histos2[i].SetMarkerSize(0.8)
#    histos2[i].Scale(1/(histos2[i].Integral())) # comment that out if binning is wrong
    histos2[i].Draw("same")
    histos3[i].SetMarkerColor(6)
    histos3[i].SetMarkerStyle(22)
    histos3[i].SetMarkerSize(0.8)
#    histos3[i].Scale(1/(histos3[i].Integral())) # comment that out if binning is wrong
    histos3[i].Draw("same")
    histos4[i].SetMarkerColor(8)
    histos4[i].SetMarkerStyle(22)
    histos4[i].SetMarkerSize(0.8)
#    histos4[i].Scale(1/(histos4[i].Integral())) # comment that out if binning is wrong
    histos4[i].Draw("same")
    histos5[i].SetMarkerColor(5)
    histos5[i].SetMarkerStyle(22)
    histos5[i].SetMarkerSize(0.8)
#    histos5[i].Scale(1/(histos5[i].Integral())) # comment that out if binning is wrong
    histos5[i].Draw("same")
    histos6[i].SetMarkerColor(12)
    histos6[i].SetMarkerStyle(22)
    histos6[i].SetMarkerSize(0.8)
#    histos6[i].Scale(1/(histos6[i].Integral())) # comment that out if binning is wrong
    histos6[i].Draw("same")
    leg = ROOT.TLegend(0.7,0.7,0.8,0.85)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(132)
    leg.SetTextSize(0.055)
    leg.AddEntry(histos1[i], "with tuning", "P")
    leg.AddEntry(histos2[i], "no tuning", "P")
    leg.AddEntry(histos3[i], "very small Tx, tuned", "P")
    leg.AddEntry(histos4[i], "old Tx, rest tuned", "P")
    leg.AddEntry(histos5[i], "0.8 Tx, rest tuned", "P")
    leg.AddEntry(histos6[i], "0.6 Tx, rest tuned", "P")
    leg.Draw()
    #c1.SetLogx()
    #c.BuildLegend(0.5,0.3,0.8,0.5,"","P") #0.5,0.3,0.8,0.5
    T1 = TLatex()
    T1.SetTextSize(0.05)
    T1.DrawLatexNDC(.25,.80, "LHCb Internal")
    T1.DrawLatexNDC(.25,.75, "Run 269045")

    c.SaveAs("home/nbreer/fast_plotting_root/outfiles/comp_Tx/" + names[i] + "comp_vars.pdf")
