import ROOT as r
from plotStyle import *
from tools import *
from collections import OrderedDict
r.gROOT.SetBatch(1)
SetPlotStyle()
r.TH1F.AddDirectory(0)
r.gROOT.ProcessLine("gErrorIgnoreLevel = 9999;")
import os
if not os.path.exists('clusterMultiplicity'):
    os.makedirs('clusterMultiplicity')

cmsText     = "CMS";
cmsTextFont   = 61  
cmsTextSize      = 1.75#0.75
extraText   = "Preliminary"
extraTextFont = 52 
sqrtsText = '13 TeV'

# 2016 pre VFP change
dataFill = 1 # Label for all fills in dataset, not actually Fill 1
year = 2016

dataFileName = 'landau_Data_Fill{fill}.root'.format( fill = dataFill )


# Which taus to plot
# -1 is for no APV simulation
# 0 is for best choice of tau for each layer, with possiblydifferent tau for each layer
taus = [ -1, 0 ]
fileNames = OrderedDict([
	('Data' , dataFileName)
])

if -1 in taus:
	fileNames['Default MC'] = 'landau_Sim_{year}_{fill}_default.root'.format(year = year, fill = dataFill)
	taus.remove(-1)

for tau in taus: fileNames['#tau = {tau}#mus'.format(tau=tau)] = 'landau_Sim_{year}_{fill}_{tau}us_newCharge.root'.format(year = year, fill = dataFill, tau = tau)

if 0 in taus:
	fileNames['With APV dynamic gain'] = fileNames['#tau = 0#mus']
	del fileNames['#tau = 0#mus']

niceColourList = [1, 9, 414, 633, 618]
if not 'Data' in fileNames.keys():
	print ('Must have a data file, going to crash')

pu_range_width = 10
minPU = 10
maxPU = 50
pu_ranges = [ [ minPU + pu_range_width * a, minPU + pu_range_width * (a+1) ] for a in range(0, int( (maxPU-minPU)/pu_range_width) )]


plotName = 'demo/nClusters_Vs_TruePU'

layers = [
'TIB1','TIB2','TIB3','TIB4',
'TOB1','TOB2','TOB3',
'TOB4','TOB5','TOB6',
'TID1','TID2','TID3',
'TEC1','TEC2','TEC3',
'TEC4','TEC5','TEC6',
'TEC7','TEC8','TEC9',
]

normToOne = True
rebinFactor = 1 # Tweaked later on for TIB/TOB

dirName = plotName.split('/')[-1]
projections_y = {}

projections_perFile = {}
projections_inclusvePU_perFile = {}

hists2_2d_reweighted = {}

# Get input histograms
# 2D histos of e.g. cluster charge vs PU
for counter, (label,fileName) in enumerate( fileNames.items() ):		
	inputFile = r.TFile(fileName)
	hists2_2d_reweighted[label] = get2DHists(layers, inputFile, plotName )



for counter, (label,fileName) in enumerate( fileNames.items() ):
	inputFile = r.TFile(fileName)

	projections_perFile[label] = get1DProjections( layers, inputFile, plotName, pu_ranges, normFactor = 1, rebinFactor = 1 )

dataProjections = projections_perFile['Data']

puLabels = []
for pu_range in pu_ranges:
	puRangeLabel = 'PU range : {min} to {max}'.format( min = pu_range[0], max = pu_range[-1])
	puLabels.append(r.TText(0.7, 0.6,puRangeLabel))
	puLabels[-1].SetNDC()
	puLabels[-1].SetTextAlign(22);
	puLabels[-1].SetTextFont(43);
	puLabels[-1].SetTextSize(15);

