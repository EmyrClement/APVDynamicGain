import ROOT as r
from plotStyle import *
from tools import *
from collections import OrderedDict
r.gROOT.SetBatch(1)
SetPlotStyle()
r.TH1F.AddDirectory(0)
r.gROOT.ProcessLine("gErrorIgnoreLevel = 9999;")
import os
if not os.path.exists('clusterCharge'):
    os.makedirs('clusterCharge')

cmsText     = "CMS";
cmsTextFont   = 61  
cmsTextSize      = 1#0.75
extraText   = "Preliminary"
extraTextFont = 52 
sqrtsText = '13 TeV'
lumiText = '0.44 fb^{-1} (13 TeV)'

# 2016 pre VFP change
dataFill = 1 # Label for all fills in dataset, not actually Fill 1
year = 2016

# dataFileName = 'landau_Data_Fill{fill}.root'.format( fill = dataFill )
dataFileName = '/Users/ec6821/Documents/sc01/HIP/CMSSW_10_6_12/src/APVDynamicGain/ChargeAna/python/landau_Data.root'

# Which taus to plot
# -1 is for no APV simulation
# 0 is for best choice of tau for each layer, with possiblydifferent tau for each layer
taus = [ -1 ]

fileNames = OrderedDict([
	('Data' , dataFileName)
])

if -1 in taus:
	fileNames['MC EOY'] = 'landau_Sim_{year}_{fill}_default.root'.format(year = year, fill = dataFill)
	taus.remove(-1)


for tau in taus: fileNames['#tau = {tau}#mus'.format(tau=tau)] = 'landau_Sim_{year}_{fill}_{tau}us_newCharge.root'.format(year = year, fill = dataFill, tau = tau)

if 0 in taus:
	fileNames['With APV dynamic gain'] = fileNames['#tau = 0#mus']
	del fileNames['#tau = 0#mus']

niceColourList = [1, 9, 414, 633, 618]
if not 'Data' in fileNames.keys():
	print ('Must have a data file, going to crash')

fileNames['MC (with APV simulation)'] = '/Users/ec6821/Documents/sc01/HIP/CMSSW_10_6_12/src/APVDynamicGain/ChargeAna/python/landau_Sim.root'

puRangeCalib = [0,50]
pu_range_width = 40
minPU = 10
maxPU = 50
pu_ranges = [ [ minPU + pu_range_width * a, minPU + pu_range_width * (a+1) ] for a in range(0, int( (maxPU-minPU)/pu_range_width) )]


plotName = 'demo/ClusterCharge_Vs_TruePU'

# If "afterG2", then use my implementation of G2 calibration
# Otherwise use simple calibration, where MPV of landau in simulation is scaled on-the-fly to match data
afterG2 = 'afterG2' in plotName

layers = [
# 'TIB1','TIB2','TIB3','TIB4',
# 'TOB1','TOB2','TOB3',
# 'TOB4','TOB5','TOB6',
# 'TID1','TID2','TID3',
# 'TEC1','TEC2','TEC3',
# 'TEC4','TEC5','TEC6',
# 'TEC7','TEC8','TEC9',

'TIB1',
'TOB1',
'TID1',
'TEC1'
]

normToOne = True
rebinFactor = 24

dirName = plotName.split('/')[-1]
projections_y = {}

maxCharge = -1
if 'LeadingStripCharge' in plotName:
	maxCharge = 63200

dataNorms = {}
dataMax = {}
dataMPVs = {}
mpvs = {}

projections_perFile = {}
projections_inclusvePU_perFile = {}
nEventsInPURange = {}
puWeightHists = {}

hists2_2d_reweighted = {}

nEventsInPURange, puWeightHists = getNumEventsInPURanges( fileNames, pu_ranges )

# Get input histograms
# 2D histos of e.g. cluster charge vs PU
for counter, (label,fileName) in enumerate( fileNames.items() ):		
	inputFile = r.TFile(fileName)
	if afterG2 and ( label == 'Data' or label == 'Default MC'):
		hists2_2d_reweighted[label] = get2DHists(layers, inputFile, plotName.split('_afterG2')[0] )
	else:
		hists2_2d_reweighted[label] = get2DHists(layers, inputFile, plotName )

