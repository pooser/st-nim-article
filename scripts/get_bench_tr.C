#include <TMath.h>
#include <TH1I.h>
#include <TH2I.h>
#include <TFile.h>
#include <TTree.h>
#include <TGraphErrors.h>
#include <TCanvas.h>
#include <TMultiGraph.h>

#include <vector>
#include <iostream>

using namespace std;

// Declare constants
static const Int_t NOP = 30;  // Number of scintillator paddles
static const Int_t NOL = 12;  // Number of source locations
static const Int_t TDC_MIN = 1700;
static const Int_t TDC_MAX = 2000;
static const Int_t NTDC_BINS = 150;
static const Double_t FWHM = 2.355;
// Array of source positions for each paddle
static const Double_t pos[NOL]  = {8.682, 16.575, 24.467, 32.360, 40.940, 42.190, 43.424, 47.106, 50.084, 53.062, 56.040, 59.018};

TFile *df[NOP][NOL];

TTree *camac[NOP][NOL];

TH1F *h_tdc[NOP][NOL];

Float_t SiPM_Tout_CFD_TDC[NOP][NOL];

Int_t nentries[NOP][NOL];

TF1 *init_fit[NOP][NOL], *final_fit[NOP][NOL];

ofstream otf;

void get_bench_tr() {

  // Create output ROOT file
  otf.open("../data/time_res_bench.dat");
  otf << "# paddle number | source location (cm) | time resolution (ps) | time resoltuion error (ps)" << endl;

  // Loop through all root files and acqure the data 
  for (UInt_t ipad = 0; ipad < NOP; ipad++) {  // Paddle loop
    for (UInt_t ipos = 0; ipos < NOL; ipos++) {  // Source location loop

      // Acquire the data files
      df[ipad][ipos] = new TFile(Form("../ROOTfiles/Sector_ROOT_Data/Bar_%d/zpos_%1.3f.root", ipad+1, pos[ipos]));
      // Acquire the camac tree and acquire the tdc cfd leafs 
      camac[ipad][ipos] = dynamic_cast <TTree*> (df[ipad][ipos]->Get("camac"));
      camac[ipad][ipos]->SetBranchAddress("SiPM_Tout_CFD_TDC", &SiPM_Tout_CFD_TDC[ipad][ipos]);
      // Book tdc histos
      h_tdc[ipad][ipos] = new TH1F(Form("tdc_histo_bar_%d_zpos_%1.3f.root", ipad+1, pos[ipos]), "CFD TDC; TDC Channels; Number of Entries / 2 TDC Channels", NTDC_BINS, TDC_MIN, TDC_MAX);
      // Acquire the number of entries in each leaf
      nentries[ipad][ipos] = (Int_t) camac[ipad][ipos]->GetEntries();  
      // Loop of entries and fill the tdc histograms
      for (UInt_t ientry = 0; ientry < nentries[ipad][ipos]; ientry++) {  // Entry loop
	// Acquire the individual entries
	camac[ipad][ipos]->GetEntry(ientry);
	h_tdc[ipad][ipos]->Fill(SiPM_Tout_CFD_TDC[ipad][ipos]);
      }  // Entry loop

      // Declare initial fits and initialize fit parameters
      init_fit[ipad][ipos] = new TF1(Form("init_fit_bar_%d_zpos_%d", ipad+1, ipos), "gaus", TDC_MIN, TDC_MAX);
      init_fit[ipad][ipos]->SetParameters(h_tdc[ipad][ipos]->GetMaximum(),
					  h_tdc[ipad][ipos]->GetMean(),
					  h_tdc[ipad][ipos]->GetRMS());
      // Perform the initial fits
      h_tdc[ipad][ipos]->Fit(Form("init_fit_bar_%d_zpos_%d", ipad+1, ipos), "QR");
      // Declare final fits and initialize fit parameters
      final_fit[ipad][ipos] = new TF1(Form("final_fit_bar_%d_zpos_%d", ipad+1, ipos), "gaus", TDC_MIN, TDC_MAX);
      final_fit[ipad][ipos]->SetParameters(init_fit[ipad][ipos]->GetParameter(0),
					   init_fit[ipad][ipos]->GetParameter(1),
					   init_fit[ipad][ipos]->GetParameter(2));
      // Define the fit range
      final_fit[ipad][ipos]->SetRange(init_fit[ipad][ipos]->GetParameter(1) - FWHM*init_fit[ipad][ipos]->GetParameter(2),
				      init_fit[ipad][ipos]->GetParameter(1) + FWHM*init_fit[ipad][ipos]->GetParameter(2));
      // Perform the final fit
      h_tdc[ipad][ipos]->Fit(Form("final_fit_bar_%d_zpos_%d", ipad+1, ipos), "QR");

      // Write the data to a text file
      otf << ipad+1 << "\t" << pos[ipos] << "\t\t" 
	  << final_fit[ipad][ipos]->GetParameter(2)*50.0 << "\t\t"
	  << final_fit[ipad][ipos]->GetParError(2)*50.0 << endl;

    }  // Source location loop
  }  // Paddle loop
}
