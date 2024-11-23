from annotated_intake import *
from data_intake import *
import os

# get annotated beat txt
def getAnnotatedBeats(song):
    return beat_intake("ground_truth/Beats_Downbeats/" + song + "_Beats.txt")

# get predicted downbeat csv
def getDownbeatOutput(song):
    return parse_downbeats_to_tuples("downbeatOutputs/" + song + "_DBOutput.csv")

# get where the annotated and predicted beats align at the start
def getStart(anno_beats, predicted_beats, threshold=0.1):
    predicted_start_index = 0
    anno_start = anno_beats[0]
    predicted_start = predicted_beats[0]
    while abs(float(predicted_start[0])-float(anno_start[0])) > threshold:
        predicted_start_index=predicted_start_index+1
        if(predicted_start_index < len(predicted_beats)):
            predicted_start = predicted_beats[predicted_start_index]
        else:
            threshold=threshold+0.1
            predicted_start = predicted_beats[0]
    return predicted_start_index

# check all the beats in the annotated and predicted, seeing which match
def checkBeats(anno_beats, predicted_beats, predicted_start_index, threshold=0.1):
    timeCount = 0
    beatCount = 0
    for anno_start_index in range(min(len(anno_beats), len(predicted_beats)-predicted_start_index)):
        if(abs(float(anno_beats[anno_start_index][0]) - float(predicted_beats[predicted_start_index][0])) < threshold):
            timeCount=timeCount+1
        if(float(anno_beats[anno_start_index][1]) == float(predicted_beats[predicted_start_index][1])):
            beatCount=beatCount+1
        predicted_start_index=predicted_start_index+1
    return timeCount, beatCount


def evaluateDownBeatTracker():
    for song in os.scandir("ground_truth/Beats_Downbeats"):
        songName = song.name.strip().split("_")[0]
        print(songName)
        anno_beats = getAnnotatedBeats(songName)
        predicted_beats = getDownbeatOutput(songName)

        predicted_start_index = getStart(anno_beats, predicted_beats)
        timeCount, beatCount = checkBeats(anno_beats, predicted_beats, predicted_start_index)

        print("Percentage of timestamps in time: ", timeCount/len(predicted_beats))
        print("Percentage of timestamps from annotated: ", timeCount/len(anno_beats))
        print("Percentage of downbeats/beats correct: ", beatCount/len(predicted_beats))

