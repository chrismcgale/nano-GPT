<h1>NANO GIPTY</h1>

The accronym GPT (Generative Pre-Trained Transformer) is self explanatory. It's a transformer that is pre-trained and generates something..., but what is a transformer?

<h2>Role out</h2>

![image](https://github.com/chrismcgale/nano-GPT/assets/56483395/5d5964bf-e5ef-4f85-9463-eccb804c48ab)

This is the traditional picture of a transformer architecure. The left side of the model encodes input to a sequence of states and the right side is the decoder, which takes the output from the encoder and predicts the next appropriate token.

<b>But this is not what GPT uses. GPT is a decoder only model so throw out the left side.

This means that GPT uses the input tokens directly to create an output token of the same type. This can be fed back into the system to continuously produce new tokens.

<h2>What the hell is a token?</h2>

A token is just a short fragment of some input. The most basic token is a binary 0 or 1, but they can even be whole words / sentences depending on the systems resources. Larger tokens allow models to store more information and perform better however, they demand significant memory and computational resources.

<h2>How does this create?</h2>

Given a set of previous tokens (aka the context) he transformer uses a method called 'self-attention' to create a probaility distribution of the next token.


Transformer Architecure As described by Andrej Karpathy https://www.youtube.com/watch?v=kCc8FmEb1nY
