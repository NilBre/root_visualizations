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

prefix = "roots/"
no_tuning = '500k_i10_base_loose/GoodLongTracks_base_500k_i10.root'
#no_tuning = 'GoodLongTracks_best_strict.root' # strict selection
with_tuning = 'GoodLongTracks_histo_i8_500k_loose.root' # 500k best, converged

# new files to compare for joint constraints
small_Tx = "root_500k/GoodLongTracks_tuned_0_0001_Tx.root"
oldTx_other_tuned = "root_500k/GoodLongTracks_oldTx_rest_tuned.root"
Tx_0_8 = "root_500k/GoodLongTracks_0_8_onlyTx.root"
Tx_0_6 = "root_500k/GoodLongTracks_0_6_onlyTx.root"

filenames = ['no_tuning', 'with_tuning', 'small_Tx', 'oldTx_other_tuned', 'Tx_0_8', 'Tx_0_6']

names = ["FTResidual", "chi2_per_ndof", "chi2ProbVsMom"]
axes_titles = ["FT X Residual [mm]", "chi2 / ndof", "pT [MeV]"]

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

print('1')

file1 = TFile.Open(prefix + no_tuning)
file2 = TFile.Open(prefix + with_tuning)
file3 = TFile.Open(prefix + small_Tx)
file4 = TFile.Open(prefix + oldTx_other_tuned)
file5 = TFile.Open(prefix + Tx_0_8)
file6 = TFile.Open(prefix + Tx_0_6)
files =[file2, file1, file3, file4, file5, file6]

print('2')

################
#for monitorname in ["AlignTracksInFTTrackMonitor_Q0"]:
#    ROOT.gStyle.SetOptStat(1)
#    source=[getattr(thisfile,monitorname) for thisfile in filein]
#    for var in variables:
#        c8=ROOT.TCanvas("","",1400,1000)
#               stack=ROOT.THStack("hs",f"{nodelabel}, compare {variables[0]}")
#        hist=source[0].FindObjectAny(var)
#        hist.SetLineColor(ROOT.kBlack)
#               hist.SetLineWidth(3)
#        stack.Add(hist)
################
filein = []
for fileintag in [prefix + no_tuning,
                  prefix + with_tuning,
                  prefix + small_Tx,
                  prefix + oldTx_other_tuned,
                  prefix + Tx_0_8,
                  prefix + Tx_0_6]:

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
    hist.Scale(1/(hist.Integral()))
    hist.GetXaxis().SetTitle(var)
    hist.GetYaxis().SetTitle("Events")

    hist1=source[1].FindObjectAny(var)  
    hist1.SetLineColor(ROOT.kRed)
    hist1.SetLineWidth(2)
    hist1.SetMarkerStyle(20)
    hist1.SetMarkerSize(0.8)
    hist1.SetMarkerColor(ROOT.kRed)
    hist1.Scale(1/(hist1.Integral()))

    hist2=source[2].FindObjectAny(var)
    hist2.SetLineColor(ROOT.kBlue)
    hist2.SetLineWidth(2)
    hist2.SetMarkerStyle(20)
    hist2.SetMarkerSize(0.8)
    hist2.SetMarkerColor(ROOT.kBlue)
    hist2.Scale(1/(hist2.Integral()))
    
    hist3=source[3].FindObjectAny(var)
    hist3.SetLineColor(ROOT.kGreen)
    hist3.SetLineWidth(2)
    hist3.SetMarkerStyle(20)
    hist3.SetMarkerSize(0.8)
    hist3.SetMarkerColor(ROOT.kGreen)
    hist3.Scale(1/(hist3.Integral()))
    
    hist4=source[4].FindObjectAny(var)
    hist4.SetLineColor(ROOT.kYellow)
    hist4.SetLineWidth(2)
    hist4.SetMarkerStyle(20)
    hist4.SetMarkerSize(0.8)
    hist4.SetMarkerColor(ROOT.kYellow)
    hist4.Scale(1/(hist4.Integral()))
    
    hist5=source[5].FindObjectAny(var)
    hist5.SetLineColor(ROOT.kMagenta)
    hist5.SetLineWidth(2)
    hist5.SetMarkerStyle(20)
    hist5.SetMarkerSize(0.8)
    hist5.SetMarkerColor(ROOT.kMagenta)
    hist5.Scale(1/(hist5.Integral()))

    if var == 'chi2ProbVsMom':
        bins_f0, bins_f1, bins_f2 = [], [], []
        bins_f3, bins_f4, bins_f5 = [], [], []
    
        for bin in range(50):
            bins_f0.append(hist.GetBinContent(bin))
            bins_f1.append(hist1.GetBinContent(bin))
            bins_f2.append(hist2.GetBinContent(bin))
            bins_f3.append(hist3.GetBinContent(bin))
            bins_f4.append(hist4.GetBinContent(bin))
            bins_f5.append(hist5.GetBinContent(bin))
        print('maximum bin content of each file')
        print(f'max: {filenames[0]}', max(bins_f0)) 
        print(f'max: {filenames[1]}', max(bins_f1))
        print(f'max: {filenames[2]}', max(bins_f2))
        print(f'max: {filenames[3]}', max(bins_f3))
        print(f'max: {filenames[4]}', max(bins_f4))
        print(f'max: {filenames[5]}', max(bins_f5))

    stack.Add(hist)
    stack.Add(hist1)
    stack.Add(hist2)
    stack.Add(hist3)
    stack.Add(hist4)
    stack.Add(hist5)
    stack.Draw("nostack")
    if var == "FTResidual":
        hist.GetXaxis().SetLimits(-0.5, 0.5)
    if var == "chi2_per_ndof":
        hist.GetXaxis().SetLimits(0, 3.5)
    leg = ROOT.TLegend(0.7,0.7,0.8,0.85)
    leg.SetFillStyle(0)
    leg.SetFillColor(0)
    leg.SetBorderSize(0)
    leg.SetTextFont(132)
    leg.SetTextSize(0.055)
    leg.AddEntry(hist, "no tuning", "P")
    leg.AddEntry(hist1, "with tuning", "P")
    leg.AddEntry(hist2, "very small Tx", "P")
    leg.AddEntry(hist3, "old Tx, rest tuned", "P")
    leg.AddEntry(hist4, "0.8 Tx, rest tuned", "P")
    leg.AddEntry(hist5, "0.6 Tx, rest tuned", "P")
    leg.Draw()
    c3.Draw()
    c3.SaveAs(f"home/nbreer/fast_plotting_root/outfiles/comp_Tx/" + var + "_comp_normalised.pdf")
