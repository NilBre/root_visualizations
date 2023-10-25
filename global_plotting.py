import ROOT
from ROOT import TFile, TH1D
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
import argparse
import json

markers = ['o', 'x', 'D', 'd', '.', 'v', 's', 'p', '1']

path = 'global_alignment_files/'
name = 'GoodLongTracks_histo.root'

# input files
v1   = f'{path}v1/{name}'
v1_1 = f'{path}v1_1/{name}'
v1_2 = f'{path}v1_2/{name}'
v2   = f'{path}v2/{name}'
v2_1 = f'{path}v2_1/{name}'
v2_2 = f'{path}v2_2/{name}'
v3   = f'{path}v3/{name}'
v3_1 = f'{path}v3_1/{name}'
v3_2 = f'{path}v3_2/{name}'
Tx_10mu_TxRxRz_SmallSurveyRxUnc = 'root_500k/GoodLongTracks_TxRxRz_smallRxSurveyUnc.root'

labels = ['v1', 'v1_1', 'v1_2', 'v2', 'v2_1', 'v2_2', 'v3', 'v3_1', 'v3_2']

names = ["yT1", "yT2", "yT3", "xT1", "xT2", "xT3", "xT1","yT1","txT1", "txT2", "txT3", "tyT1", "tyT2", "tyT3", "unbiasedFTResidual", "RMSResidualModules", "RMSResidualQuarters"]

axes_titles = ["y T1 Station [mm]", "y T2 Station [mm]", "y T3 Station [mm]",
               "x T1 Station [mm]", "x T2 Station [mm]", "x T3 Station [mm]",
               "x T1 Station [mm]", "y T1 Station [mm]",
               "tx T1 Station", "tx T2 Station", "tx T3 Station",
               "ty T1 Station", "ty T2 Station", "ty T3 Station",
               "FT X Resiudual [mm]" , "RMS ResidualModules [mm]", "RMSResidualQuarters [mm]"]

names = ["FTResidual", "chi2_per_ndof", "chi2ProbVsMom"]
axes_titles = ["FT X Residual [mm]", "chi2 / ndof", "pT [MeV]"]

histos1 = []
histos2 = []
histos3 = []

for i in range(0,len(names)):
    histos1.append(TH1D())
    histos2.append(TH1D())
    histos3.append(TH1D())

filein = []
for fileintag in [
    v1,
    v1_1,
    v1_2,
    ]:

    filein.append(ROOT.TFile(fileintag))

monitorname = "TrackMonitor_GoodLongTracks"
monitorname = "TrackFitMatchMonitor__Event_TrackSelectionMerger_8b22d9f1_OutputLocation"

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

    hist1=source[1].FindObjectAny(var)
    hist1.GetXaxis().SetTitle(var)
    hist1.GetYaxis().SetTitle("Events")
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
        print(f'max: {filenames[0]}', max(bins_f1))
        print(f'max: {filenames[1]}', max(bins_f2))
        print(f'max: {filenames[2]}', max(bins_f3))

    stack.Add(hist1)
    stack.Add(hist2)
    stack.Add(hist7)

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
    leg.AddEntry(hist1, "10 micron TxRz", "P")
    leg.AddEntry(hist2, "10 micron TxTzRxRz", "P")
    leg.Draw()
    c3.Draw()
    c3.SaveAs("out_global_alignment/" + names[i] + f"{labels[i]}_.pdf")

histos1 = []
histos2 = []
histos3 = []

for i in range(0,len(names)):
    histos1.append(TH1D())
    histos2.append(TH1D())
    histos3.append(TH1D())

file1 = TFile.Open(v1)
file2 = TFile.Open(v1_1)
file3 = TFile.Open(v1_2)

# file1 = TFile.Open(v2)
# file2 = TFile.Open(v2_1)
# file3 = TFile.Open(v2_2)

# file1 = TFile.Open(v3)
# file2 = TFile.Open(v3_1)
# file3 = TFile.Open(v3_2)

files =[file1, file2, file3]

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

line = TLine()
for i in range(0,len(histos1)):
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
    leg.AddEntry(histos1[i], f"{labels[0]}", "P")
    leg.AddEntry(histos2[i], f"{labels[1]}", "P")
    leg.AddEntry(histos3[i], f"{labels[2]}", "P")
    leg.Draw()
    T1 = TLatex()
    T1.SetTextSize(0.05)
    T1.DrawLatexNDC(.25,.80, "LHCb Internal")
    T1.DrawLatexNDC(.25,.75, "Run 269045")

    c.SaveAs("out_global_alignment/" + names[i] + f"{labels[i]}_.pdf")
