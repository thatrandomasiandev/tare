"""Fill the 19-slide TARE deck: text at run level (formatting kept), pictures swapped in place, tables, notes."""
import copy
import sys

from pptx import Presentation

W = "/private/tmp/claude-501/-Users-joshuaterranova-Desktop-CSCI270-ACTS/b81e8eea-2190-4d0f-82c6-7f701194ea1f/scratchpad/deck"
FIG = "/Users/joshuaterranova/Desktop/CSCI270/ACTS-hub/pipeline/presentation/deck"
prs = Presentation(f"{W}/stage1.pptx")
S = list(prs.slides)


def shape(slide, sid):
    for sh in slide.shapes:
        if sh.shape_id == sid:
            return sh
    raise KeyError(sid)


def set_paras(tf, lines):
    """Set text per paragraph, keeping each paragraph's first run formatting. Adds/removes paragraphs by cloning."""
    paras = list(tf.paragraphs)
    while len(paras) < len(lines):
        new = copy.deepcopy(paras[-1]._p)
        paras[-1]._p.addnext(new)
        paras = list(tf.paragraphs)
    for extra in paras[len(lines):]:
        extra._p.getparent().remove(extra._p)
    for para, text in zip(tf.paragraphs, lines):
        runs = list(para.runs)
        if not runs:
            r = para.add_run()
            runs = [r]
        runs[0].text = text
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
        for br in para._p.findall("{http://schemas.openxmlformats.org/drawingml/2006/main}br"):
            br.getparent().remove(br)


def text(slide, sid, *lines):
    set_paras(shape(slide, sid).text_frame, list(lines))


def table(slide, sid, rows):
    tbl = shape(slide, sid).table
    trs = list(tbl._tbl.tr_lst)
    while len(trs) < len(rows):
        new = copy.deepcopy(trs[-1])
        trs[-1].addnext(new)
        trs = list(tbl._tbl.tr_lst)
    for extra in trs[len(rows):]:
        extra.getparent().remove(extra)
    for r, vals in zip(tbl.rows, rows):
        assert len(vals) == len(r.cells), (sid, vals)
        for c, v in zip(r.cells, vals):
            set_paras(c.text_frame, [v])


def picture(slide, sid, name):
    old = shape(slide, sid)
    new = slide.shapes.add_picture(f"{FIG}/{name}.png", old.left, old.top, old.width, old.height)
    new.name = f"TARE graph: {name}"
    old._element.addprevious(new._element)
    old._element.getparent().remove(old._element)


def notes(slide, body):
    slide.notes_slide.notes_text_frame.text = body


# 1 title
s = S[0]
text(s, 90, "TARE: Exact Incremental Re-annotation Across Reference Database Releases", "",
     "Reuse last release's annotations, rerun only what changed, and get output byte-identical to a full rerun, or knowingly fall back")
text(s, 91, "Joshua Terranova, University of Southern California", "Progress update, October 2026")
notes(s, "This is a progress update on TARE, a system for updating protein annotations when a reference database such as "
         "Pfam publishes a new release. The short version: on Pfam updates it is about four times faster than redoing the "
         "work, and every output line is identical to a full rerun. The rest of the talk shows how, how we know it is exact "
         "and safe, and what is still open before the OSDI deadline on December 8.")

# 2 contents
s = S[1]
for (n, t, d), ids in zip([
        ("01", "The problem", "Reference databases change every release, so annotations go stale"),
        ("02", "The method", "Pin the database size, replay only candidates, check or refuse"),
        ("03", "Exactness", "715,704 output lines across HMMER and Infernal, none different"),
        ("04", "Speed", "4.24× on Pfam updates, a cost model, and where the time goes"),
        ("05", "Safety and baselines", "A bounded audit, the DIAMOND finding, and existing tools"),
        ("06", "Status and next steps", "Generality, what is open, and the OSDI plan")],
        [(105, 106, 107), (109, 110, 111), (113, 114, 115), (117, 118, 119), (121, 122, 123), (125, 126, 127)]):
    text(s, ids[0], n); text(s, ids[1], t); text(s, ids[2], d)
notes(s, "Six parts: the problem, the method, the two main results (exactness and speed), safety and how TARE compares "
         "with existing tools, and finally where the project stands and what is next.")

