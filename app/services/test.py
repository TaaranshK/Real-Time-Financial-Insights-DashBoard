# #ip/ ->input -> ["eat", "tea", "tan", "ate", "nat", "bat"]
# output -> [
# ["eat","tea","ate"],
# ["tan","nat"],
# ["bat"]
# ] 
from collections import defaultdict
def group(strs):
    groups = defaultdict(list)
    for w in strs:
        key = "".join(sorted(w))
        groups[key].append(w)

    return list(groups.values())

strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
print(group(strs))
       
