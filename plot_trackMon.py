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

#no_tuning = 'GoodLongTracks_best_strict.root' # strict selection
prefix = 'root_500k/'
# no_tuning = 'GoodLongTracks_base_500k_i10.root' # base, probably 200k but not sure (also not sure if loose or strict)
# with_tuning = 'GoodLongTracks_histo_i8_500k_loose.root' # 500k best, converged
# Tx_micron_10 = 'GoodLongTracks_Tx_10micron_Rz_better.root'
# Tx_2mm = 'GoodLongTracks_2mm_Tx.root'
# oldTx_other_tuned = "GoodLongTracks_oldTx_rest_tuned.root"
# Tx_0_8 = "GoodLongTracks_0_8_onlyTx.root"
# Tx_0_6 = "GoodLongTracks_0_6_onlyTx.root"
# small_Tx = "GoodLongTracks_tuned_0_0001_Tx.root"

Tx_2mm = 'GoodLongTracks_2mm_Tx.root'
Tx_micron_10 = 'GoodLongTracks_Tx_10micron_Rz_better.root' # this uses TxRz
Tx_10mu_TxTzRxRz = 'GoodLongtracks_TxTzRxRz_iter4_10micron_tuned.root'
Tx_100mu_TxRz = 'GoodLongTracks_100mu_TxRz_iter15.root'

filenames = [
            # 'no_tuning',
            # 'with_tuning',
            '2_micron',
            '10_micron',
            '10_TxTzRxRz',
            '100_TxRz',
            # '1_micron',
            # '0_8_micron',
            # '0_6_micron',
            # '0_1_micron',
            ]

names = ["FTResidual", "chi2_per_ndof", "chi2ProbVsMom"]
axes_titles = ["FT X Residual [mm]", "chi2 / ndof", "pT [MeV]"]

histos1 = []
histos2 = []
histos3 = []
histos4 = []
# histos5 = []
# histos6 = []
# histos7 = []
# histos8 = []
for i in range(0,len(names)):
    histos1.append(TH1D())
    histos2.append(TH1D())
    histos3.append(TH1D())
    histos4.append(TH1D())
    # histos5.append(TH1D())
    # histos6.append(TH1D())
    # histos7.append(TH1D())
    # histos8.append(TH1D())
print('1')

filein = []
for fileintag in [
                #   prefix + no_tuning,
                #   prefix + with_tuning,
                  prefix + Tx_2mm,
                  prefix + Tx_micron_10,
                  prefix + Tx_10mu_TxTzRxRz,
                  prefix + Tx_100mu_TxRz,
                  # prefix + oldTx_other_tuned,
                  # prefix + Tx_0_8,
                  # prefix + Tx_0_6,
                  # prefix + small_Tx
                 ]:

    filein.append(ROOT.TFile(fileintag))

monitorname = "TrackMonitor_GoodLongTracks"

ROOT.gStyle.SetOptStat(1)

source = [getattr(file, monitorname) for file in filein]
source = [getattr(label, "Long") for label in source]

for var in names:
    c3 = ROOT.TCanvas("","",1200,900)
    stack=ROOT.THStack("hs","joint uncertainties tuning")
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

    hist3=source[3].FindObjectAny(var)
    hist3.SetLineColor(ROOT.kYellow)
    hist3.SetLineWidth(2)
    hist3.SetMarkerStyle(20)
    hist3.SetMarkerSize(0.8)
    hist3.SetMarkerColor(ROOT.kYellow)
    # hist3.Scale(1/(hist3.Integral()))

    # hist4=source[4].FindObjectAny(var)
    # hist4.SetLineColor(ROOT.kGreen)
    # hist4.SetLineWidth(2)
    # hist4.SetMarkerStyle(20)
    # hist4.SetMarkerSize(0.8)
    # hist4.SetMarkerColor(ROOT.kGreen)
    # # hist4.Scale(1/(hist4.Integral()))
    #
    # hist5=source[5].FindObjectAny(var)
    # hist5.SetLineColor(ROOT.kMagenta)
    # hist5.SetLineWidth(2)
    # hist5.SetMarkerStyle(20)
    # hist5.SetMarkerSize(0.8)
    # hist5.SetMarkerColor(ROOT.kMagenta)
    # # hist5.Scale(1/(hist5.Integral()))
    #
    # hist6=source[6].FindObjectAny(var)
    # hist6.SetLineColor(ROOT.kCyan)
    # hist6.SetLineWidth(2)
    # hist6.SetMarkerStyle(20)
    # hist6.SetMarkerSize(0.8)
    # hist6.SetMarkerColor(ROOT.kCyan)
    # # hist6.Scale(1/(hist6.Integral()))
    #
    # hist7=source[7].FindObjectAny(var)
    # hist7.SetLineColor(ROOT.kOrange)
    # hist7.SetLineWidth(2)
    # hist7.SetMarkerStyle(20)
    # hist7.SetMarkerSize(0.8)
    # hist7.SetMarkerColor(ROOT.kOrange)
    # # hist7.Scale(1/(hist7.Integral()))

    if var == 'chi2ProbVsMom':
        bins_f0, bins_f1, bins_f2 = [], [], []
        bins_f3, bins_f4, bins_f5 = [], [], []
        bins_f6, bins_f7 = [], []
        for bin in range(50):
            bins_f0.append(hist.GetBinContent(bin))
            bins_f1.append(hist1.GetBinContent(bin))
            bins_f2.append(hist2.GetBinContent(bin))
            bins_f3.append(hist3.GetBinContent(bin))
            # bins_f4.append(hist4.GetBinContent(bin))
            # bins_f5.append(hist5.GetBinContent(bin))
            # bins_f6.append(hist6.GetBinContent(bin))
            # bins_f7.append(hist7.GetBinContent(bin))

        print('maximum bin content of each file')
        print(f'max: {filenames[0]}', max(bins_f0))
        print(f'max: {filenames[1]}', max(bins_f1))
        print(f'max: {filenames[2]}', max(bins_f2))
        print(f'max: {filenames[3]}', max(bins_f3))
        # print(f'max: {filenames[4]}', max(bins_f4))
        # print(f'max: {filenames[5]}', max(bins_f5))
        # print(f'max: {filenames[6]}', max(bins_f6))
        # print(f'max: {filenames[7]}', max(bins_f7))

    stack.Add(hist)
    stack.Add(hist1)
    stack.Add(hist2)
    stack.Add(hist3)
    # stack.Add(hist4)
    # stack.Add(hist5)
    # stack.Add(hist6)
    # stack.Add(hist7)

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
    # leg.AddEntry(hist, "no tuning", "P")
    # leg.AddEntry(hist1, "with tuning", "P")
    leg.AddEntry(hist, "2 micron", "P")
    leg.AddEntry(hist1, "10 micron TxRz", "P")
    leg.AddEntry(hist2, "10 micron TxTzRxRz", "P")
    leg.AddEntry(hist3, "100 micron TxRz", "P")
    # leg.AddEntry(hist4, "1 micron", "P")
    # leg.AddEntry(hist5, "0.8 micron", "P")
    # leg.AddEntry(hist6, "0.8 micron", "P")
    # leg.AddEntry(hist7, "0.1 micron", "P")
    leg.Draw()
    c3.Draw()
    c3.SaveAs(f"outfiles/compi/" + var + "_comp_looser.pdf")
