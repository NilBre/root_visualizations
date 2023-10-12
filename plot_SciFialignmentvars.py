print('import ROOT')
import ROOT
print('from ROOT import TFile and TH1D')
from ROOT import TFile, TH1D
print('import TTree, gROOT, TStyle')
from ROOT import TTree, gROOT, TStyle, TLatex, TLine
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

markers = ['o', 'x', 'D', 'd', '.', 'v', 's', 'p', '1']

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
print('start reading data')

prefix = 'root_500k/'

no_tuning = 'GoodLongTracks_base_500k_i10.root' # base, probably 200k but not sure (also not sure if loose or strict)
# with_tuning = 'GoodLongTracks_histo_i8_500k_loose.root' # 500k best, converged
# small_Tx = "GoodLongTracks_tuned_0_0001_Tx.root"
# oldTx_other_tuned = "GoodLongTracks_oldTx_rest_tuned.root"
# Tx_0_8 = "GoodLongTracks_0_8_onlyTx.root"
# Tx_0_6 = "GoodLongTracks_0_6_onlyTx.root"

# Tx_2mm = 'GoodLongTracks_2mm_Tx.root' # 2 micron in Tx, rest are my tuned params
Tx_micron_10 = 'GoodLongTracks_Tx_10micron_Rz_better.root' # TxRz alignment, 10micron Tx
Tx_10mu_TxTzRxRz = 'GoodLongtracks_TxTzRxRz_iter4_10micron_tuned.root' # TxTzRxRz, 10 micron Tx, only needing 4 iter instead of 9
# Tx_100mu_TxTzRxRz = 'GoodLongTracks_100mu_TxTzRxRz_iter15.root' # 100 micron Tx joint unc., TxTzRxRz alignment
# Tx_100mu_TxRz = 'GoodLongTracks_100mu_TxRz.root' # 100mu TX unc., TxRz alignment, i belive 11 iters

# Tx_10mu_TxRxRz_SmallSurveyRxUnc = 'GoodLongTracks_TxRxRz_smallRxSurveyUnc.root'
# V2_constraint = 'GoodLongTracks_V2_constraint.root'
# T1V_T2V_fix = 'GoodLongTracks_v2_fix_survey.root'
# globalMod = 'GoodLongTracks_global_TxTzRxRz.root'

# Tx_10mu_TxRz_LargeRxJoint = 'GoodLongTracks_small_joint_Rx_10mu_Tx_TxRz.root' # set Rx joint to 2e-7, iter9 convergence
# Tx_10mu_SmallRxJoint = 'GoodLongTracks_10mu_RxJoints_0.root'

print('finished reading data')

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
# histos4 = []
# histos5 = []
# histos6 = []
# histos7 = []
# histos8 = []
for i in range(0,len(names)):
    histos1.append(TH1D())
    histos2.append(TH1D())
    histos3.append(TH1D())
    # histos4.append(TH1D())
    # histos5.append(TH1D())
    # histos6.append(TH1D())
    # histos7.append(TH1D())
    # histos8.append(TH1D())

file1 = TFile.Open(prefix + no_tuning)
# file2 = TFile.Open(prefix + with_tuning)
# file1 = TFile.Open(prefix + Tx_2mm)
file2 = TFile.Open(prefix + Tx_micron_10)
file3 = TFile.Open(prefix + Tx_10mu_TxTzRxRz)
# file4 = TFile.Open(prefix + Tx_100mu_TxTzRxRz)
# file5 = TFile.Open(prefix + Tx_100mu_TxRz)

# file4 = TFile.Open(prefix + V2_constraint)
# file5 = TFile.Open(prefix + Tx_10mu_TxRxRz_SmallSurveyRxUnc)
# file6 = TFile.Open(prefix + T1V_T2V_fix)
# file7 = TFile.Open(prefix + globalMod)

# file6 = TFile.Open(prefix + Tx_10mu_TxRz_LargeRxJoint)
# file8 = TFile.Open(prefix + Tx_10mu_SmallRxJoint)
# file6 = TFile.Open(prefix + Tx_0_8)
# file7 = TFile.Open(prefix + Tx_0_6)
# file8 = TFile.Open(prefix + small_Tx)
# order changed
files =[file2, file3, file1]#, file4, file5, file6, file1]
# files =[file2, file1, file3, file4, file5, file6, file7, file8]
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
        # if f == 3:
        #     histos4 = gethistos
        # if f == 4:
        #     histos5 = gethistos
        # if f == 5:
        #     histos6 = gethistos
        # if f == 6:
        #     histos7 = gethistos
        # if f == 7:
        #     histos8 = gethistos
print('4')

c = ROOT.TCanvas()
ROOT.gStyle.SetOptStat(0)

line = TLine()
for i in range(0,len(histos1)):
    # c3 = ROOT.TCanvas("","",1200,900)
    # stack=ROOT.THStack("hs",f"{names}")
    histos1[i].SetMarkerStyle(20)
    histos1[i].SetMarkerSize(0.8)
    histos1[i].SetMarkerColor(6)
    histos1[i].SetLineColor(2)
    histos1[i].GetYaxis().SetTitle(axes_titles[i])
    histos1[i].GetXaxis().SetTitle("Module numbers")
    histos1[i].GetYaxis().SetRangeUser(-0.03, 0.03)
#    histos1[i].Scale(1/(histos1[i].Integral())) # also comment that out when binning is wrong
    histos1[i].Draw("EP")

    histos2[i].SetMarkerColor(4)
    histos2[i].SetLineColor(4)
    # histos2[i].GetYaxis().SetTitle(axes_titles[i])
    # histos2[i].GetXaxis().SetTitle("Events")
    histos2[i].SetMarkerStyle(22)
    histos2[i].SetMarkerSize(0.8)
