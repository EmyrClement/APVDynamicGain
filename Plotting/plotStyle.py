import ROOT as r
def SetPlotStyle():
  # from ATLAS plot style macro
  # use plain black on white colors
  r.gStyle.SetFrameBorderMode(0)
  r.gStyle.SetFrameFillColor(0)
  r.gStyle.SetCanvasBorderMode(0)
  r.gStyle.SetCanvasColor(0)
  r.gStyle.SetPadBorderMode(0)
  r.gStyle.SetPadColor(0)
  r.gStyle.SetStatColor(0)
  r.gStyle.SetHistLineColor(1)

  r.gStyle.SetPalette(1)

  # set the paper & margin sizes
  r.gStyle.SetPaperSize(20,26)
  r.gStyle.SetPadTopMargin(0.05)
  r.gStyle.SetPadRightMargin(0.05)
  r.gStyle.SetPadBottomMargin(0.16)
  r.gStyle.SetPadLeftMargin(0.16)

  # set title offsets (for axis label)
  r.gStyle.SetTitleXOffset(1.4)
  r.gStyle.SetTitleYOffset(1.4)

  # use large fonts
  r.gStyle.SetTextFont(42)
  r.gStyle.SetTextSize(0.05)
  r.gStyle.SetLabelFont(42,"x")
  r.gStyle.SetTitleFont(42,"x")
  r.gStyle.SetLabelFont(42,"y")
  r.gStyle.SetTitleFont(42,"y")
  r.gStyle.SetLabelFont(42,"z")
  r.gStyle.SetTitleFont(42,"z")
  r.gStyle.SetLabelSize(0.05,"x")
  r.gStyle.SetTitleSize(0.05,"x")
  r.gStyle.SetLabelSize(0.05,"y")
  r.gStyle.SetTitleSize(0.05,"y")
  r.gStyle.SetLabelSize(0.05,"z")
  r.gStyle.SetTitleSize(0.05,"z")

  # use bold lines and markers
  r.gStyle.SetMarkerStyle(20)
  r.gStyle.SetMarkerSize(1.2)
  r.gStyle.SetHistLineWidth(2)
  r.gStyle.SetLineStyleString(2,"[12 12]")

  # get rid of error bar caps
  r.gStyle.SetEndErrorSize(0.)

  # do not display any of the standard histogram decorations
  r.gStyle.SetOptTitle(0)
  r.gStyle.SetOptStat(0)
  r.gStyle.SetOptFit(0)

  # put tick marks on top and RHS of plots
  r.gStyle.SetPadTickX(1)
  r.gStyle.SetPadTickY(1)



# CMS_lumi
#   Initiated by: Gautier Hamel de Monchenault (Saclay)
#   Translated in Python by: Joshua Hardenbrook (Princeton)
#   Updated by:   Dinko Ferencek (Rutgers)
#

cmsText     = "CMS";
cmsTextFont   = 61  

writeExtraText = True
extraText   = "Preliminary"
extraTextFont = 52 

lumiTextSize     = 0.6
lumiTextOffset   = 0.2

cmsTextSize      = 0.75
cmsTextOffset    = 0.1

relPosX    = 0.045
relPosY    = 0.035
relExtraDY = 1.2

extraOverCmsTextSize  = 0.76

lumi_13TeV = "20.1 fb^{-1}"
lumi_8TeV  = "19.7 fb^{-1}" 
lumi_7TeV  = "5.1 fb^{-1}"
lumi_sqrtS = ""

drawLogo      = False

# def CMS_lumi(pad,  iPeriod,  iPosX ):
#     outOfFrame    = False
#     if(iPosX/10==0 ): outOfFrame = True

#     alignY_=3
#     alignX_=2
#     if( iPosX/10==0 ): alignX_=1
#     if( iPosX==0    ): alignY_=1
#     if( iPosX/10==1 ): alignX_=1
#     if( iPosX/10==2 ): alignX_=2
#     if( iPosX/10==3 ): alignX_=3
#     align_ = 10*alignX_ + alignY_

#     H = pad.GetWh()
#     W = pad.GetWw()
#     l = pad.GetLeftMargin()
#     t = pad.GetTopMargin()
#     right = pad.GetRightMargin()
#     b = pad.GetBottomMargin()
#     e = 0.025

