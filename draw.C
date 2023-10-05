void draw(){
	using namespace RooFit;

	gROOT->ProcessLine(".x ~/lhcbStyle.C");
        gStyle->SetOptStat(0);

	TChain* chain = new TChain("Tuple/DecayTree");
	chain->Add("tuple.root");

	TCut massCut = "D0_M>1800 && D0_M<1925";

	//TCut totCut="muminus_PIDmu>0 && muplus_PIDmu>0 && muplus_IsMuon==1 && muminus_IsMuon==1 && muplus_PT>700 && muminus_PT>700 && muplus_P>3000 && muminus_P>3000 && muplus_P<500000&&muminus_P<500000 && ((Jpsi_END_VZ-Jpsi_BPVZ)*Jpsi_M/Jpsi_PZ<10) ";
 	TCut totCut="";
        //TCut totCut="muminus_PIDmu>0 && muplus_PIDmu>0";
	//TTree *tree = chain->CopyTree(totCut+run_cut);
	TTree *tree = chain->CopyTree(totCut+massCut);
	std::cout << " tree entries : " << tree->GetEntries() << std::endl;

	double TotalSize = tree->GetEntries();
	RooRealVar x1("D0_M", "#it{m}_{#it{K^{-}#pi^{+}}}[MeV/#it{c}^{2}]", 1800, 1925);
	//RooDataHist * dataHist1 = new RooDataHist("dataHist", "dataHist", x1, Import(*h1, kFALSE));

	// Import only observables (y,z)
	RooDataSet* dataHist1 = new RooDataSet("dataHist", "", tree, RooArgSet(x1) );
	dataHist1->Print();

	// signal
	//RooRealVar mean1("#mu", "mean", 1865., 3100-10.0, 3100+10.0); // parameter (name, description,
	//RooRealVar sigma1("#sigma", "width", 13, 5, 25.0);
	//RooGaussian *SigMPdf1 = new RooGaussian("SigMPdf1","SigMPdf1", x1, mean1, sigma1);

	RooRealVar *SigM= new RooRealVar("M(B^{-})","",1865, 1865-10.0, 1865+10.0,"MeV/#it{c}^{2}");
	RooRealVar *SigMRes  = new RooRealVar("#sigma_{M}",    "", 8, 1, 20, "MeV/#it{c}^{2}");
	RooRealVar *SigMRes2 = new RooRealVar("#sigma_{M,2}",  "",  8, 1, 30, "MeV/#it{c}^{2}");

	//RooRealVar n1("n1","",35.221,0.1,50);
	//RooRealVar n2("n2","",35.221,0.1,50);
	RooRealVar n1("n1","",35.221);
	RooRealVar n2("n2","",35.221);
	RooRealVar a1("a1","", 1.5,    0, 100);
	RooRealVar a2("a2","", -1.5,   -30, 0.1);
	//RooRealVar a2("a2","",-4.0,-20, 0);

	//RooCBShape SigMPdf1("CB1","",x1,*SigM,*SigMRes ,a1, n1);
	//RooCBShape SigMPdf2("CB2","",x1,*SigM,*SigMRes2,a2, n2);

	RooGaussian SigMPdf1("CB1", "Gaussian PDF", x1, *SigM,*SigMRes);
	RooGaussian SigMPdf2("CB2", "Gaussian PDF", x1, *SigM,*SigMRes2);

	RooRealVar CB_fr("CB_fr","",0.45,0.2,0.8);
	//RooAddPdf *SigMPdf = new RooAddPdf("SigMPdf","SigMPdf", RooArgList(SigMPdf1,SigMPdf2),RooArgList(CB_fr));
	RooAddPdf *SigMPdf = new RooAddPdf("SigMPdf","SigMPdf", RooArgList(SigMPdf1,SigMPdf2),RooArgList(CB_fr));


	// combination bkg
	RooRealVar *p01=new RooRealVar("p0","p0",-0.,-0.5,0.5,"MeV/c^{2}");
	RooAbsPdf *comb_BkgMPdf1=new RooExponential("comb_BkgMPdf1","combine BkgMPdf1",x1,*p01);
	// number
	RooRealVar *nSig1 = new RooRealVar("N_{Sig}","nsig",TotalSize*0.4,0, TotalSize*1.3);
	RooRealVar *nBkg_comb1 = new RooRealVar("N_{Bkg_comb}","nbkg combination", TotalSize*0.6,0, TotalSize);
	//RooAbsPdf *MassPdf=new RooAddPdf("MassPdf","mass_pdf",RooArgList(SigMPdf1, *comb_BkgMPdf1),RooArgList(*nSig1,*nBkg_comb1));
	RooAbsPdf *MassPdf=new RooAddPdf("MassPdf","mass_pdf",RooArgList(*SigMPdf, *comb_BkgMPdf1),RooArgList(*nSig1,*nBkg_comb1));


        //Do the fit
        RooFitResult* fitRes1 = MassPdf -> fitTo( *dataHist1, Extended(kTRUE), SumW2Error(kTRUE), NumCPU(1), PrintLevel(1), Save());
	fitRes1->Print();

	//double sigma = sqrt( SigMRes->getVal()*SigMRes->getVal()*(1-CB_fr.getVal()) + SigMRes2->getVal()*SigMRes2->getVal()*CB_fr.getVal() );


	TCanvas *MyCan = new TCanvas("MyCan","", 1000,700);
	MyCan->SetFillColor(kWhite);

	RooPlot * range = x1.frame(Name("range"), Bins(100-3), Title("Mixed Sample"));
	range->GetYaxis()->SetTitle("Candidates/(3MeV/#it{c}^{2})");

	dataHist1->plotOn(range, MarkerColor(kBlack), Name("data"), DataError(RooAbsData::SumW2));
	MassPdf->plotOn(range, Name("signal"), Components("SigMPdf"), LineColor(kRed), FillColor(kRed), RooFit::FillStyle(3013), DrawOption("F") );  
	//MassPdf->plotOn(range, Name("signal"), Components("SigMPdf"), LineColor(kRed)  );  
	MassPdf->plotOn(range, Name("background"), Components("comb_BkgMPdf1"), LineColor(6) );    
	MassPdf->plotOn(range, Name("CB1"), Components("CB1"), LineColor(9) );
	MassPdf->plotOn(range, Name("CB2"), Components("CB2"), LineColor(10) );
	
        MassPdf->plotOn(range, Name("fit"), LineColor(kBlue) );
	dataHist1->plotOn(range, MarkerColor(kBlack), Name("data"), DataError(RooAbsData::SumW2));
	dataHist1->plotOn(range, MarkerColor(kBlack), Name("data"), DataError(RooAbsData::SumW2));
	range->Draw();

#if 1 
	auto legend = new TLegend(0.15,0.7,0.48,0.9);
	legend->AddEntry("data", "Data", "ep");
	legend->AddEntry("fit", "Fit", "l");
	legend->AddEntry("signal", "Signal", "F");
	legend->AddEntry("background", "Background", "l");
	//legend->AddEntry((TObject*)0, "", "");
	legend->Draw("same");
#endif


        TLatex latex;
        latex.SetTextSize(0.045);
        latex.SetTextAlign(12);  //align at top
        int maxy = tree->GetEntries()*0.04 ; 
	//latex.DrawLatex(1880, 0.9*maxy, "Run 256145");
	latex.DrawLatex(1880, 0.9*maxy, "LHCb 2023 : 269377");
	//latex.DrawLatex(1880, 0.8*maxy, "V10 Alignment");
        latex.DrawLatex(1880, 0.8*maxy, Form("#mu=%.1f #pm %.1f MeV/#it{c}^{2}", SigM->getVal(), SigM->getError() ) );
        //latex.DrawLatex(1880, 0.8*maxy, Form("#mu=%.1f", SigM->getVal()) );
        latex.DrawLatex(1880, 0.7*maxy, Form("#sigma1=%.1f #pm %.1f MeV/#it{c}^{2}", SigMRes->getVal(), SigMRes->getError() ) );
        latex.DrawLatex(1880, 0.6*maxy, Form("#sigma2=%.1f #pm %.1f MeV/#it{c}^{2}", SigMRes2->getVal(), SigMRes2->getError() ) );
        //latex.DrawLatex(1880, 0.7*maxy, Form("#sigma=%.1f #pm %.1f", sigma1.getVal(), sigma1.getError()) );
        latex.DrawLatex(1880, 0.5*maxy, Form("N_{sig}=%.0f #pm %.0f", nSig1->getVal(), nSig1->getError()) );
        latex.DrawLatex(1880, 0.4*maxy, Form("N_{bkg}=%.0f #pm %.0f", nBkg_comb1->getVal(), nBkg_comb1->getError()) );

	double this_sigma = sqrt( CB_fr.getVal()*SigMRes->getVal()*SigMRes->getVal() + (1-CB_fr.getVal())*SigMRes2->getVal()*SigMRes2->getVal() );
        //latex.DrawLatex(1880, 0.3*maxy, Form("#sigma=%.1f MeV/#it{c}^{2}", CB_fr.getVal()*SigMRes->getVal() + (1-CB_fr.getVal())*SigMRes2->getVal() ) );
        latex.DrawLatex(1880, 0.3*maxy, Form("#sigma=%.1f MeV/#it{c}^{2}", this_sigma ) );

	//TImage *img = TImage::Open("lhcb-commissioning-logo.png");

	//if (!img) {
	//	printf("Could not create an image... exit\n");
	//	return;
	//}

	//TPad *l2 = new TPad("l2","l2",0.55,0.0,0.8,0.3);
	//l2->SetFillColor(18);
	//l2->Draw();

	TPad *l = new TPad("l","l",0.15,0.35,0.4,0.68);
	//l->SetFillColor(15);
	l->Draw("same");
	//gPad->cd(0);
	l->cd();
	img->Draw("");
	l->Draw();

	MyCan->cd();
	MyCan->Update();

	//MyCan->Print( "Jpsi_mass.pdf" );
	MyCan->SaveAs( "D0_mass.pdf" );


#if 0 
//create a new RooDataSet with sweight~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	RooDataSet *t_data = new RooDataSet(dataHist1->GetName(),dataHist1->GetTitle(), dataHist1, *dataHist1->get());
	//RooStats::SPlot *sdata = new RooStats::SPlot("sdata","An SPlot",*t_data,MassPdf,RooArgList(*nSig,*nBkg_comb));
	RooStats::SPlot *sdata = new RooStats::SPlot("sdata","An SPlot",*t_data, MassPdf, RooArgList(*nSig1,*nBkg_comb1) );
	//RooStats::SPlot *sdata = new RooStats::SPlot("sdata","An SPlot",*t_data,MassPdf,RooArgList(*nSig, *nSig_rho, *nBkg_comb));
	//TFile f("/projects/lhcb/users/xuzh/PentaQuark/Lb2Lc/RootFiles/SweightTree_run1.root","recreate");
	TFile f("tuple_TxRz+TzRx.root","recreate");


	TTree *newtree = tree->CloneTree(0);
	Float_t Sweight_sig; newtree->Branch("Sweight_sig",&Sweight_sig,"Sweight_sig/F");
	Float_t Sweight_bkg; newtree->Branch("Sweight_bkg",&Sweight_bkg,"Sweight_bkg/F");

	t_data->Print();
	int evtnum = t_data->numEntries();
	cout<< "The total number of events: "<< evtnum << endl;

	RooRealVar* sweight_sig = (RooRealVar*)t_data->get()->find("N_{Sig}_sw");
	RooRealVar* sweight_bkg = (RooRealVar*)t_data->get()->find("N_{Bkg_comb}_sw");
	//RooRealVar* sweight_bkg_rho = (RooRealVar*)t_data->get()->find("N_{Sig_rho}_sw");

	for(int i=0;i<evtnum;i++)
	{
		t_data->get(i);
		tree->GetEntry(i);

		Sweight_sig = sweight_sig->getVal();
		Sweight_bkg = sweight_bkg->getVal();
		//Sweight_rho = sweight_bkg_rho->getVal();

		//cout << Sweight_sig << "  vs " << Sweight_bkg << endl;
		newtree->Fill();

	}
	newtree->Write();
	f.Close();

#endif

}
