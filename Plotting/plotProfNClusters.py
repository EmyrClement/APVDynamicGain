import ROOT as r
from plotStyle import *
from tools import *
from collections import OrderedDict
r.gROOT.SetBatch(1)
SetPlotStyle()
r.TH1F.AddDirectory(0)
r.gROOT.ProcessLine("gErrorIgnoreLevel = 9999;")
import os
if not os.path.exists('clusterProfiles'):
    os.makedirs('clusterProfiles')

cmsText     = "CMS";
cmsTextFont   = 61  
cmsTextSize      = 0.75
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

plotName = 'demo/nClusters_Vs_TruePU'

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


normToOne = False
rebinFactor = 1 # Tweaked later on for TIB/TOB

dirName = plotName.split('/')[-1]
profiles_y = {}

profiles_perFile = {}
profiles_inclusvePU_perFile = {}

for counter, (label,fileName) in enumerate( fileNames.items() ):
	inputFile = r.TFile(fileName)
	profiles_perFile[label] = get1DProfiles( layers, inputFile, plotName, normFactor = 1, rebinFactor = 3 )

dataProfiles = profiles_perFile['Data']

puLabels = []

for layer in layers:
	can_profiles = r.TCanvas('can_proj_{label}'.format(label=dirName),'can_proj_{label}'.format(label=dirName),1200,900)
	can_profiles.SetTopMargin(0.1)
	can_profiles.SetFillColor(0)
	can_profiles.SetBorderMode(0)
	can_profiles.SetFrameFillStyle(0)
	can_profiles.SetFrameBorderMode(0)
	leg_profiles = r.TLegend(0.35, 0.52, 0.63, 0.88)
	leg_profiles.SetHeader("Layer : "+layer,"C")
	leg_profiles.SetBorderSize(0)
	leg_profiles.SetFillStyle(0)

	ratios = []
	pad = can_profiles.cd( 1 )
	r.gPad.Divide(2)
	pad.cd(1).SetPad(0,0.4,1,1)
	pad.cd(1).SetTopMargin(1.5)
	pad.cd(2).SetPad(0,0.05,1,0.4)
	dataHist = dataProfiles[layer]
	leg_profiles.AddEntry(dataHist,'Data (old APV settings)','PL')


	if normToOne : dataHist.Scale( 1 / dataHist.Integral() )
	dataHist.GetYaxis().SetTitle('Mean # clusters')
	dataHist.GetYaxis().SetTitleSize( 0.1 )
	dataHist.GetYaxis().SetTitleOffset( 0.6 )
	dataHist.GetYaxis().SetLabelSize(0.08)
	dataHist.GetXaxis().SetLabelSize(0.0)
	dataHist.GetYaxis().SetNdivisions(403)
	dataHist.SetMaximum( dataHist.GetMaximum()*1.8 )
	dataHist.GetXaxis().SetRangeUser( 0, 45 )

	dataHist.SetMarkerStyle(8)
	dataHist.SetMarkerColor(1)
	dataHist.SetLineColor(1)
	dataHist.SetLineWidth(3)
	if counter == 0 : leg_profiles.AddEntry(dataHist,'Data','P')

	drawOption = 'E'
	dataHist.SetMaximum( dataHist.GetMaximum() * 1.5 )
	p = pad.cd(1)
	p.SetBottomMargin(0.05)
	dataHist.Draw(drawOption)
	drawOption = 'HIST ]['

	isFirstHist = True
	firstTRatioPlot = None
	for simCounter, simLabel in enumerate( fileNames.keys() ):
		if simLabel == 'Data' : continue
		simHist = profiles_perFile[simLabel][layer]

		simHist.Rebin( rebinFactor )

		if normToOne : simHist.Scale( 1 / simHist.Integral() )
		simHist.SetLineColor( niceColourList[ simCounter ] )
		simHist.SetLineWidth(3)

		p = pad.cd(2)
		p.SetBottomMargin(0.3)
		p.SetTopMargin(0.05)

		ratios.append( simHist.Clone() )
		ratios[-1].GetXaxis().SetTitle('# Vertices')
		ratios[-1].GetXaxis().SetLabelSize( 0.14 )
		ratios[-1].GetXaxis().SetTitleSize( 0.15 )
		ratios[-1].GetXaxis().SetTitleOffset( 0.8 )
		ratios[-1].GetYaxis().SetTitle('Ratio to Data')
		ratios[-1].GetYaxis().SetTitleSize( 0.15 )
		ratios[-1].GetYaxis().SetTitleOffset( 0.35 )
		ratios[-1].Divide( dataHist )
		ratios[-1].GetYaxis().SetNdivisions(2,3,0)
		ratios[-1].Draw(drawOption)
		ratios[-1].GetYaxis().SetLabelSize(0.15)
		ratios[-1].GetXaxis().SetRangeUser(0,45)
		ratios[-1].SetMinimum(0.5)
		ratios[-1].SetMaximum(1.5)


		drawOption = 'HIST SAME ]['
		leg_profiles.AddEntry(simHist,simLabel,'L')
		pad.cd(1)
		simHist.Draw(drawOption)
	pad.cd(1)
	dataHist.Draw('E SAME')



	# Add CMS labels	
	latex = r.TLatex(0.2, 0.8, cmsText)
	latex.SetTextFont(cmsTextFont)
	latex.SetTextAlign(11)
	latex.SetTextSize(0.76*cmsTextSize*pad.GetTopMargin())
	latex.DrawTextNDC(0.2,0.8, cmsText)
	latex.SetTextFont(extraTextFont)
	latex.SetTextAlign(11)
	latex.SetTextSize(0.76*cmsTextSize*pad.GetTopMargin())
	latex.DrawTextNDC(0.2,0.8-1.2*cmsTextSize*pad.GetTopMargin(), extraText)
	# pad.Update()

	# Lumi text
	latex.SetTextAlign(31)
	latex.SetTextFont(42)
	# latex.SetTextSize(cmsTextSize*pad.GetTopMargin())
	latex.SetTextSize(0.07)
	# latex.DrawTextNDC(1-pad.GetRightMargin(),1-cmsTextSize*pad.GetTopMargin(), lumiText)
	latex.DrawLatexNDC(1-pad.GetRightMargin(),0.92, lumiText)
	pad.cd(2).SetGridy()

	can_profiles.cd( 1 )
	leg_profiles.Draw()
	can_profiles.Update()
	# input('...')
	can_profiles.Print("clusterProfiles/"+layer+".pdf");
	can_profiles.Print("clusterProfiles/"+layer+".png");