for layer in layers:
	can_projections = r.TCanvas('can_proj_{label}'.format(label=dirName),'can_proj_{label}'.format(label=dirName),900,900)
	can_projections.DivideSquare( len( pu_ranges ) + 1 )
	leg_projections = r.TLegend(0.1, 0.1, 0.9, 0.9)
	leg_projections.SetHeader(layer,"C")

	ratios = []
	for counter, pu_range in enumerate( pu_ranges ) :
		pad = can_projections.cd( counter + 1 )
		r.gPad.Divide(2)
		pad.cd(1).SetPad(0,0.4,1,1)
		pad.cd(2).SetPad(0,0.05,1,0.4)

		pu_range_label = getPURangeLabel( pu_range )
		dataHist = dataProjections[layer][pu_range_label]
		
		if normToOne : dataHist.Scale( 1 / dataHist.Integral() )
		dataHist.GetYaxis().SetTitle('Fraction of events')
		dataHist.GetYaxis().SetTitleSize( 0.1 )
		dataHist.GetYaxis().SetTitleOffset( 0.5 )
		dataHist.GetYaxis().SetLabelSize(0.08)
		dataHist.GetXaxis().SetLabelSize(0.0)
		dataHist.GetYaxis().SetNdivisions(403)
		lastNonZeroBin = dataHist.FindLastBinAbove(0)
		dataHist.GetXaxis().SetRange( 1, lastNonZeroBin + 1)

		if dataHist.GetBinCenter( lastNonZeroBin ) < 200 : 
			rebinFactor = 2+0
		elif dataHist.GetBinCenter( lastNonZeroBin ) < 400 : 
			rebinFactor = 4+0
		else: 
			rebinFactor = 8+0

		dataHist.Rebin( rebinFactor )
		lastNonZeroBin = dataHist.FindLastBinAbove(0)
		dataHist.GetXaxis().SetRange( 1, lastNonZeroBin + 1)

		dataHist.SetMarkerStyle(8)
		dataHist.SetMarkerColor(1)
		dataHist.SetLineColor(1)
		if counter == 0 : leg_projections.AddEntry(dataHist,'Data','P')

		drawOption = 'E'
		dataHist.SetMaximum( dataHist.GetMaximum() * 1.5 )
		p = pad.cd(1)
		p.SetBottomMargin(0.05)
		dataHist.Draw(drawOption)
		drawOption = 'HIST'

		isFirstHist = True
		firstTRatioPlot = None
		for simCounter, simLabel in enumerate( fileNames.keys() ):
			if simLabel == 'Data' : continue
			simHist = projections_perFile[simLabel][layer][pu_range_label]

			simHist.Rebin( rebinFactor )

			if normToOne : simHist.Scale( 1 / simHist.Integral() )
			simHist.SetLineColor( niceColourList[ simCounter ] )

			p = pad.cd(2)
			p.SetBottomMargin(0.3)
			p.SetTopMargin(0.05)

			ratios.append( simHist.Clone() )
			ratios[-1].GetXaxis().SetTitle('# clusters per event')
			ratios[-1].GetXaxis().SetLabelSize( 0.14 )
			ratios[-1].GetXaxis().SetTitleSize( 0.15 )
			ratios[-1].GetXaxis().SetTitleOffset( 0.8 )
			ratios[-1].GetYaxis().SetTitle('Ratio to Data')
			ratios[-1].GetYaxis().SetTitleSize( 0.15 )
			ratios[-1].GetYaxis().SetTitleOffset( 0.3 )
			ratios[-1].Divide( dataHist )
			ratios[-1].GetYaxis().SetNdivisions(2)
			ratios[-1].Draw(drawOption)
			ratios[-1].GetYaxis().SetLabelSize(0.15)
			ratios[-1].GetXaxis().SetRange(1,lastNonZeroBin+1)
			ratios[-1].SetMinimum(0.1)
			ratios[-1].SetMaximum(1.9)


			drawOption = 'HIST SAME'
			if counter == 0 : leg_projections.AddEntry(simHist,simLabel,'L')
			pad.cd(1)
			simHist.Draw(drawOption)
		pad.cd(1)
		dataHist.Draw('E SAME')

		# Add CMS labels	
		latex = r.TText(0.2, 0.8, cmsText)
		latex.SetTextFont(cmsTextFont)
		latex.SetTextAlign(11)
		latex.SetTextSize(cmsTextSize*pad.GetTopMargin())
		latex.DrawTextNDC(0.2,0.84, cmsText)
		latex.SetTextFont(extraTextFont)
		latex.SetTextAlign(11)
		latex.SetTextSize(0.76*cmsTextSize*pad.GetTopMargin())
		latex.DrawTextNDC(0.2,0.84-1.2*cmsTextSize*pad.GetTopMargin(), extraText)
		pad.Update()

		puLabels[counter].Draw()

		pad.cd(2).SetGridy()

	can_projections.cd( len( pu_ranges ) + 1 )
	leg_projections.Draw()
	can_projections.Update()

	can_projections.Print("clusterMultiplicity/"+layer+".png");

