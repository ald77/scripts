#! /usr/bin/env python

import ROOT
import optparse

def SkimFiles(files, options):
    out_file = ROOT.TFile(options.dest, "recreate")
    out_file.cd()
    in_chain = ROOT.TChain(options.tree, options.tree)
    for file_name in files:
        in_chain.Add(file_name)

    if options.overlaps:
        out_tree = in_chain.CopyTree(options.cut)
        out_tree.Write()
    else:
        num_entries = in_chain.GetEntries()

        out_tree = in_chain.CloneTree(0)
        in_chain.CopyAddresses(out_tree)

        ttf = ROOT.TTreeFormula("", options.cut, in_chain);
        ttf.GetNdata()
        run_dict = dict()
        ievent = 0;
        for event in in_chain:
            ievent += 1
            if ievent % 1000 == 0:
                print "Event %d of %d (%.2f%% complete)." % (ievent, num_entries, 100.*ievent/num_entries)
            ttf.UpdateFormulaLeaves()
            cut_val = ttf.EvalInstance()
            if not cut_val: continue

            repeat = False
            lumi_dict = run_dict.get(in_chain.run)
            if lumi_dict:
                event_list = lumi_dict.get(in_chain.lumiblock)
                if event_list:
                    if type(event_list) is list:
                        if in_chain.event in event_list:
                            repeat = True
                        lumi_dict[in_chain.lumiblock].extend([in_chain.event])
                    else:
                        if in_chain.event == event_list:
                            repeat = True
                        lumi_dict[in_chain.lumiblock] = [event_list, in_chain.event]
                else:
                    lumi_dict[in_chain.lumiblock] = [in_chain.event]
            else:
                run_dict[in_chain.run] = {in_chain.lumiblock : in_chain.event}

            if repeat:
                print "Skipping repeat event:", in_chain.run, in_chain.lumiblock, in_chain.event
                continue

            out_tree.Fill()
        out_tree.Write()
    out_file.Close()
    print "Wrote TTree \""+options.tree+"\" to "+options.dest

if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-d", "--dest", default="skim.root", help="Output file path")
    parser.add_option("-c", "--cut", default="", help="Skim cut")
    parser.add_option("-t", "--tree", default="tree", help="TTree name")
    parser.add_option("-o", "--overlaps", action="store_false", help="Allow events with same run,lumi,event")

    (options, files) = parser.parse_args()
    SkimFiles(files, options)
