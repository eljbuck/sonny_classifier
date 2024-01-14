"""
name: sonny_classifier.py
=========================
author: Ethan Buck
date: 12/06/2023

desc: a Naive Bayes classifier to differentiate tenor saxophonists Sonny Rollins and Sonny
Stitt on the album, Sonny Side Up.
"""

import mido
from mido import MidiFile
import numpy
import matplotlib.pyplot as plt

# all midi files and their corresponding tempos
stitt_train_midi = {'./midi_files/stitt_training.mid': 135.0}
rollins_train_midi = {'./midi_files/rollins_training.mid': 120.0}
stitt_on_sunny_midi = {'./midi_files/sunny_test_stitt.mid': 120.0}
rollins_on_sunny_midi = {'./midi_files/sunny_test_rollins.mid': 120.0}
stitt_on_eternal_midi = {'./midi_files/eternal_test_stitt.mid': 138.0}
rollins_on_eternal_midi = {'./midi_files/eternal_test_rollins.mid': 138.0}


"""
func: get_tempo()
==================
desc: given a MidiFile as mid, returns set tempo or default otherwise
"""
def get_tempo(mid):
    for msg in mid.play():
        if msg.type == 'set_tempo':
            return msg.tempo
        else:
         # Default tempo.
            return 500000
    
"""
func: position()
================
desc: given a MidiFile as mid, this function returns the index of the first note
"""
def position(mid):
    i = 0
    while not mid.tracks[0][i].type == 'note_on':
        i += 1
    return i

"""
func: populate_map()
====================
given a path to a  monophonic, legato, non-overlapping midi file, this function returns
a dictionary of the total time elapsed (in sec) since the first note and the midi note value. 
For example, let t_i = total time elapsed from the beginning of the first note to the end of 
the ith note and let n_i = midi value for the ith note. Our dictionary takes the following format:

{ t_1: n_1, t_2: n_2, ... , t_i: n_i }
"""
def populate_map(midi_file_path):
    map = {}
    mid = MidiFile(midi_file_path)
    ticks_elapsed = 0
    polytouch_sum = 0
    mid_tempo = get_tempo(mid)
    advance = position(mid)     # starts counting time at the beginning of the file
    for i in range(len(mid.tracks[0]) - advance):
        msg = mid.tracks[0][i + advance]
        if msg.type == 'polytouch':     # accounts for time elapse during weird polytouch state
            polytouch_sum += msg.time
        elif msg.type == 'note_off':
            ticks_elapsed += msg.time + polytouch_sum
            map[mido.tick2second(ticks_elapsed, mid.ticks_per_beat, tempo=mid_tempo)] = msg.note
            polytouch_sum = 0
    return map

"""
func: get_times()
=================
desc: given a dictionary of time stamps as time_map and the corresponding note changes, 
this function returns the list of times (in ms) in between each of the notes.
"""
def get_times(time_map):
    prev = 0
    times = []
    for time in time_map:
        times.append(round((time - prev) * 1000, 2))
        prev = time
    return times

"""
func: get_note_durs()
====================
desc: given a list of times and a bpm, this function returns a list of note duration
values (e.g. 1/16 note, 1/8 triplet, dotted half, etc). This discretizes our timing data, 
as well as normalizes varying bpms"""
def get_note_durs(times, bpm):
    durs = []
    bpms = bpm / 60 * 1000   # gets beats per millisecond
    sixteenth = bpms / 4     # duration of 16th note in ms (can do our cutoff calculations based on this)
    eighth = 2 * sixteenth   # duration of 8th note in ms
    quarter = 2 * eighth     # etc.
    half = 2 * quarter
    whole = 4 * quarter
    eighth_t = quarter / 3   # eighth note triplet
    quarter_t = half / 3     # quarter note triplet
    dot_half = quarter * 3   # dotted half note
    for time in times:
        if (time > whole - eighth): # check greater than 3/4 note cutoff
            durs.append('>=4/4')
        elif (time > dot_half - eighth): # check greater than half note cutoff
            durs.append('3/4')
        elif (time > half - eighth): # check greater than 1/4 note cutoff
            durs.append('1/2')
        elif (time > (quarter + quarter_t) / 2): #checks greater than 1/4 trip cutoff
            durs.append('1/4')
        elif (time > (quarter_t + eighth) / 2): # checks greater than 1/8 note cutoff
            durs.append('1/4t')
        elif (time > (eighth + eighth_t) / 2): # checks greater than 1/8 trip cutoff
            durs.append('1/8')
        elif (time > (eighth_t + sixteenth) / 2): # checks greater than 1/16 note cutoff
            durs.append('1/8t')
        elif (time > (eighth_t + sixteenth) / 2 - sixteenth): # checks greater than < 1/16 cutoff
            durs.append('1/16')
        else: # we know our note is faster than a 16th note
            durs.append('<1/16')
    return durs