# 3 hero
s = S[2]
text(s, 199, "Same answer. A quarter of the time.")
text(s, 201, "FULL RERUN · PFAM 38.2"); text(s, 202, "2,204 s"); text(s, 203, "to re-annotate one genome from scratch")
text(s, 204, "→ 30,134"); text(s, 205, "families searched for every protein")
text(s, 207, "TARE UPDATE · SAME OUTPUT"); text(s, 208, "519 s"); text(s, 209, "reusing the Pfam 38.1 results")
text(s, 210, "→ 4.24×"); text(s, 211, "faster, byte-identical output")
notes(s, "The headline in one picture. For the median genome on a dedicated server, a full rerun against Pfam 38.2 takes "
         "about 2,200 seconds. TARE produces the identical output in about 520 seconds by reusing the results from Pfam 38.1. "
         "Across nine genomes the median speedup is 4.24 times, and not one output byte differs from the full rerun.")

# 4 problem: churn
s = S[3]
text(s, 150, "THE PROBLEM · PFAM RELEASE CHURN")
text(s, 151, "Each release changes only part of the database")
table(s, 152, [["Release", "Changed", "Reused"], ["37.3 → 37.4", "2.0%", "98.0%"], ["38.0 → 38.1", "12.2%", "87.8%"],
               ["38.1 → 38.2", "13.4%", "86.6%"], ["37.4 → 38.0", "93.1%", "6.9%"]])
text(s, 153, "A full rerun searches all ~30,000 families for every protein, even when most of Pfam is unchanged. Across seven releases, the median changed share is 12.2%.")
text(s, 154, "Labs pay for the whole database at every release; NCBI and JGI both cite this cost.")
picture(s, 156, "churn")
notes(s, "Pfam publishes a new release every few months. We hashed every family in seven consecutive releases. Usually only "
         "a small share changes: 2 to 13 percent, median 12.2. One release, 37.4 to 38.0, was a full rebuild where 93 percent "
         "changed. Today labs redo everything anyway, because the annotation programs have no memory of earlier runs. NCBI "
         "and JGI both say in print that this cost limits how often they can update.")

# 5 why hard
s = S[4]
text(s, 303, "WHY REUSE IS HARD")
text(s, 304, "Every printed number depends on the whole database.")
text(s, 305, "HMMER scales each E-value by the database size, so cached results are wrong after a release, and rerunning only the changed families changes 99.9% of output lines.")
notes(s, "Why not just search the new families and keep the rest? Because HMMER's E-value is a probability times the number "
         "of families in the database. Add families and every printed number shifts. If you rerun HMMER on only the changed "
         "families, it uses the smaller size, and 99.9 percent of output lines come out different. So the problem is not "
         "finding what changed; it is getting the program to print exactly what a full run would.")

# 6 method
s = S[5]
text(s, 315, "THE METHOD")
text(s, 316, "Pin, replay only what can change, then check")
text(s, 317, "1. Hash every family in both releases; only new or edited ones can change.")
text(s, 318, "2. Search all proteins against the changed families to find new hits.")
text(s, 319, "3. Rerun each protein against only its candidates, with -Z pinned to the new size.")
text(s, 320, "4. Check: add back left-out families; if any line changes, rerun in full.")
text(s, 321, "So the program itself prints every number, exactly as a full run would.")
text(s, 323, "What this guarantees")
text(s, 324, "Byte-identical output whenever it ships", "No changes to the program (unmodified HMMER)",
     "Refuses whole-file and neighbor coupling", "Hidden coupling on ≥1% of records: ≤5% slips",
     "Falls back to a full run when too much changed")
notes(s, "TARE wraps the unmodified program. It finds changed families by hashing, searches every protein against just "
         "those to find new hits, then reruns each protein only against its candidate families with HMMER's database-size "
         "option pinned to the new release. Because the program computes and rounds every number itself, the output is "
         "byte-identical. Before shipping, a check adds back families it left out; any change means TARE refuses and runs "
         "the full program instead. Pinning itself is known from parallel BLAST; what is new is everything around it.")

# 7 exactness
s = S[6]
text(s, 267, "RESULT 1 · EXACTNESS")
text(s, 268, "Not one output line differed from a full rerun")
text(s, 269, "Eight experiments across HMMER and Infernal compared 715,704 output lines byte for byte with a full rerun. None differed.")
text(s, 270, "Without the pin, 99.9% of lines differed: the pin is what makes reuse exact.")
text(s, 271, "An error rate above 4.2 per million lines is ruled out (one-sided 95%), across 60+ HMMER genomes and 21 Infernal genomes, including archaea, eukaryotes and metagenomes.")
picture(s, 273, "exactness")
notes(s, "Every experiment compares TARE's output with a full rerun, byte for byte. Across eight experiments, 715,704 lines, "
         "zero differences. The largest set is 48 diverse genomes, including archaea, a fly proteome and metagenome-assembled "
         "genomes. The same replay without the pin changes almost every line, so the pin is the key. Statistically, a per-line "
         "error rate above about 4 in a million is ruled out.")

