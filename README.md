# Generate common prefixes and suffixes, and words that match them

This package generates lists of affixes (word prefixes and suffixes) of the desired length, and finds words that match them. It chooses from the most common words in the English language, and can return these affixes and their examples sorted in order of length.

The idea is to generate lists of affixes that you can use to practice n-gram recognition in your CW practice. Between instant character recognition and instant word recognition, there's a space where you can start to hear "sound-bites", or short, common letter combinations. Being able to recognise these n-grams will help you progress in your head-copy.

For instance, in English, many words end in `ING` (doing, being, saying, etc.) and many words start with `TH` (they, them, their, there, these, etc.). `ING` is a 3-gram (three letter) suffix, and `TH` is a 2-gram prefix. If you start recognising the sounds they make (_did-it dah-dit dah-dah-dit_, and _dah di-di-di-dit_), you will have an easier time head-copying at reasonable speeds.

## Lists of prefixes and suffixes

If you want to skip running this yourself and just look at some results, [here are a few scenarios you might be interested in](results).

## Using `cw_ngrams`

This simple Python 3.7+ module should be called via the command-line :

```bash
python cw_ngrams.py
```

This will output a list of ten affixes, each with five examples of words that match them. The affixes are in order of frequency, as are the examples for each affix.

```
ING - USING, SHIPPING, BEING, FOLLOWING, INCLUDING
ION - INFORMATION, EDUCATION, VERSION, SECTION, LOCATION
ENT - MANAGEMENT, DEVELOPMENT, CURRENT, GOVERNMENT, DEPARTMENT
PRO - PRODUCTS, PRODUCT, PROGRAM, PROJECT, PROFILE
CON - CONTACT, CONTROL, CONTENT, CONDITIONS, CONFERENCE
HAT - THAT, WHAT, CHAT, HATE, SOMEWHAT
COM - COMPANY, COMMENTS, COMMUNITY, COMPUTER, COMPARE
THE - THEY, THEIR, THERE, THESE, THEM
THA - THAT, THAN, THANKS, THANK, THAILAND
THI - THIS, THINK, THINGS, THING, THIRD
```

There are a bunch of arguments you can use to tailor the output.

- `--ngram_length <N>` : The length of the n-gram affixes you want to generate. This defaults to `3`, giving you tri-grams (things like the common suffix `ING` or the common prefix `PRO`).
- `--n_affixes <N>` : The number of affixes you want to generate. In effect, this controls the number of lines of text to print to screen. This defaults to `10`.
- `--n_examples <N>` : The number of examples you want to generate for each affix. This defaults to `5`.
- `--n_words <N>` : The number of words you want to use to generate the affixes. This defaults to `10000`, using the most common 10,000 words to generate prefixes and suffixes. This is generally a good option unless you start using `--shuffle`, in which case reducing it will help you avoid some of the weirder ones that might not make sense, like the very uncommon `USS` suffix (and its only example, `DISCUSS`).
- `--prefixes` : Passing this argument will generate only common prefixes, and words that match those prefixes.
- `--suffixes` : passing this argument will generate only common suffixes, and words that match those suffixes.
- `--sort` : Return the output sorted in order of length -- both the examples for each affix, and the total length of the examples. This is helpful if you're practicing and want to increase the difficulty as you go. If you leave this option out, both the affixes and their examples will be printed in order of frequency, meaning the most common ones will come up first.
- `--shuffle` : Instead of selecting the most common affixes, randomly choose them. Consider this hard mode : you're going to get some fairly random stuff here. In order to avoid getting some completely weird ones (I've seen `INB` as a prefix, with only example word `INBOX`), this option randomly samples from the most common 1,000 affixes.

## Data

The word and frequency data is based on [Peter Norvig's 1/3 million most frequent English words](https://norvig.com/ngrams/count_1w.txt) truncated down to the top 10,000 words. N-grams are calculated based on word prefixes and suffixes, and can be weighed using the count data in this dataset.
