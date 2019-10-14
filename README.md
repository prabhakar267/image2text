# Convert Image to Text
[![Build Status](https://api.travis-ci.org/prabhakar267/ocr-convert-image-to-text.svg?branch=master)](https://travis-ci.org/prabhakar267/ocr-convert-image-to-text)

Python wrapper to grab text from all the images in a directory and save a subdirectory as text files using [Tesseract Engine](https://github.com/tesseract-ocr/tesseract).

> Tesseract is an optical character recognition engine for various operating systems. It is free software, released under the Apache License, Version 2.0, and development has been sponsored by Google since 2006. In 2006 Tesseract was considered one of the most accurate open-source OCR engines then available.

## Usage
#### Run
```
python main.py -i <input_directory> -o <output_directory>
```
```
usage: main.py [-h] -i INPUT [-o OUTPUT] [-d]

required arguments:
  -i INPUT, --input INPUT       Single image file path or images directory path

optional arguments:
  -o OUTPUT, --output OUTPUT    (Optional) Output directory for converted text
  -d, --debug                   Enable verbose DEBUG logging
```
#### Example
```
python main.py -i sample/
```
or
```
python main.py -i sample/ -o output/
```

#### Run Tests
```
python -m unittest
```

## Tesseract Installation
#### Linux

```
[sudo] apt-get install tesseract-ocr
```
#### Windows
1. Install tesseract-ocr from UB Mannheim here: https://github.com/UB-Mannheim/tesseract/wiki
2. Add the installed Tesseract-OCR directory path to PATH system variable


### Sample image taken

(Wikipedia page for Google | Lang : Simple English)

![](/sample/file-page1.jpg?raw=true)

### Text output
```
 

A man signing in at Google’s main aﬁce, Googleplex.

Google Inc. is an American multinational corporation
that is best known for running one of the largest search
engines on the World Wide Web (WWW). Every day,
200 million (200,000,000) people use it. Google’s main
ofﬁce (“Googleplex”) is in Mountain View, California,
USA.

With Google Search, people can also search for pictures,
Usenet newsgroups, news, and things to buy online. By
June 2004, Google had 4.28 billion web pages on its
database, 880 million (880,000,000) pictures and 845
million (845,000,000) Usenet messages — six billion
things.

“To google,” as an action word (verb) means “to search
for something on Google”. Because Google is so popular
(more than half of people on the web use it) it has been
used to mean “to search the web”. Google dislikes this
use since the name of the company is a trademark.

As a public company, Google Inc. trades on the
NASDAQ under the tickers GOOG and GOOGL.

In August 2015, Google announced it was being restruc-
tured under a new holding company called Alphabet Inc.

1 History

Google was started in early 1996 by Larry Page and
Sergey Brin, two students at Stanford University, USA.
It used to be called Backrub. Later, they made it into a
company, Google Inc., on September 7, 1998 at a friend’s
garage in Menlo Park, California. In February 1999, the
company moved to 165 University Ave., Palo Alto, Cal-
ifornia. Later that year, it moved to another place, now

called the “Googleplex”.

In September 2001, Google’s rating system (“PageR-
ank”, for saying which information is more helpful) got a
US. Patent. The patent was to Stanford University, with
Lawrence (Larry) Page as the inventor (the person who
ﬁrst had the idea).

Google makes an important, though shrinking, percent-
age of its money through its friends like America Online
and InterActiveCorp. It has a special group known as the
Partner Solutions Organization (PSO) which helps make
contracts, helps making accounts better, and gives engi-
neering help.

2 How Google makes money

Google makes money by advertising. People or compa-
nies who want people to buy their product, service, or
ideas give Google money, and Google shows an adver-
tisement to people Google thinks will click on the adver-
tisement. Google only gets money when people click on
the link, so it tries to know as much about people as pos-
sible to only show the advertisement to the “right people”.
It does this with Google Analytics, which sends data back
to Google whenever someone visits a web site. From this
and other data, Google makes a proﬁle about the person,
which it then uses to ﬁgure out which advertisements to
show.

3 The name “Google”

The name “Google” is a misspelling of the word
g00g01.[7][8] Milton Sirotta, nephew of US. mathemati-
cian Edward Kasner, made this word in 1938, for the
number 1 followed by one hundred zeroes ( 10100 ). It
is said that the word “googol” was chosen as a name for
this number because it sounded like baby talk. Google
uses this word because the company wants to make lots
of stuff on the Web easy to ﬁnd and use. Andy Bechtol-
sheim ﬁrst thought of the name.

The name for Google’s main ofﬁce, the “Googleplex,” is a
play on a different, even bigger number, the "googolpleX",
which is 1 followed by one googol of zeroes.


```

### Stargazers over time

[![Stargazers over time](https://starcharts.herokuapp.com/prabhakar267/ocr-convert-image-to-text.svg)](https://starcharts.herokuapp.com/prabhakar267/ocr-convert-image-to-text)


      
