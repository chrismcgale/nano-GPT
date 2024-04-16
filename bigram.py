
import torch
import torch.nn as nn 
from torch.nn import functional as F

# hyperparameters
batch_size = 32 # number of independent sequences processed in parallel
block_size = 8 # max context length for predictions
max_iters = 3000
eval_iter = 300
learning_rate = 1e-2
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters = 200
n_embed = 32
#----------------

torch.manual_seed(1337)


with open('input.txt', 'r', encoding='utf-8') as f:
    text = f.read()


alphabet = sorted(list(set(text)))
vocab_size = len(alphabet)

stoi = { ch:i for i, ch in enumerate(alphabet) }
itos = { i:ch for i, ch in enumerate(alphabet) }
encode = lambda s: [stoi[c] for c in s] # encodes string as a list of integers
decode = lambda l: ''.join([itos[i] for i in l]) # tae a list of integers, returns a string


data = torch.tensor(encode(text), dtype=torch.long)
n = int(0.9 * len(data))
train_data = data[:n]
val_data = data[:n]


# generate a small batch of data with inputs x and targets y
def get_batch(split):
    data = train_data if split == 'train' else val_data
    ix = torch.randint(len(data) - block_size, (batch_size,))
    x = torch.stack([data[i:i+block_size] for i in ix])
    y = torch.stack([data[i+1:i+block_size+1] for i in ix])
    return x, y


@torch.no_grad()
def estimate_loss():
    out = {}
    model.eval()
    for split in ['train', 'val']:
        losses = torch.zeros(eval_iters)
        for k in range(eval_iters):
            X, Y = get_batch(split)
            logits, loss = model(X, Y)
            losses[k] = loss.item()
        out[split] = losses.mean()
    model.train()
    return out

class BigramLanguageModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, n_embed)
        self.position_embedding_table = nn.Embedding(block_size, n_embed)
        self.lm_head = nn.Linear(n_embed, vocab_size)
        
    def forward(self, idx, targets=None):
        
        # idx and targets are both (B,T) tensor of integers
        tok_emb = self.token_embedding_table(idx) # (Batch, Time, Channel)
        pos_emb = self.position_embedding_table(torch.arrange(T, device=device)) # (T, C)
        x = tok_emb + pos_emb # (B, T, C)
        logits = self.lm_head(tok_emb) # (B,T,vocab_size)
        
        if targets == None:
            loss = None
        else:
            # Reshape
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            
            targets = targets.view(B*T)
            
            loss = F.cross_entropy(logits, targets)
        
        return logits, loss
    
    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens):
            logits, loss = self(idx)
            
            logits = logits[:, -1, :] # becomes (B, C)
            
            probs = F.softmax(logits, dim=-1)
            
            # sample from distribution
            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            
            # append sampled index to the running sequence
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
            
        return idx
    
model = BigramLanguageModel()
m = model.to(device)

optimizer = torch.optim.Adam(m.parameters(), lr=1e-3)


for iter in range(max_iters):
    
    if iter % eval_iters == 0:
        losses = estimate_loss()
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")
        
    xb, yb = get_batch('train')
    
    logits, loss = m(xb, yb)
    optimizer.zero_grad(set_to_none=True)
    loss.backward()
    optimizer.step()

context = torch.zeros((1, 1), dtype=torch.long, device=device)

print(decode(m.generate(context, max_new_tokens=500)[0].tolist()))

