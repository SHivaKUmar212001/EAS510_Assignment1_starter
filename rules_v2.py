"""EAS 510 - Project 1 - Phase 2: the V2 rule set.

Rules 1-3 are kept exactly as in `rules.py`. Your job is to ADD Rule 4 that
targets the systematic weakness you diagnosed from results_v1_hard.txt.

Constraint: the rules' `out_of` weights must still sum to 100 so the Final
Score stays on a /100 scale (the format validator enforces "Final Score:
<s>/100" equals the sum of the block's rule scores).

Example split that keeps the original spirit: Rules 1-3 -> 25/25/40 and
Rule 4 -> 10 (or trim the losers more aggressively).
"""

import rules
from functools import lru_cache
import cv2

#: Import the original rules and append your new one.

def new_wt(result, n):
    result = dict(result)
    result["score"] = round(result["score"] * n / result["out_of"])
    result["out_of"] = n
    return result

def rule1_v2(target, path): 
    return new_wt(rules.rule1_metadata(target, path), 20)
def rule2_v2(target, path): 
    return new_wt(rules.rule2_histogram(target, path), 20)
def rule3_v2(target, path): 
    return new_wt(rules.rule3_template(target, path), 25)
 

RULES = ("rule1_v2", "rule2_v2", "rule3_v2", "rule4_sift") 

sift = cv2.SIFT_create(nfeatures=1000)

@lru_cache(maxsize=None)
def find_spots(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    scale = 1000 / max(img.shape)
    img = cv2.resize(img, None, fx=scale, fy=scale)
    _, spots = sift.detectAndCompute(img, None)
    return spots

from sklearn.neighbors import NearestNeighbors

def rule4_sift(target, input_path):
    spots_org = find_spots(target["path"])
    spots_input  = find_spots(input_path)

    if spots_org is None or spots_input is None:   
        x = 0
    else:
        knn = NearestNeighbors(n_neighbors=2)          
        knn.fit(spots_org)                         
        dist, idx = knn.kneighbors(spots_input)
        
        x = 0
        for d in dist:
            if d[0] < 0.6 * d[1]:
                x += 1                 

    score = min(35, round(x / 100 * 35))

    if x < 30:
        score = 0
    
    return {
        "rule": 4,
        "name": "SIFT",
        "fired": x >= 30,
        "score": score,
        "out_of": 35,
        "note": x,
        "metric": round(min(1, x / 100), 2),
    }