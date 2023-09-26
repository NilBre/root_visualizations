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
#no_tuning = 'GoodLongTracks_best_strict.root' # strict selection
with_tuning = 'GoodLongTracks_histo_i8_500k_loose.root' # 500k best, converged

# new files to compare for joint constraints
# small_Tx = "GoodLongTracks_tuned_0_0001_Tx.root"
# oldTx_other_tuned = "GoodLongTracks_oldTx_rest_tuned.root"
# Tx_0_8 = "GoodLongTracks_0_8_onlyTx.root"
# Tx_0_6 = "GoodLongTracks_0_6_onlyTx.root"
Tx_2mm = 'GoodLongTracks_2mm_Tx.root'

filenames = ['no_tuning', 'with_tuning', '2mm_Tx']

names = ["FTResidual", "chi2_per_ndof", "chi2ProbVsMom"]
axes_titles = ["FT X Residual [mm]", "chi2 / ndof", "pT [MeV]"]

histos1 = []
histos2 = []
histos3 = []

for i in range(0,len(names)):
    histos1.append(TH1D())
    histos2.append(TH1D())
    histos3.append(TH1D())

print('1')

file1 = TFile.Open(prefix + no_tuning)
file2 = TFile.Open(prefix + with_tuning)
file3 = TFile.Open(prefix + Tx_2mm)

files =[file2, file1, file3]

print('2')

filein = []
for fileintag in [prefix + no_tuning,
                  prefix + with_tuning,
                  prefix + Tx_2mm
                 ]:

    filein.append(ROOT.TFile(fileintag))

monitorname = "TrackMonitor_GoodLongTracks"

ROOT.gStyle.SetOptStat(1)

#source1 = getattr(filein[0], monitorname)
#source2 = getattr(filein[1], monitorname)

#source1 = getattr(source1, "Long")
#source2 = getattr(source2, "Long")

source = [getattr(file, monitorname) for file in filein]
source = [getattr(label, "Long") for label in source]

for var in names:
    c3 = ROOT.TCanvas("","",1200,900)
    stack=ROOT.THStack("hs","compare old new joints uncertainties")
    hist=source[0].FindObjectAny(var)
    hist.SetLineColor(ROOT.kBlack)
    hist.SetLineWidth(2)
    hist.SetMarkerStyle(20)
    hist.SetMarkerSize(0.8)
    hist.SetMarkerColor(ROOT.kBlack)
    # hist.Scale(1/(hist.Integral()))
    hist.GetXaxis().SetTitle(var)
    hist.GetYaxis().SetTitle("Events")

    hist1=source[1].FindObjectAny(var)
    hist1.SetLineColor(ROOT.kRed)
    hist1.SetLineWidth(2)
    hist1.SetMarkerStyle(20)
    hist1.SetMarkerSize(0.8)
    hist1.SetMarkerColor(ROOT.kRed)
    # hist1.Scale(1/(hist1.Integral()))

    hist2=source[2].FindObjectAny(var)
    hist2.SetLineColor(ROOT.kBlue)
    hist2.SetLineWidth(2)
    hist2.SetMarkerStyle(20)
    hist2.SetMarkerSize(0.8)
    hist2.SetMarkerColor(ROOT.kBlue)
    # hist2.Scale(1/(hist2.Integral()))

    if var == 'chi2ProbVsMom':
        bins_f0, bins_f1, bins_f2 = [], [], []
        bins_f3, bins_f4, bins_f5 = [], [], []

        for bin in range(50):
            bins_f0.append(hist.GetBinContent(bin))
            bins_f1.append(hist1.GetBinContent(bin))
            bins_f2.append(hist2.GetBinContent(bin))
        print('maximum bin content of each file')
        print(f'max: {filenames[0]}', max(bins_f0))
        print(f'max: {filenames[1]}', max(bins_f1))
        print(f'max: {filenames[2]}', max(bins_f2))

    stack.Add(hist)
    stack.Add(hist1)
    stack.Add(hist2)

    stack.Draw("nostack")
    if var == "FTResidual":
        hist.GetXaxis().SetLimits(-0.5, 0.5)
    if var == "chi2_per_ndof":
        hist.GetXaxis().SetLimits(0, 3.5)
    leg = ROOT.TLegend(0.7,0.4,0.8,0.65)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(132)
    leg.SetTextSize(0.055)
    leg.AddEntry(hist, "no tuning", "P")
    leg.AddEntry(hist1, "with tuning", "P")
    leg.AddEntry(hist2, "2mm Tx", "P")
    leg.Draw()
    c3.Draw()
    c3.SaveAs(f"outfiles/compi/" + var + "_comp_normalised.pdf")
