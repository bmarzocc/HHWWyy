import ROOT
import argparse

if __name__ == '__main__':

 ROOT.gROOT.SetBatch(ROOT.kTRUE)

 parser =  argparse.ArgumentParser(description='split_Tree')
 parser.add_argument('-i', '--input', dest='input', required=True, type=str)
 parser.add_argument('-d', '--dir', dest='dir', required=False, type=str) 
 args = parser.parse_args()

 #dir = "tagsDumper/trees" 
 #dir = ""
 #if args.dir!="": dir = args.dir
 #dir = ""
 dir = ""

 output_name = args.input
 output_nameEven = output_name.replace('.root','_even.root')
 output_nameOdd = output_name.replace('.root','_odd.root')
 outfile_even = ROOT.TFile(output_nameEven, "RECREATE")
 outfile_odd = ROOT.TFile(output_nameOdd, "RECREATE")
 inFile = ROOT.TFile(args.input,"READ")

 print "Running on even events..."
 if dir!="":
   dir1 = inFile.Get("tagsDumper") 
   dir2 = dir1.Get("trees") 
   print dir2.GetName()
   for key in dir2.GetListOfKeys():
    print "Even events:",key.GetName()
    tree = inFile.Get(dir+"/"+key.GetName())
    outfile_even.cd()
    outtree_even = tree.CloneTree(0)
    nentries = tree.GetEntries()
    for i in range(0, nentries):
       tree.GetEntry(i) 
       if i%2 == 0: outtree_even.Fill() 
    outtree_even.Write(key.GetName())
   outfile_even.Close()
   for key in dir2.GetListOfKeys():
    print "Odd events:",key.GetName()
    tree = inFile.Get(dir+"/"+key.GetName())
    outfile_odd.cd()
    outtree_odd = tree.CloneTree(0)
    nentries = tree.GetEntries()
    for i in range(0, nentries):
       tree.GetEntry(i) 
       if i%2 != 0: outtree_odd.Fill() 
    outtree_odd.Write(key.GetName())
   outfile_odd.Close()
 else:
   for key in inFile.GetListOfKeys():
    #if key.GetName()!="GluGluToHHTo2G2Qlnu_node_10_13TeV_HHWWggTag_0_v1": continue
    print "Even events:",key.GetName()
    tree = inFile.Get(key.GetName())
    outfile_even.cd()
    outtree_even = tree.CloneTree(0)
    nentries = tree.GetEntries()
    for i in range(0, nentries):
       tree.GetEntry(i) 
       if i%2 == 0: outtree_even.Fill() 
    outtree_even.Write(key.GetName())
   outfile_even.Close()
   for key in inFile.GetListOfKeys():
    #if key.GetName()!="GluGluToHHTo2G2Qlnu_node_10_13TeV_HHWWggTag_0_v1": continue
    print "Odd events:",key.GetName()
    tree = inFile.Get(key.GetName())
    outfile_odd.cd()
    outtree_odd = tree.CloneTree(0)
    nentries = tree.GetEntries()
    for i in range(0, nentries):
       tree.GetEntry(i) 
       if i%2 != 0: outtree_odd.Fill() 
    outtree_odd.Write(key.GetName())
   outfile_odd.Close()