#     pad.cd()

#     lumiText = ""
#     if( iPeriod==1 ):
#         lumiText += lumi_7TeV
#         lumiText += " (7 TeV)"
#     elif ( iPeriod==2 ):
#         lumiText += lumi_8TeV
#         lumiText += " (8 TeV)"

#     elif( iPeriod==3 ):      
#         lumiText = lumi_8TeV 
#         lumiText += " (8 TeV)"
#         lumiText += " + "
#         lumiText += lumi_7TeV
#         lumiText += " (7 TeV)"
#     elif ( iPeriod==4 ):
#         lumiText += lumi_13TeV
#         lumiText += " (13 TeV)"
#     elif ( iPeriod==7 ):
#         if( outOfFrame ):lumiText += "#scale[0.85]{"
#         lumiText += lumi_13TeV 
#         lumiText += " (13 TeV)"
#         lumiText += " + "
#         lumiText += lumi_8TeV 
#         lumiText += " (8 TeV)"
#         lumiText += " + "
#         lumiText += lumi_7TeV
#         lumiText += " (7 TeV)"
#         if( outOfFrame): lumiText += "}"
#     elif ( iPeriod==12 ):
#         lumiText += "8 TeV"
#     elif ( iPeriod==0 ):
#         lumiText += lumi_sqrtS
            
#     print (lumiText)

#     latex = r.TLatex()
#     latex.SetNDC()
#     latex.SetTextAngle(0)
#     latex.SetTextColor(r.kBlack)    
    
#     extraTextSize = extraOverCmsTextSize*cmsTextSize
    
#     latex.SetTextFont(42)
#     latex.SetTextAlign(31) 
#     latex.SetTextSize(lumiTextSize*t)    

#     latex.DrawLatex(1-right,1-t+lumiTextOffset*t,lumiText)

#     if( outOfFrame ):
#         latex.SetTextFont(cmsTextFont)
#         latex.SetTextAlign(11) 
#         latex.SetTextSize(cmsTextSize*t)    
#         latex.DrawLatex(l,1-t+lumiTextOffset*t,cmsText)
  
#     pad.cd()

#     posX_ = 0
#     if( iPosX%10<=1 ):
#         posX_ =   l + relPosX*(1-l-right)
#     elif( iPosX%10==2 ):
#         posX_ =  l + 0.5*(1-l-r)
#     elif( iPosX%10==3 ):
#         posX_ =  1-r - relPosX*(1-l-right)

#     posY_ = 1-t - relPosY*(1-t-b)

#     if( not outOfFrame ):
#         if( drawLogo ):
#             posX_ =   l + 0.045*(1-l-right)*W/H
#             posY_ = 1-t - 0.045*(1-t-b)
#             xl_0 = posX_
#             yl_0 = posY_ - 0.15
#             xl_1 = posX_ + 0.15*H/W
#             yl_1 = posY_
#             CMS_logo = r.TASImage("CMS-BW-label.png")
#             pad_logo =  r.TPad("logo","logo", xl_0, yl_0, xl_1, yl_1 )
#             pad_logo.Draw()
#             pad_logo.cd()
#             CMS_logo.Draw("X")
#             pad_logo.Modified()
#             pad.cd()          
#         else:
#             latex.SetTextFont(cmsTextFont)
#             latex.SetTextSize(cmsTextSize*t)
#             latex.SetTextAlign(align_)
#             latex.DrawLatex(posX_, posY_, cmsText)
#             if( writeExtraText ) :
#                 latex.SetTextFont(extraTextFont)
#                 latex.SetTextAlign(align_)
#                 latex.SetTextSize(extraTextSize*t)
#                 latex.DrawLatex(posX_, posY_- relExtraDY*cmsTextSize*t, extraText)
#     elif( writeExtraText ):
#         if( iPosX==0):
#             posX_ =   l +  relPosX*(1-l-right)
#             posY_ =   1-t+lumiTextOffset*t

#         latex.SetTextFont(extraTextFont)
#         latex.SetTextSize(extraTextSize*t)
#         latex.SetTextAlign(align_)
#         latex.DrawLatex(posX_, posY_, extraText)      

#     pad.Update()