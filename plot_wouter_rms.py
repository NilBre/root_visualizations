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

prefix = 'root_500k/'

no_tuning = 'GoodLongTracks_base_500k_i10.root' # base, probably 200k but not sure (also not sure if loose or strict)
with_tuning = 'GoodLongTracks_histo_i8_500k_loose.root' # 500k best, converged
Tx_micron_10 = 'GoodLongTracks_Tx_10micron_Rz_better.root'
print('finished reading data')

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
for i in range(0,len(names)):
    histos1.append(TH1D())
    histos2.append(TH1D())
    histos3.append(TH1D())

file1 = TFile.Open(prefix + no_tuning)
file2 = TFile.Open(prefix + with_tuning)
file3 = TFile.Open(prefix + Tx_micron_10)

files =[file2, file3, file1]

for f in range(0,len(files)):
    for n in range(0,len(names)):
        dir2 = files[f].GetDirectory("FTTrackMonitor_GoodLongTracks")
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
print('4')

c = ROOT.TCanvas()
ROOT.gStyle.SetOptStat(0)

line = TLine()
for i in range(0,len(histos1)):
    histos1[i].SetMarkerStyle(20)
    histos1[i].SetMarkerSize(0.8)
    histos1[i].SetMarkerColor(2)
    histos1[i].SetLineColor(2)
    histos1[i].GetYaxis().SetTitle(axes_titles[i])
    histos1[i].GetXaxis().SetTitle("Module numbers")
    histos1[i].GetYaxis().SetRangeUser(-0.03, 0.03)
#    histos1[i].Scale(1/(histos1[i].Integral())) # also comment that out when binning is wrong
    histos1[i].Draw("EP")

    histos2[i].SetMarkerColor(4)
    histos2[i].SetLineColor(4)
    histos2[i].SetMarkerStyle(22)
    histos2[i].SetMarkerSize(0.8)
#    histos2[i].Scale(1/(histos2[i].Integral())) # comment that out if binning is wrong
    histos2[i].Draw("EP same")

    histos3[i].SetMarkerColor(5)
    histos3[i].SetLineColor(5)
    histos3[i].SetMarkerStyle(22)
    histos3[i].SetMarkerSize(0.8)
#    histos2[i].Scale(1/(histos2[i].Integral())) # comment that out if binning is wrong
    histos3[i].Draw("EP same")

    leg = ROOT.TLegend(0.6,0.7,0.8,0.9)
    leg.SetFillStyle(0)
    leg.SetFillColor(11)
    leg.SetBorderSize(0)
    leg.SetTextFont(132)
    leg.SetTextSize(0.053)
    leg.AddEntry(histos1[i], "with tuning", "P")
    leg.AddEntry(histos2[i], "tuned, 10 micron in Tx", "P")
    leg.AddEntry(histos3[i], "no tuning", "P")
    leg.Draw()
    #c1.SetLogx()
    #c.BuildLegend(0.5,0.3,0.8,0.5,"","P") #0.5,0.3,0.8,0.5
    T1 = TLatex()
    T1.SetTextSize(0.05)
    T1.DrawLatexNDC(.25,.80, "LHCb Internal")
    T1.DrawLatexNDC(.25,.75, "Run 269045")

    c.SaveAs("outfiles/compi/wp2_comparison/" + names[i] + "_with_vs_without.pdf")