# Apply calibration to histograms
# i.e. make MPV in simulation match that in data
if not afterG2:
	for label in puWeightHists:
		mpvs[label] = {}
		for layer, hist2d in hists2_2d_reweighted[label].items():

			# Calculate MPV for this simulation and layer
			proj = hist2d.ProjectionY('temp').Clone().Rebin(1)

			# Cross check...
			maxBin = proj.GetMaximumBin()
			mpv_maxBin = proj.GetBinCenter( maxBin )
			if mpv_maxBin > 60000:
				if 'TIB' in layer:
					mpv_maxBin = 35000
				else:
					mpv_maxBin = 35000

			# Fit to get mpv
			fitResults = None
			if 'LeadingStripCharge' in plotName:
				if 'TIB' in layer:
					fitResults = proj.Fit('landau','QS','',mpv_maxBin - 8000, mpv_maxBin + 10000)
				elif 'TOB' in layer:
					fitResults = proj.Fit('landau','QS','',mpv_maxBin - 8000, mpv_maxBin + 10000)
				else :
					fitResults = proj.Fit('landau','QS','',mpv_maxBin - 8000, mpv_maxBin + 10000)

			else:
				if 'TIB' in layer:
					fitResults = proj.Fit('landau','QS','',mpv_maxBin - 8000, mpv_maxBin + 10000)
				elif 'TOB' in layer:
					fitResults = proj.Fit('landau','QS','',mpv_maxBin - 8000, mpv_maxBin + 10000)
				else :
					fitResults = proj.Fit('landau','QS','',mpv_maxBin - 8000, mpv_maxBin + 10000)

			mpv = fitResults.Parameter(1)
			if ( abs(mpv - mpv_maxBin) > 0.1 * mpv ): print ('WARNING : MPV from fit differs by more than 10% from maximum bin, check your fits')
			mpvs[label][layer] = mpv_maxBin