"""
func: get_dur_map()
====================
desc: given a list of note durations, this function creates a frequency map of different
duration note values (e.g. 1/16 note, 1/8 triplet note, 1/8 note, 1/4 triplet note, etc)
"""
def get_dur_map(durs):
    # instantiates map with laplace prior (assume at least 1 has been observed for each bucket)
    dur_map = {'<1/16': 1, '1/16': 1, '1/8t': 1, '1/8': 1, '1/4t': 1, 
               '1/4': 1, '1/2': 1, '3/4': 1, '>=4/4': 1} 
    for dur in durs:
        dur_map[dur] += 1
    return dur_map

"""
func: get_notes()
=================
desc: given a dictionary of time stamps and the corresponding note changes, this function
returns a list of all the notes (in terms of midi numbers) played throughout
"""
def get_notes(time_map):
    notes = []
    for time in time_map:
        notes.append(time_map[time])
    return notes

"""
func: get_intervals()
=====================
desc: given a list of notes (in midi), this function returns a list of the intervals
in between each of the notes (returns list of size len(notes) - 1)
"""
def get_intervals(notes):
    intervals = []
    for i in range(len(notes)):
        if i < len(notes) - 1:
            intervals.append(notes[i + 1] - notes[i])
    return intervals

"""
func: get_intervals_map()
=========================
desc: given a list of intervals, this function returns a frequency map of all intervals
(with laplace prior for all possible intervals)
"""
def get_intervals_map(intervals):
    map = {}
    #laplace prior for all possible intervals (extremely unlikely a leap of > 24 semitones occurs)
    for i in range(24):
        map[i] = 1
        map[-i] = 1    
    for interval in intervals:
        if interval in map:
            map[interval] += 1
        else:
            map[interval] = 1
    # sort the dictionary for convenience
    keys = list(map.keys())
    keys.sort()
    sorted_dict = {i: map[i] for i in keys}
    return sorted_dict

"""
func: map_to_pmf()
===================
desc: given any frequency map, this function returns a dictionary of the pmf
"""
def map_to_pmf(map):
    pmf = map
    sum = 0.0
    for key in map:
        sum += map[key]
    for key in pmf:
        pmf[key] /= sum
    return pmf

"""
func: format_data()
===================
desc: given a list of midi file names, if test param is false (i.e. data is for training), 
this function returns a list in the following format:

[ {duration_pmf} , {interval_pmf} ], where duration_pmf and interval_pmf
are both dictionarys and duration_pmf['1/4'] = P(playing a quarter note)

if test param is true (i.e. data is for testing) the function returns the following format:

[ [dur_list], [intvl_list] ], where dur_list and intvl_list are lists of all instances
of note durations and intervals in the given midi files
"""
def format_data(midi_file_names, test):
    output = []
    dur_list = []
    intvl_list = []
    for midi_file_name in midi_file_names:
        map = populate_map(midi_file_name)
        times = get_times(map)
        dur_list += get_note_durs(times, midi_file_names[midi_file_name])
        notes = get_notes(map)
        intvl_list += get_intervals(notes)
    if test:
        output.append(dur_list)
        output.append(intvl_list)
    else: 
        dur_map = get_dur_map(dur_list)
        intvl_map = get_intervals_map(intvl_list)
        output.append(map_to_pmf(dur_map))
        output.append(map_to_pmf(intvl_map))
    return output

"""
func: plot_pmf()
================
desc: given a pmf dictionary, this function plots the pmf using matplotlib
"""
def plot_pmf(pmf, title):
    keys = list(pmf.keys())
    vals = list(pmf.values())
    color = (0.6509803921568628, 0.11372549019607843, 0.13725490196078433)
    plt.bar(keys, vals, width=0.8, color=color)
    plt.title(title)
    for i, j in enumerate(vals):
        if (type(keys[0]) == int):
            plt.text(i + keys[0], j, str(round(j, 3)), ha='center')
        else:
            plt.text(i, j, str(round(j, 3)), ha='center')
    plt.show()

"""
func: calc_log_score()
======================
desc: given training data, test data, and a prior, this funtion uses Naive Bayes 
to calculate the log of the likelihood score that the test data
was played by the subject of the training data
"""
def calc_log_score(training_data, test_data, prior):
    log_p_dur_given_training = 0
    for dur in test_data[0]:
        p_played_by_training = numpy.log(training_data[0][dur])
        log_p_dur_given_training += p_played_by_training
    log_p_interval_given_training = 0
    for interval in test_data[1]:
        p_played_by_training = numpy.log(training_data[1][interval])
        log_p_interval_given_training += p_played_by_training
    return numpy.log(prior) + log_p_interval_given_training + log_p_dur_given_training