# 8 headline
s = S[7]
text(s, 236, "RESULT 2 · SPEED · DEDICATED SERVER, NINE GENOMES")
text(s, 237, "Pfam updates run 4.24× faster")
text(s, 238, "4.24×"); text(s, 239, "Median speedup, 95% CI 4.17–4.68, every update byte-identical")
text(s, 240, "4.37×"); text(s, 241, "Predicted in advance by a two-term cost model (within 3%)")
text(s, 242, "1.32×"); text(s, 243, "Cost of the first, cache-filling run: pays back on the first update")
picture(s, 245, "headline")
notes(s, "This is the pre-registered headline: nine fresh genomes on a dedicated AMD EPYC node, three alternating runs per "
         "side. The median speedup is 4.24 times, with a 95 percent confidence interval from 4.17 to 4.68, and every update "
         "was identical to the full rerun. A simple cost model predicted 4.37. The first run, which fills the cache, costs "
         "1.32 times a normal run, so it pays for itself on the first update. Caveat: these runs used our earlier audit; a "
         "re-timing under the new default is queued and we expect about 3.7 times.")

# 9 cost model + time
s = S[8]
text(s, 389, "RESULT 2 · WHY THE SPEEDUP IS WHAT IT IS")
text(s, 390, "Searching the changed families dominates")
picture(s, 392, "cost_model")
text(s, 393, "The model 1/(a·f + c) tracks the changed share f. Ceiling 10.2×; a full rebuild (93%) falls back to a full run.")
picture(s, 395, "time_split")
text(s, 396, "Median genome: discovery 302 s and check plus audit 115 s, of a 519 s update vs a 2,204 s rerun.")
notes(s, "Left: the cost model. Update time is roughly the changed share of the database times a full run, plus a fixed "
         "overhead of about 10 percent. That predicts 4.37 at Pfam 38.2's 13 percent change, close to the measured 4.24, and "
         "caps the speedup at about 10 times. For the 93 percent rebuild, replay cannot win, so TARE now falls back to a full "
         "run automatically. Right: in the median update, most time is the search for new hits on changed families; the "
         "safety check and audit are about a fifth.")

# 10 infernal
s = S[9]
text(s, 184, "RESULT 3 · A SECOND PROGRAM · INFERNAL (RNA FAMILIES)")
text(s, 185, "Infernal updates run about twice as fast")
text(s, 186, "2.16×")
text(s, 187, "median over ten genomes (2.07× with clan competition)")
table(s, 188, [["Version", "Speedup", "Output"], ["First version", "0.49×", "Exact"], ["No clans", "2.16×", "Exact"],
               ["With clans", "2.07×", "Exact"], ["Full rerun", "1.00×", "Reference"]])
text(s, 189, "Fix: size the safety check by work, not by record count.")
picture(s, 191, "infernal")
notes(s, "The same method works on Infernal, which annotates RNA families using Rfam. The first version was exact but slower "
         "than a full run, because a bacterial genome is one long sequence and our sampled checks ended up re-checking the "
         "whole genome. Sizing those checks by residues fixed it: 2.16 times faster, 2.07 with clan competition, all exact. "
         "These are laptop timings with three runs each, and on these inputs two of the four safety layers are skipped.")

# 11 safety
s = S[10]
text(s, 150, "SAFETY · INJECTED HIDDEN COUPLING, 800 TRIALS PER CHECK")
text(s, 151, "A sized audit turns \"usually caught\" into a bound")
table(s, 152, [["Check", "All hidden", "≥1% of records"], ["Audit off", "92.6%", "n/a"], ["Audit, ~50 records", "61.1%", "31.8%"],
               ["Bounded, 299", "34.0%", "0.8%"], ["Guarantee", "n/a", "≤ 5%"]])