for counter, (label,fileName) in enumerate( fileNames.items() ):
	inputFile = r.TFile(fileName)

	if 'afterG2' in plotName and ( label == 'Data' or label == 'Default MC' ):
		projections_perFile[label] = get1DProjections( layers, inputFile, plotName.split('_afterG2')[0], pu_ranges, normFactor = 1, rebinFactor = 1 )
	else:
		projections_perFile[label] = get1DProjections( layers, inputFile, plotName, pu_ranges, normFactor = 1, rebinFactor = 1 )

	if label == 'Data': 
		for layer in projections_perFile[label]:
			for pu_range in pu_ranges:
				pu_range_label = getPURangeLabel( pu_range )
				projections_perFile[label][layer][pu_range_label].Rebin(rebinFactor)
		continue

	for layer in projections_perFile[label]:
		calibMPV = 1
		if not afterG2:
			dataMPV = mpvs['Data'][layer]
			simMPV = mpvs[label][layer]
			# calibMPV = dataMPV/simMPV
			calibMPV = 1 # uncomment to disable calibration


		for pu_range in pu_ranges:
			pu_range_label = getPURangeLabel( pu_range )
			hist_toCalib = projections_perFile[label][layer][pu_range_label]
			hist_temp = projections_perFile[label][layer][pu_range_label].Clone()
			hist_temp.Reset('ICES')
			for bin in range(1,hist_toCalib.GetNbinsX()+1):
				binContent = hist_toCalib.GetBinContent(bin)
				binCenter = hist_toCalib.GetBinCenter(bin)

				newBinCenter = binCenter * calibMPV
				newBinIndex = hist_temp.FindBin( newBinCenter )
				newBinContent = hist_temp.GetBinContent( newBinIndex ) + binContent

				hist_temp.SetBinContent( newBinIndex, newBinContent )
			hist_temp.Rebin(rebinFactor)
			projections_perFile[label][layer][pu_range_label] = hist_temp

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
	leg_projections = None
	if len( pu_ranges ) == 1 :
		leg_projections = r.TLegend(0.5, 0.5, 0.9, 0.9)
		leg_projections.SetBorderSize(0)
		leg_projections.SetFillStyle(0)
		puRangeLabel = 'PU {min} to {max}'.format( min = pu_ranges[0][0], max = pu_ranges[0][-1])
		leg_projections.SetHeader(layer + ", " + puRangeLabel,"C")
	else:
		can_projections.DivideSquare( len( pu_ranges ) + 1 )
		leg_projections = r.TLegend(0.2, 0.2, 0.8, 0.8)


	ratios = []
	for counter, pu_range in enumerate( pu_ranges ) :
		pad = can_projections.cd( counter + 1 )
		# can_projections.SetTopMargin(0.1)
		r.gPad.Divide(2)
		pad.cd(1).SetPad(0,0.4,1,1)
		pad.cd(1).SetTopMargin(1.)
		pad.cd(2).SetPad(0,0.05,1,0.4)

		pu_range_label = getPURangeLabel( pu_range )
		dataHist = dataProjections[layer][pu_range_label]
		if normToOne : dataHist.Scale( 1 / dataHist.Integral() )

		dataHist.GetYaxis().SetTitle('Fraction of clusters')
		dataHist.GetYaxis().SetTitleSize( 0.08 )
		dataHist.GetYaxis().SetTitleOffset( 0.9 )
		dataHist.GetYaxis().SetLabelSize(0.07)
		dataHist.GetXaxis().SetLabelSize(0.0)
		dataHist.GetYaxis().SetNdivisions(4,4,0)

		dataHist.SetMarkerStyle(8)
		dataHist.SetMarkerColor(1)
		dataHist.SetLineColor(1)
		if counter == 0 : leg_projections.AddEntry(dataHist,'Data (old APV settings)','P')

		drawOption = 'E'
		dataHist.SetMaximum( dataHist.GetMaximum() * 1.6 )
		p = pad.cd(1)
		p.SetBottomMargin(0.05)
		p.SetRightMargin(0.12)
		dataHist.Draw(drawOption)
		drawOption = 'HIST'

		isFirstHist = True
		firstTRatioPlot = None
		for simCounter, simLabel in enumerate( fileNames.keys() ):
			if simLabel == 'Data' : continue
			simHist = projections_perFile[simLabel][layer][pu_range_label]

			normFactor = float( nEventsInPURange['Data'][pu_range_label] ) / float( nEventsInPURange[simLabel][pu_range_label] )
			simHist.Scale( normFactor )
			if normToOne : simHist.Scale( 1 / simHist.Integral() )

			simHist.SetLineColor( niceColourList[ simCounter ] )

			p = pad.cd(2)
			p.SetBottomMargin(0.3)
			p.SetTopMargin(0.05)
			p.SetRightMargin(0.12)
			ratios.append( simHist.Clone() )
			ratios[-1].GetXaxis().SetTitle('# electrons')
			ratios[-1].GetXaxis().SetLabelSize( 0.1 )
			ratios[-1].GetXaxis().SetTitleSize( 0.1 )
			ratios[-1].GetXaxis().SetTitleOffset( 0.9 )
			ratios[-1].GetYaxis().SetTitle('Ratio to Data')
			ratios[-1].GetYaxis().SetTitleSize( 0.1 )
			ratios[-1].GetYaxis().SetTitleOffset( 0.5 )
			ratios[-1].GetYaxis().SetLabelSize( 0.1 )
			ratios[-1].Divide( dataHist )
			ratios[-1].GetYaxis().SetNdivisions(2)
			ratios[-1].Draw(drawOption)
			ratios[-1].SetMinimum(0.4)
			ratios[-1].SetMaximum(1.8)


			drawOption = 'HIST SAME'
			if counter == 0 : leg_projections.AddEntry(simHist,simLabel,'L')
			pad.cd(1)
			simHist.Draw(drawOption)
		pad.cd(1)
		dataHist.Draw('E SAME')

		# Add CMS labels	
		latex = r.TLatex(0.2, 0.8, cmsText)
		latex.SetTextFont(cmsTextFont)
		latex.SetTextAlign(11)
		latex.SetTextSize(cmsTextSize*pad.GetTopMargin())
		latex.DrawTextNDC(0.2,0.83, cmsText)
		latex.SetTextFont(extraTextFont)
		latex.SetTextAlign(11)
		latex.SetTextSize(0.76*cmsTextSize*pad.GetTopMargin())
		latex.DrawTextNDC(0.2,0.83-1.2*cmsTextSize*pad.GetTopMargin(), extraText)
		pad.Update()


		# Lumi text
		latex.SetTextAlign(31)
		latex.SetTextFont(42)
		# latex.SetTextSize(cmsTextSize*pad.GetTopMargin())
		latex.SetTextSize(0.05)
		# latex.DrawTextNDC(1-pad.GetRightMargin(),1-cmsTextSize*pad.GetTopMargin(), lumiText)
		latex.DrawLatexNDC(1-pad.GetRightMargin()-0.06,0.93, lumiText)

		pad.cd(2).SetGridy()

	if len( pu_ranges ) == 1:
		can_projections.cd( 1 )
	else:
		can_projections.cd( len( pu_ranges ) + 1 )		
	leg_projections.Draw()
	can_projections.Update()

	can_projections.Print("clusterCharge/"+layer+".pdf");