#    histos2[i].Scale(1/(histos2[i].Integral())) # comment that out if binning is wrong
    histos2[i].Draw("EP same")

    histos3[i].SetMarkerColor(2)
    histos3[i].SetLineColor(2)
    histos3[i].SetMarkerStyle(2)
    histos3[i].SetMarkerSize(0.8)
#    histos3[i].Scale(1/(histos3[i].Integral())) # comment that out if binning is wrong
    histos3[i].Draw("EP same")

    # histos4[i].SetMarkerColor(8)
    # histos1[i].SetLineColor(8)
    # histos4[i].SetMarkerStyle(21)
    # histos4[i].SetMarkerSize(0.8)
    # # histos4[i].Scale(1/(histos4[i].Integral())) # comment that out if binning is wrong
    # histos4[i].Draw("EP same")

    # histos5[i].SetMarkerColor(5)
    # histos1[i].SetLineColor(5)
    # histos5[i].SetMarkerStyle(23)
    # histos5[i].SetMarkerSize(0.8)
    # # histos5[i].Scale(1/(histos5[i].Integral())) # comment that out if binning is wrong
    # histos5[i].Draw("EP same")

    # histos6[i].SetMarkerColor(12)
    # histos6[i].SetMarkerStyle(5)
    # histos1[i].SetLineColor(12)
    # histos6[i].SetMarkerSize(0.8)
    # # histos6[i].Scale(1/(histos6[i].Integral())) # comment that out if binning is wrong
    # histos6[i].Draw("EP same")

    # histos7[i].SetMarkerColor(2)
    # histos1[i].SetLineColor(1)
    # histos7[i].SetMarkerStyle(20)
    # histos7[i].SetMarkerSize(0.8)
    # # histos7[i].Scale(1/(histos7[i].Integral())) # comment that out if binning is wrong
    # histos7[i].Draw("EP same")

    # histos8[i].SetMarkerColor(1)
    # histos8[i].SetMarkerStyle(22)
    # histos8[i].SetMarkerSize(0.8)
    # # histos8[i].Scale(1/(histos8[i].Integral())) # comment that out if binning is wrong
    # histos8[i].Draw("EP same")

    if names[i] == 'RMSResidualQuarters':
        for j in range(48):
            if j % 4 == 0 and j != 0:
                histos3[i].Draw('same')
                line.DrawLine(j-0.5,-0.00125, j-0.5, 0.00125)
    leg = ROOT.TLegend(0.6,0.7,0.8,0.9)
    leg.SetFillStyle(0)
    leg.SetFillColor(11)
    leg.SetBorderSize(0)
    leg.SetTextFont(132)
    leg.SetTextSize(0.053)
    # leg.AddEntry(histos1[i], "with tuning", "P")
    # leg.AddEntry(histos1[i], "2 micron", "P")
    leg.AddEntry(histos1[i], "10 micron TxRz", "P")
    leg.AddEntry(histos2[i], "10 micron TxTzRxRz", "P")
    leg.AddEntry(histos3[i], "no tuning", "P")
    # leg.AddEntry(histos4[i], "100 micron TxTzRxRz", "P")
    # leg.AddEntry(histos5[i], "100 micron TxRz", "P")
    # leg.AddEntry(histos4[i], "V2 constraint added", "P")
    # leg.AddEntry(histos5[i], "10 micron, TxRxRz, small Rx survey unc", "P")
    # leg.AddEntry(histos6[i], "T1V T2V constraint, 10mu TxTzRxRz", "P")
    # leg.AddEntry(histos7[i], "10 micron, TxTzRxRz + global Modules", "P")
    
    # leg.AddEntry(histos6[i], "10 micron, Rx joint large", "P")
    # leg.AddEntry(histos8[i], "10mu, small Rx joint", "P")
    # leg.AddEntry(histos7[i], "0.6 micron", "P")
    # leg.AddEntry(histos8[i], "0.1 micron", "P")
    leg.Draw()
    #c1.SetLogx()
    #c.BuildLegend(0.5,0.3,0.8,0.5,"","P") #0.5,0.3,0.8,0.5
    T1 = TLatex()
    T1.SetTextSize(0.05)
    T1.DrawLatexNDC(.25,.80, "LHCb Internal")
    T1.DrawLatexNDC(.25,.75, "Run 269045")

    if names[i] == 'RMSResidualQuarters' or names[i] == 'RMSResidualModules':
        print(f'######## mean values of the histograms: variable = {names[i]}')
        # print('mean Tx_2mm: axis 2', histos1[i].GetMean(axis=2))
        print('mean Tx_micron_10: axis 2', histos2[i].GetMean(axis=2))
        print('mean Tx_10mu_TxTzRxRz: axis 2', histos3[i].GetMean(axis=2))
        # print('mean Tx_100mu_TxTzRxRz: axis 2', histos4[i].GetMean(axis=2))
        # print('mean Tx_100mu_TxRz: axis 2', histos5[i].GetMean(axis=2))
        # print('mean V2_constraint: axis 2', histos6[i].GetMean(axis=2))
        # print('mean Tx_10mu_TxRxRz_SmallSurveyRxUnc: axis 2', histos7[i].GetMean(axis=2))
    c.SaveAs("outfiles/compi/wp2_comparison/" + names[i] + "comp_WP2_comparison.pdf")