"""
func: classify() 
================
desc: given some test data, as well as Stitt's and Rollin's training data, this 
function compares the log likelihood scores given Stitt and Rollins and 
estimates whether it is more likely that Stitt played the test data or 
Rollins played the test data
"""
def classify(test_data, stitt_data, rollins_data):
    log_p_stitt = calc_log_score(stitt_data, test_data, 0.5)
    log_p_rollins = calc_log_score(rollins_data, test_data, 0.5)
    print("LL(Stitt) =", round(log_p_stitt, 2))
    print("LL(Rollins) =", round(log_p_rollins, 2))
    margin = round(numpy.abs(log_p_stitt - log_p_rollins), 2)
    if log_p_stitt - log_p_rollins > 0:
        print('It is most likely to have been played by Stitt, with a margin of ', margin)
    else:
        print('It is most likely to have been played by Rollins, with a margin of ', margin)

# prepackaged print statement to be used be classify_compare()
def print_stitt_first():
    print('It is most likely that Stitt was first and Rollins was second')
# prepackaged print statement to be used be classify_compare()
def print_rollins_first():
    print('It is most likely that Rollins was first and Stitt was second')

"""
func: classify_compare()
========================
desc: given two pieces of test data (assuming exactly one is Stitt and one is Rollins),
this function indicates which data set is more likely to have been played by Stitt
and which is more likely to have been played by Rollins.
"""
def classify_compare(test_data1, test_data2, stitt_data, rollins_data):
    log_p_stitt1 = calc_log_score(stitt_data, test_data1, 0.5)
    log_p_rollins1 = calc_log_score(rollins_data, test_data1, 0.5)
    margin1 = numpy.abs(log_p_stitt1 - log_p_rollins1)
    log_p_stitt2 = calc_log_score(stitt_data, test_data2, 0.5)
    log_p_rollins2 = calc_log_score(rollins_data, test_data2, 0.5)
    margin2 = numpy.abs(log_p_stitt2 - log_p_rollins2)
    if log_p_stitt1 - log_p_rollins1 > 0: # we know our model thinks the 1st data set is from Stitt
        if log_p_stitt2 - log_p_rollins2 > 0: # if 2nd set is also from Stitt, decide based on margin
            if margin1 > margin2:
                print_stitt_first()
            else:
                print_rollins_first()
        else: 
            print_stitt_first()
    else: # we know our model thinks the 1st data set is from Rollins
        if log_p_stitt2 - log_p_rollins2 < 0: # if 2nd set is also from Rollins, decide based on margin
            if margin1 > margin2:
                print_rollins_first()
            else:
                print_stitt_first()
        else:
            print_rollins_first()

"""
func: main()
============
desc: initializes and formats test and train data, then runs classifier.
"""
def main():
    # FORMATTING TRAINING DATA
    stitt_training_data = format_data(stitt_train_midi, test=False)
    rollins_training_data = format_data(rollins_train_midi, test=False)

    # UNCOMMENT TO DISPLAY FREQUENCY DISTRIBUTIONS
    # plot_pmf(stitt_data[0], "Stitt Note Durations")       
    # plot_pmf(rollins_data[0], "Rollins Note Durations")
    # plot_pmf(stitt_data[1], "Stitt Intervals")
    # plot_pmf(rollins_data[1], "Rollins Intervals")

    # FORMATTING TESTING DATA
    stitt_on_sunny = format_data(stitt_on_sunny_midi, test=True)
    rollins_on_sunny = format_data(rollins_on_sunny_midi, test=True)
    stitt_on_eternal = format_data(stitt_on_eternal_midi, test=True)
    rollins_on_eternal = format_data(rollins_on_eternal_midi, test=True)
    # ADD NEW TEST DATA BELOW
    
    
    # PRINTING RESULTS
    print("stitt on Sunny Side of the Street:")
    classify(stitt_on_sunny, stitt_training_data, rollins_training_data)
    print("rollins on Sunny Side of the Street:")
    classify(rollins_on_sunny, stitt_training_data, rollins_training_data)
    print("stitt on The Eternal Triangle:")
    classify(stitt_on_eternal, stitt_training_data, rollins_training_data)
    print("rollins on The Eternal Triangle:")
    classify(rollins_on_eternal, stitt_training_data, rollins_training_data)
    print("classify Sunny Side of the Street:")
    classify_compare(stitt_on_sunny, rollins_on_sunny, stitt_training_data, rollins_training_data)
    print("classify The Eternal Triangle:")
    classify_compare(stitt_on_eternal, rollins_on_eternal, stitt_training_data, rollins_training_data)
    # ADD NEW TEST RESULTS BELOW (e.g. classify(new_data, stitt_training_data, rollins_training_data) or 
    #                             classify_compare(new_stitt, new_rollins, stitt_training_data, rollins_training_data))


if __name__ == "__main__":
    main()