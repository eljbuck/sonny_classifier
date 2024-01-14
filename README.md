# sonny_classifier

`sonny_classifier` is a Naive Bayes classifier that aims to tell the difference between jazz musicians Sonny Rollins and Sonny Stitt. It does so by analyzing two features of the MIDI representations of their solos as training. Then, given a new, unknown MIDI solo, the classifier will estimate whether it was more likely to have been played by Sonny Rollins or Sonny Stitt (based on its training data). 

## Motivation

It can be very frustrating when you hear music that you like, but you cannot to identify who the artist is. Luckily,in jazz, if musicians are correctly credited, you can typically figure out who plays what based on differing instruments. When two players on the same session play the same instrument, however, things get trickier. In this case, even if both are credited, it is exceedingly difficult to differentiate who is playing what, unless you are extremely familiar with one or both of their playing. This situation is not uncommon, particularly in older jazz recordings. One example is in a very famous record by Dizzy Gillespie, *Sonny Side Up*. This record features two well-known tenor saxophonists, Sonny Rollins and Sonny Stitt. As such, it is difficult to determine whether a given tenor sax solo is played by Rollins or Stitt. So, I aimed to make a linear classifier that could differentiate between them. 

## Installation

### Method 1: 

Download .zip file from [live app.](https://ccrma.stanford.edu/~eljbuck/109/project/)

### Method 2: Install from Source

```{bash}
git clone https://github.com/eljbuck/sonny_classifier.git
```

## Usage
To run the classifier, navigate to `./src/algo`. Then, with Python 3 installed, run the following command in the command line:

```bash
python3 sonny_classifier.py
```

## Output
The output of this command will print 6 classifications, based on their solos from two songs, "The Eternal Triangle" and "On The Sunny Side of the Street" ("OTSSOTS"). 

The first four will be the classification of Stitt's solo on "OTSSOTS", followed by Rollin's solo on "OTSSOTS", followed by Stitt's solo on "The Eternal Triangle", followed by Rollin's solo on "The Eternal Triangle". 

The next two classifications will use a modified algorithm to determine, given two solos on a song (where exactly one must be Stitt and exactly one must be Rollins), which solo is more likely to be Stitt and which is more likely to be Rollins. It will then perform this classification on the solos from "OTSSOTS" and then "The Eternal Triangle".

## Modify
Currently, the web application does not support importing MIDI files. As such, the only way to interact with the classifier is to modify the `sonny_classifier.py` file, located here: `./src/algo/sonny_classifier.py`. There are three basic modifications one can make.

### 1. Add training data

To add training data to either Stitt or Rollins, first import the relevant MIDI files into `./src/algo/midi_files`. For demonstration's sake, let's import two new files: `rollins_train.mid` and `stitt_train.mid`, each with a BPM (beats per minute) of 120.0. Once we move these files into the `midi_files` directory, we can then modify `sonny_classifier.py`. To do so, add the correct file paths and associated BPM to the training lists (`stitt_train_midi` and `rollins_train_midi`) on lines 17 and 18:

#### Before

```python
stitt_train_midi = {'./midi_files/stitt_training.mid': 135.0}
rollins_train_midi = {'./midi_files/rollins_training.mid': 120.0}
```

#### After

```python
stitt_train_midi = {'./midi_files/stitt_training.mid': 135.0, './midi_files/stitt_train.mid': 120.0}
rollins_train_midi = {'./midi_files/rollins_training.mid': 120.0, './midi_files/rollins_train.mid': 120.0}
```


### 2. Run classify() on a new test MIDI file

To test a new MIDI file, you will also need to import the file into the `midi_files` directory, located here: `./src/algo/midi_files`. For example's sake, call this file `unknown_test.mid` with a BPM of 120.0. Once `unknown_test.mid` is in the `midi_files` directory, we can then modify `sonny_classifier.py`. To do so, first add the following at line 23, which reads the MIDI file:

```python
unknown_test_midi = {'./midi_files/unknown_test.mid': 120.0}
```

Then, in `main()`, add the following at line 353, which properly formats the data in the MIDI file:

```python
unknown_test = format_data(unknown_test_midi, test=True)
``` 

Finally, also in `main()`, add the following at line 370, which performs the classification based on the training data:

```python
print("unknown_test")
classify(unknown_test, stitt_training_data, rollings_training_data)
```

### 3. Run classify_compare() on two new test MIDI files

To run `classify_compare()` , we will need to import two MIDI files (both from one song) into the `midi_files` directory, located here: `./src/algo/midi_files`. For example's sake, call these files `solo_one.mid` and `solo_two.mid`, each with a BPM of 120.0. Once they are in the `midi_files` directory, we will modify `sonny_classifier.py`. To do so, first add the following at line 23-24, which reads both MIDI files:

```python
solo_one_midi = {'./midi_files/solo_one.mid': 120.0}
solo_two_midi = {'./midi_files/solo_two.mid': 120.0}
```

Then, in `main()` add the following lines at line 353, which formats the data:

```python
solo_one = format_data(solo_one_midi, test=True)
solo_two = format_data(solo_two_midi, test=True)
``` 

Finally, also in `main()`, add the following at line 370, which performs the classification:

```python
print("classify song with solo_one and solo_two")
classify_compare(solo_one, solo_two, stitt_training_data, rollings_training_data)
```
