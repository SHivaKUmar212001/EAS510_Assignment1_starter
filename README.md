# EAS 510 - Assignment 1: Digital Forensics Apprentice

A rule-based expert system that matches modified images back to their originals.

This is the **starter repository** for Project 1. Two repositories matter:

| Repository | Role |
|------------|------|
| `delveccj/EAS510_Assignment1_starter` (this repo) | Your **code** lives here. You will fork it, work in your fork, and push your final submission here. |
| `delveccj/EAS510_Assignment1` | The **dataset** (read-only). Clone it for the images; never commit it to your fork. |

## Setup on your Codio box

```bash
# 1. Fork this repo on GitHub, then in your box:
git clone https://github.com/YOUR-USERNAME/EAS510_Assignment1_starter.git
cd EAS510_Assignment1_starter

# 2. Clone the read-only dataset as a sibling folder (images live there):
cd ~/workspace
git clone https://github.com/delveccj/EAS510_Assignment1.git

# 3. Install dependencies:
cd ~/workspace/EAS510_Assignment1_starter
python3 -m pip install -r requirements.txt

# 4. Point this box at YOUR fork (run once):
./setup_git.sh
```

## Repository layout

```
forensics_detective.py   SimpleDetector: register targets + find_best_match
rules.py                 Rule functions (Rule 1: Metadata, Rule 2: Histogram, Rule 3: Template)
test_system.py           Runs the detector over the data folders and writes results_*.txt
scripts/check_output_format.py   Validates a results file against the required format
setup_git.sh, submit.sh  One-time setup + commit/push helper ("backup button")
```

## The task in one paragraph

Implement three interpretable rules (metadata, color histogram, template matching)
that combine into a 0-100 confidence score. Run your system on `modified_images/`
and `random/` and save the full output as `results_v1.txt`. In Phase 2, run on
`hard/`, diagnose a systematic failure, add a **Rule 4**, and save
`results_v1_hard.txt` and `results_v2.txt`. Full instructions are in the Codio guide
and in the assignment PDF in UBLearns.

## Running

```bash
# Phase 1 (easy + random) -> results_v1.txt
python3 test_system.py --modified --random --output results_v1.txt

# Phase 1 on hard cases -> results_v1_hard.txt
python3 test_system.py --hard --output results_v1_hard.txt

# Phase 2 (everything) -> results_v2.txt
python3 test_system.py --modified --hard --random --output results_v2.txt

# Validate any results file against the required format:
python3 scripts/check_output_format.py results_v1.txt
```

The data folders are resolved from a sibling clone of `EAS510_Assignment1`.
If your data is elsewhere, pass `--data-dir /path/to/EAS510_Assignment1`.

## Output format (do not alter)

```
Processing: modified_image_01.jpg
Rule 1 (Metadata): FIRED - Size ratio 0.85 -> 20/30 points
Rule 2 (Histogram): FIRED - Correlation 0.92 -> 25/30 points
Rule 3 (Template): FIRED - Match score 0.76 -> 30/40 points
Final Score: 75/100 -> MATCH to original_03.jpg
```

## Backup doctrine

Your Codio box can be reset at any time. **Your fork on GitHub is the only safe
copy.** After every milestone run `./submit.sh "describe what you did"`. A box
restart never touches GitHub.

## License

Apache 2.0. See `LICENSE`.

# Reflection


## Observed weakness in V1: what failed and why
- V1 scored good on the modified and random images. It scored 48/60 after I changed the metric calculation.
- What my thought was that in what way can I tweak the features or triggers so that I can get a 60% match? 
- I tried to change those metric weights which was giving equal weightage to size ratio and area kept and I kept trying to change those weights like for size ratio as it is not that good to determine if images are related in any way or form, 
- I gave it a low weightage like 0.2 and for area kept I gave 0.8, but after I tried various such weights (like 0.3,0.7; 0.4, 0.6; 0.25, 0.75, etc)
- I realized its never gonna work like this, so I tried to make a new feature, like using size ratio and area kept, so I just find there similarity ratio which was just the ratio of min(size_ratio, area_kept) and max(size_ratio, area_kept) and it worked, I was like very happy that a shot in the dark worked just
  like this. 
- So another thing I did that there were threshold values which were present for all the rules, I was tweaking them too like for the correlation histogram, I increased the threshold to 0.8 and for the template as well I increased it to 0.8 and i tried other values before like decreasing to 0.4 and increasing to 0.9 
- But with all the trials, I found this sweet spot of 0.8 and voila!, when i changed that the metric calc, all came into place and I got an 80% match result with all randoms getting dropped with 0 pts.
- But, When in Hard cases, the V1 failed with getting only 6 matches out of 60 and I went through its result doc and found that mostly the correlation histogram rule is giving out points and other rules failing to give out scores and hence the non matches.

## Design decision for V2: what Rule 4 is and why you chose it
- I made the decision to chose SIFT just because it sounded nice in the ideas it was listed, I read about this thing and found that this just finds distinct spots near it and matches.
- So, I thought if I could find the spots of the images and used KNN to like figure out which spots are nearer in the input image to that of the original and if I find any kind of correlation, I can achieve this.
- So, that's what i did next, I used sift to find those spots, put the KNN algorithm to find the nearest neighbors and put them in an array. 
- I measured the distances of those spots and made an array of how many spots are matching with the original and based of that I put up a score. 
- One more thing I did was I decreased the weights of the rules in V1 to 20,20 and 25% and gave the 35% weigtage to SIFT which was working well. 

## Effect of the change: accuracy before/after on easy vs hard
- Before the accuracy was like 6/60 images being matched, now it jumped to 42 out of 60 images. 
- Results (Based on all modified, hard and random images)
  Before: processed 135 images: 55 matched, 80 rejected
  After: processed 135 images: 89 matched, 46 rejected

## Trade-offs: what new costs or risks did Rule 4 introduce
- I guess run time was increased with this, I have ran this rule and it ran for a longer duration than before.
- Also I added scikit-learn to the requirements for KNN Model, I guess it counts as an additional system requirement, but it certainly is not a burden.