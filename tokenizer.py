
def find_freq(ids):
    pair_frequency = {}
    for pair in zip(ids, ids[1:]): # Pythonic way to iterate consecutive elements
        pair_frequency[pair] = pair_frequency.get(pair, 0) + 1
        
    return(pair_frequency)
    

# In a new list, replace all consecutive ids equal to pair with idx
def merge(ids, pair, idx):
    newids = []
    i = 0
    while i < len(ids):
        if i < len(ids) - 1 and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            newids.append(idx)
            i += 2
        else:
            newids.append(idx[i])
            i += 1
    return newids


# ---
vocab_size = 276 # desired end vocabulary size
num_merges = vocab_size - 256
merges = {}


for i in range(num_merges):
    stats = find_freq(ids)
    pair = max(stats, key=stats.get)
    idx = 256 + i
    ids = merge(ids, pair, idx)
    merges[pair] = idx
    
    
vocab = {idx: bytes([idx]) for idx in range(256)}
for (p0, p1), idx in merges.items():
    vocab[idx] = vocab[p0] + vocab[p1]
    
def decode(ids):
    # given ids return Python string
    tokens = b"".join(vocab[idx] for idx in ids)
    text = tokens.decode("utf-8", errors='replace')
    return text

def encode(text):
    tokens = list(text.encode("utf-8"))
    while len(tokens) >= 2:
        stats = find_freq(tokens)
        pair = min(stats, key=lambda p: merges.get(p, float("inf")))
        if pair not in merges:
            break # nothing else can be merged
        
        idx = merges[pair]
        tokens = merge(tokens, pair, idx)
    return tokens
    