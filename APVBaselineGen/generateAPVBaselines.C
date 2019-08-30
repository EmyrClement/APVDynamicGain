#include "TCanvas.h"
#include "TROOT.h"
#include "TF1.h"
#include "TLegend.h"
#include "TH1F.h"
#include "TFile.h"
#include "TParameter.h"
#include "TKey.h"
#include "TString.h"
#include "TRandom3.h"
#include <ROOT/TProcessExecutor.hxx>


using namespace std;

// The value of tau you are generating baselines for
double apv_decayConstantInMicroS = 22;

// Helper function to convert between Q (N. electrons) and mV
double QToV( double charge ) {
    return charge * 5.5 * 1.602e-4;
}

void generateAPVBaselines(){

    gErrorIgnoreLevel = kFatal;

    // Argument is how many cores you want to use
    ROOT::TProcessExecutor pool(20);

    // Input files contain fits of strip charge distribution (SCD) and occupancy
    // Both in bins of z and PU
    TFile *f = new TFile("scdFits.root", "READ");

    TRandom3 *random = new TRandom3();

    vector< TH1F > allBaselines;

    // Loop over all SCD fits in file
    for(auto k : *f->GetListOfKeys()) {

        // Get the TF1 for this SCD fit, and corresponding occupancy
        TKey *key = static_cast<TKey*>(k);
        TClass *cl = gROOT->GetClass(key->GetClassName());
        if (!cl->InheritsFrom("TF1")) continue;
        TF1 *func = (TF1*)key->ReadObj();
        TParameter<float> *occParam = 0;
        f->GetObject( TString( func->GetName() ) + TString( "_occupancy" ), occParam );
        double occupancy = occParam->GetVal() / 100;
        cout << func->GetName() << " " << occupancy << endl;

        // Set range of charge distribution
        // func->SetRange( 5000, 1000000 );
        func->SetRange( 5000, 2500000 );

        // Function for calculating baseline distribution for one SCD and occupancy, 
        // starting from no charge on a strip (i.e. similar to start of a fill)
        auto calculateBaseline = [=](int seed = 0 ) {

            // Histogram to store baseline distribution
            auto h_baseline = new TH1F(func->GetName(), func->GetName(), 82, 0, 738 );

            // Start with zero charge on strip
            double baselineQ = 0;

            // Maximum number of BX to consider
            unsigned int maxNBX = 100000;
            for ( unsigned i_BX = 0; i_BX < maxNBX; ++i_BX ) {

                // Decay away any remaining charge from previous BX
                // Exponential decay: exp( -25ns / tau us )
                if ( baselineQ > 0 ) baselineQ *= exp( - 25.0/1000.0 / apv_decayConstantInMicroS );

                // Store APV baseline (in mV) in each BX
                // Ignore first few BXs where there have not been many charge deposits
                // Conditions are then closer to the typical scenario in the middle of a fill
                if ( i_BX * occupancy > 20 ) {
                    if ( QToV( baselineQ ) > 729 ) {
                        h_baseline->Fill( 729 );
                    }
                    else {
                        h_baseline->Fill( QToV( baselineQ ) );
                    }
                }

                // Throw random number to decide whether a charge was deposited or not
                if ( random->Rndm() > occupancy ) {
                    continue;
                }

                // Sample the charge deposited and add to the baseline
                double charge = func->GetRandom();
                baselineQ += charge;

            }
            return h_baseline;
        };

        // Exectue the above function maxNBaselines time, on many cores
        // and combine output histograms
        // We repeat the process several times, rather than having just one 
        // long "fill", in case the early part of the "fill" can affect/dominate
        // the APV baseline dsitribution e.g. there could be a very large charge depostied 
        // very early on, which takes many BX to decay away.
        unsigned int maxNBaselines = 1000;
        auto seeds = ROOT::TSeqI(maxNBaselines);
        ROOT::ExecutorUtils::ReduceObjects<TH1F*> redfunc;
        auto h_baseline = pool.MapReduce(calculateBaseline, seeds, redfunc);

        // Normalise APV baseline distribution, and store in output vector
        h_baseline->Scale( 1 / h_baseline->Integral() );
        allBaselines.push_back( *h_baseline );
        f->cd();

    }


    // Output baselines to file
    // N.B. there is bug if I try to do this inside the previous loop (some histograms are corrupt)
    TFile *f_out = new TFile(TString("apvBaselines_fromC_")+TString(std::to_string( (int) apv_decayConstantInMicroS))+TString("us.root"), "RECREATE");
    f_out->cd();

    for ( auto h : allBaselines ) h.Write();
    f_out->Close();
}

int main(){
    generateAPVBaselines();
}
