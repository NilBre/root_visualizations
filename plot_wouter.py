print('import ROOT')
import ROOT
print('from ROOT import TFile and TH1D')
from ROOT import TFile, TH1D
print('import TTree, gROOT, TStyle')
from ROOT import TTree, gROOT, TStyle, TLatex
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

prefix = 'root_500k/'
no_tuning = 'GoodLongTracks_base_500k_i10.root' # base, probably 200k but not sure (also not sure if loose or strict)
with_tuning = 'GoodLongTracks_histo_i8_500k_loose.root' # 500k best, converged

# Tx_2mm = 'GoodLongTracks_2mm_Tx.root'
# Tx_micron_10 = 'GoodLongTracks_Tx_10micron_Rz_better.root' # this uses TxRz
# Tx_10mu_TxTzRxRz = 'GoodLongtracks_TxTzRxRz_iter4_10micron_tuned.root'
# Tx_100mu_TxTzRxRz = 'GoodLongTracks_100mu_TxTzRxRz_iter15.root'
# Tx_100mu_TxRz = 'GoodLongTracks_100mu_TxRz.root' # 100mu TX unc., TxRz alignment, i belive 11 iters
# Tx_10mu_TxRz_LargeRxJoint = 'GoodLongTracks_small_joint_Rx_10mu_Tx_TxRz.root' # set Rx joint to 2e-7, iter9 convergence
# Tx_10mu_TxRxRz_SmallSurveyRxUnc = 'GoodLongTracks_TxRxRz_smallRxSurveyUnc.root'
# Tx_10mu_SmallRxJoint = 'GoodLongTracks_10mu_RxJoints_0.root'
# V2_constraint = 'GoodLongTracks_V2_constraint.root'
filenames = [
            'no_tuning',
            'with_tuning',
            ]

names = ["FTResidual", "chi2_per_ndof", "chi2ProbVsMom"]
axes_titles = ["FT X Residual [mm]", "chi2 / ndof", "pT [MeV]"]

histos1 = []
histos2 = []

for i in range(0,len(names)):
    histos1.append(TH1D())
    histos2.append(TH1D())

filein = []
for fileintag in [
                  prefix + no_tuning,
                  prefix + with_tuning,
                 ]:

    filein.append(ROOT.TFile(fileintag))

monitorname = "TrackMonitor_GoodLongTracks"

ROOT.gStyle.SetOptStat(1)

source = [getattr(file, monitorname) for file in filein]
source = [getattr(label, "Long") for label in source]

for var in names:
    c3 = ROOT.TCanvas("","",1200,900)
    stack=ROOT.THStack("hs",f"{names}")

    hist=source[0].FindObjectAny(var)
    hist.SetLineColor(ROOT.kBlack)
    hist.SetLineWidth(2)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(0.8)
    hist.SetMarkerColor(ROOT.kBlack)
    # hist.Scale(1/(hist.Integral()))


    hist1=source[0].FindObjectAny(var)
    hist1.GetXaxis().SetTitle(var)
    hist1.GetYaxis().SetTitle("Events")
    hist1.SetLineColor(ROOT.kRed)
    hist1.SetLineWidth(2)
    hist1.SetMarkerStyle(20)
    hist1.SetMarkerSize(0.8)
    hist1.SetMarkerColor(ROOT.kRed)
    # hist1.Scale(1/(hist1.Integral()))

    if var == 'chi2ProbVsMom':
        bins_f0, bins_f1, bins_f2 = [], [], []
        for bin in range(50):
            bins_f0.append(hist.GetBinContent(bin))
            bins_f1.append(hist1.GetBinContent(bin))

        print('maximum bin content of each file')
        print(f'max: {filenames[0]}', max(bins_f0))
        print(f'max: {filenames[1]}', max(bins_f1))

    stack.Add(hist)
    stack.Add(hist1)

    stack.Draw("nostack")
    if var == "FTResidual":
        hist1.GetXaxis().SetLimits(-0.5, 0.5)
    if var == "chi2_per_ndof":
        hist1.GetXaxis().SetLimits(0, 3.5)
    leg = ROOT.TLegend(0.7,0.4,0.8,0.65)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(132)
    leg.SetTextSize(0.055)
    # leg.AddEntry(hist, "no tuning", "P")
    # leg.AddEntry(hist1, "with tuning", "P")
    # leg.AddEntry(hist, "2 micron", "P")
    leg.AddEntry(hist1, "10 micron TxRz", "P")
    leg.AddEntry(hist2, "10 micron TxTzRxRz", "P")
    # leg.AddEntry(hist3, "100 micron TxTzRxRz", "P")
    # leg.AddEntry(hist4, "100 micron TxRz", "P")
    # leg.AddEntry(hist5, "10 micron TxRz, large Rx joint", "P")
    leg.AddEntry(hist6, "10 micron TxRxRz, small Rx survey unc", "P")
    leg.AddEntry(hist7, "V2 constraint added", "P")
    # leg.AddEntry(hist7, "10 mu Tx, small Rx joint", "P")
    # leg.AddEntry(hist7, "0.1 micron", "P")
    leg.Draw()
    c3.Draw()
    c3.SaveAs(f"outfiles/compi/wp2_comparison/" + var + "_wp2_comparison.pdf")