text(s, 153, "Auditing 299 random records means hidden coupling that reaches at least 1% of records ships with probability at most 5%. Measured: 3 of 400.")
text(s, 154, "Cost: about 6.4% of a full run. Now the default; no clean trial was refused.")
picture(s, 156, "safety")
notes(s, "A reviewer's strongest question: what if a program has a hidden dependency TARE does not know about? We injected "
         "such dependencies into a stand-in program, 800 trials per configuration. The original check missed most of them, "
         "partly because the audit never ran on a cold cache, which we fixed. The bounded audit samples 299 records, enough "
         "that a fault touching at least 1 percent of records gets through at most 5 percent of the time. Measured: 3 of 400. "
         "Below 1 percent it can still slip through, and the paper says so.")

# 12 diamond
s = S[11]
text(s, 267, "FINDING · DIAMOND REFUSED, AND WHY")
text(s, 268, "DIAMOND's results depend on database order")
text(s, 269, "TARE refused DIAMOND. Tracing the refusal showed its first filter reads 16 bytes before each seed without stopping at the entry boundary, so a neighbor changes the result.")
text(s, 270, "Reordering Swiss-Prot five times changed 322 rows of a 210,460-row search.")
text(s, 271, "This affects every DIAMOND user, not just TARE. A bug report for the maintainers is drafted. BLAST+ is also refused, for a different reason.")
picture(s, 273, "diamond")
notes(s, "When TARE's check refused DIAMOND, we traced why. DIAMOND's first filter looks at a 16-byte window around each seed "
         "and does not stop at the boundary between database entries, so the entry stored next door affects the result. We "
         "confirmed it directly: the same search against Swiss-Prot in five random orders changed 322 rows. That is a "
         "reproducibility issue for anyone using DIAMOND. BLAST+ is refused for a different reason, its column tests run "
         "without the size setting.")

# 13 baselines
s = S[12]
text(s, 389, "COMPARISON WITH EXISTING TOOLS")
text(s, 390, "General caches reuse nothing; shortcuts are not exact")
picture(s, 392, "baselines")
text(s, 393, "Riker and INCR rerun everything after a release and cost 1.6–2.2× on the first run. TARE: 1.32×, then 4.24×.")
picture(s, 395, "approximate")
text(s, 396, "Rescaled E-values match 58% of lines; iSeqSearch 1.3%, with 133 stale hits. TARE: 100%.")
notes(s, "Left: general-purpose caches such as Riker and INCR work at the level of whole commands. A new database release "
         "changes an input file, so they rerun everything, and their tracing makes the first run slower. Right: the obvious "
         "shortcuts are not exact. Rescaling old E-values matches only 58 percent of lines, and iSeqSearch, a published "
         "incremental search tool, matched 1.3 percent and reported hits to sequences the new release had deleted.")

# 14 generality
s = S[13]
text(s, 389, "GENERALITY")
text(s, 390, "Diverse genomes, and a program from another lab")
picture(s, 392, "diverse")
text(s, 393, "48 of 53 diverse genomes shipped exact, none wrong. The 5 refusals had two parser causes, now fixed.")
picture(s, 395, "prosite")
text(s, 396, "PROSITE pfscanV3 (SIB): 26 of 30 genomes exact, 0 wrong. Both draws fell just short of power.")
notes(s, "Two kinds of generality. Left: 53 genomes across archaea, bacteria, eukaryotes and metagenomes; 48 shipped exact "
         "and none was wrong. Five were refused even though they would have been exact, from two parser rules; after fixing "
         "them, all six affected genomes ship. Right: a program from a different research group, SIB's PROSITE scanner. "
         "26 of 30 genomes were exact with zero wrong; both draws fell just short of their power floors, so we present this "
         "as supporting evidence.")

# 15 payback
s = S[14]
text(s, 221, "ONE-TIME COST · FILLING THE CACHE")
text(s, 222, "HMMER pays back on the first update")
table(s, 223, [["Measure", "HMMER", "Infernal", "Unit"], ["First run", "1.32×", "4.45×", "× full run"],
               ["Update speedup", "4.24×", "2.16×", "median"], ["Pays back after", "0.3", "6.4", "updates"],
               ["Changed share", "13.4%", "10.8%", "of release"], ["Genomes timed", "9", "10", "fresh draw"],
               ["Machine", "Server", "Laptop", "timing"], ["Safety layers", "4 of 4", "2 of 4", "active"]])
picture(s, 225, "payback")
text(s, 226, "Infernal's fill runs whole-genome probes; cutting it is open work.")
notes(s, "TARE's first run fills the cache and runs some one-time probes. For HMMER that costs 1.32 times a normal run, so "
         "it pays for itself on the first update. For Infernal it is 4.45 times, so it needs about six updates to pay back, "
         "because the probes run on whole genomes. Reducing that is listed as open work.")

