from BaseControlPlots import BaseControlPlots

# Requirements:
# event.muons
# event.electrons

class VBFHControlPlots(BaseControlPlots):
    """A class to create control plots for VBFH"""

    def __init__(self, dir=None, dataset=None, mode="plots"):
      # create output file if needed. If no file is given, it means it is delegated
      BaseControlPlots.__init__(self, dir=dir, purpose="VBFH", dataset=dataset, mode=mode)

    def beginJob(self):
      # declare histograms
      self.add("NGenGluons", "GenGluon multiplicity", 10, 0, 10)
      self.add("NGenJets", "GenJet multiplicity", 10, 0, 10)
      self.add("GenDEtaQuarks", "#Delta#eta (q,q)", 100, 0, 10)
      self.add("GenDEtaVBF", "#Delta#eta (VBF)", 100, 0, 10)
      self.add("GenGluonEta", "gluon #eta", 100, -6, 6)
      self.add("GenGluonPhi", "gluon #phi", 63, -3.15, 3.15)
      self.add("GenGluonPt", "gluon p_{T}", 100, 0, 500)
      self.add("GenHiggsEta", "higgs #eta", 100, -6, 6)
      self.add("GenHiggsPhi", "higgs #phi", 63, -3.15, 3.15)
      self.add("GenHiggsPt", "higgs p_{T}", 100, 0, 500)
      self.add("GenMjjQuarks", "m_{jj} quark", 100, 0, 4000)
      self.add("GenMjjVBF", "m_{jj} VBF", 100, 0, 4000)
      self.add("GenQuark0Eta", "quark0 #eta", 100, -6, 6)
      self.add("GenQuark0Phi", "quark0 #phi", 63, -3.15, 3.15)
      self.add("GenQuark0Pt", "quark0 p_{T}", 100, 0, 500)
      self.add("GenQuark1Eta", "quark1 #eta", 100, -6, 6)
      self.add("GenQuark1Phi", "quark1 #phi", 63, -3.15, 3.15)
      self.add("GenQuark1Pt", "quark1 p_{T}", 100, 0, 500)
      self.add("GenVBF0Eta", "VBF0 #eta", 100, -6, 6)
      self.add("GenVBF0Phi", "VBF0 #phi", 63, -3.15, 3.15)
      self.add("GenVBF0Pt", "VBF0 p_{T}", 100, 0, 500)
      self.add("GenVBF1Eta", "VBF1 #eta", 100, -6, 6)
      self.add("GenVBF1Phi", "VBF1 #phi", 63, -3.15, 3.15)
      self.add("GenVBF1Pt", "VBF1 p_{T}", 100, 0, 500)
 

    def process(self, event):
      #get information
      result = { }

      partons = []
      quarks = []
      gluons = []
      higgs = None
      for gp in event.genparticles:
#        print "gp.PID= ", gp.PID, "gp.Status= ", gp.Status, "gp.PT= ", gp.PT
        if gp.Status != 1:
            continue
        if gp.PID == 25:
          higgs = gp
        elif abs(gp.PID) == 21 or abs(gp.PID) <= 6:
          if abs(gp.PID) == 21:
            gluons.append(gp)
          elif abs(gp.PID) <= 6:
            quarks.append(gp)
          partons.append(gp)
        else:
          "WARNING: stable particle (status 1) not accounted for: PID= ", gp.PID
    # Now sort the quarks to take the max pt pair, which will be 'quarks'
      quarks = sorted(quarks, key=lambda p: p.PT, reverse=True)
    # Keep the gluon if there is any
      gluons = sorted(gluons, key=lambda p: p.PT, reverse=True)
    # sort the partons by pt and tag the vbf pair
      partons = sorted(partons, key=lambda p: p.PT, reverse=True)
    # now output everything 
      result["NGenGluons"] = len(gluons)
      result["NGenJets"] = len(partons)
      result["GenDEtaQuarks"] = abs(quarks[0].Eta - quarks[1].Eta)
      result["GenDEtaVBF"] = abs(partons[0].Eta - partons[1].Eta)
      result["GenMjjQuarks"] = (quarks[0].P4() + quarks[1].P4()).M()
      result["GenMjjVBF"] = (partons[0].P4() + partons[1].P4()).M()
      try:
        result["GenGluonEta"] = gluons[0].Eta
        result["GenGluonPhi"] = gluons[0].Phi
        result["GenGluonPt"] = gluons[0].PT
      except IndexError: # aka: no final state gluon, must fill the (flat) tree with something still
        result["GenGluonEta"] = -1001.
        result["GenGluonPhi"] = -1001.
        result["GenGluonPt"] = -1001.
      result["GenHiggsEta"] = higgs.Eta
      result["GenHiggsPhi"] = higgs.Phi
      result["GenHiggsPt"] = higgs.PT
      result["GenQuark0Eta"] = quarks[0].Eta
      result["GenQuark0Phi"] = quarks[0].Phi
      result["GenQuark0Pt"] = quarks[0].PT
      result["GenQuark1Eta"] = quarks[1].Eta
      result["GenQuark1Phi"] = quarks[1].Phi
      result["GenQuark1Pt"] = quarks[1].PT
      result["GenVBF0Eta"] = partons[0].Eta
      result["GenVBF0Phi"] = partons[0].Phi
      result["GenVBF0Pt"] = partons[0].PT
      result["GenVBF1Eta"] = partons[1].Eta
      result["GenVBF1Phi"] = partons[1].Phi
      result["GenVBF1Pt"] = partons[1].PT

        
        
#        if event.event() % 300 == 0:

      return result

if __name__=="__main__":
  import sys
  from DelphesAnalysis.BaseControlPlots import runTest
  runTest(sys.argv[1], LeptonControlPlots())