# 16 process
s = S[15]
text(s, 352, "PROCESS")
text(s, 353, "Built so a reviewer has nothing to grab")
text(s, 355, "Pre-registration chain")
text(s, 356, "Every design and pass rule committed before the run. Deviations go in dated addenda, never edits.")
text(s, 358, "A checker for every number")
text(s, 359, "Each number in the paper names its result file; a script checks all of them at printed precision.")
text(s, 361, "Controls that must fail")
text(s, 362, "Each test has a known-bad case that must refuse: DIAMOND, injected drops, unpinned replay.")
text(s, 364, "Two mock OSDI reviews")
text(s, 365, "They drove a second round: the bounded audit, the fallback, server timing, and baselines.")
notes(s, "How the work is kept honest. Every experiment's design and pass rule is committed before it runs, and any change "
         "is recorded as a dated addendum. Every number in the paper carries a comment naming the file it comes from, and a "
         "script checks them all. Every test includes a case that must fail. And two mock OSDI reviews drove the second round "
         "of experiments.")

# 17 ledger
s = S[16]
text(s, 493, "LEDGER")
text(s, 494, "What is solid, and what is still open")
text(s, 497, "Solid")
text(s, 498, "Exact output: 715,704 lines, 0 different", "4.24× on Pfam, model within 3%", "Infernal 2.16×, exact",
     "A stated safety bound, measured", "DIAMOND order dependence")
text(s, 501, "Open or unproven")
text(s, 502, "Re-timing under the bounded audit", "A timed multi-release chain", "A powered unrelated-program draw",
     "BLAST+ (probes run unpinned)", "A cheaper Infernal cache fill")
notes(s, "A ledger of where things stand. Solid: exactness, the HMMER speedup and its model, Infernal, the safety bound, and "
         "the DIAMOND finding. Open: the headline re-timing under the stronger audit, the timed chain across several releases, "
         "a properly powered draw for the unrelated program, BLAST+, and Infernal's cache-fill cost.")

# 18 status
s = S[17]
text(s, 512, "CARC STATUS · OCTOBER 21")
text(s, 513, "What is running on the cluster")
table(s, 514, [["Workstream", "What it measures", "Status"], ["Headline re-time", "9 genomes, bounded audit", "Queued; pilot est. tonight"],
               ["Release chain", "37.3 → 38.2, 3 genomes", "Queued; est. tomorrow"], ["Expert script", "TARE vs a hand-written script", "Pilot done; measured queued"],
               ["Table 4 on x86", "Riker, INCR, ProcessCache", "Pilot done; measured queued"], ["iSeqSearch timing", "speed next to its 1.3%", "Needs a script fix"],
               ["PROSITE draw 2", "20 fresh genomes", "Done: 18 of 20 exact"]])
text(s, 515, "Queue: our account's fair-share score is low, and exclusive EPYC nodes are scarce.")
text(s, 516, "Ask: may we run the queued jobs on the second allocation (biyik_1173)?")
notes(s, "Everything left is queued on CARC and chained, so it runs without supervision. The holdup is the queue: our "
         "account has used a lot of time recently, so its priority is low, and our timing jobs need whole dedicated nodes. "
         "There is a second allocation on my login with almost no usage; using it would start these jobs within hours. "
         "That is a question for you.")

# 19 next steps
s = S[18]
text(s, 761, "NEXT TWO WEEKS")
text(s, 762, "Next steps and asks")
text(s, 763, "Next")
text(s, 764, "Fold in the re-timed headline", "Measured release chain and baselines", "Fix the iSeqSearch timing script",
     "Trim the paper to OSDI's 12 pages", "Outside read, then arXiv")
text(s, 765, "Asks")
text(s, 766, "Feedback on the safety framing", "Use of the second CARC allocation", "OSDI (Dec 8) or ATC as the venue",
     "One outside reader for the draft")
notes(s, "Next two weeks: fold in the remaining CARC results, trim the paper to OSDI's page limit, get an outside read, and "
         "post to arXiv. Asks: feedback on how the safety guarantee is framed, permission to use the second allocation, "
         "advice on OSDI versus ATC, and a suggestion for an outside reader.")

prs.save(f"{W}/TARE-progress.pptx")
print("saved")
