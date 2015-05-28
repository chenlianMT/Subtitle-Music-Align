#!/usr/bin/env python
"""
fetchSubtitles.py

Downloading subtitles from the pyMusixMatch wrapper.

(c) 2015, Chen Liang
"""

import json
from musixmatch import track as TRACK
from musixmatch import artist as ARTIST
from musixmatch import util
import random, re, sys


def getPath(filename = ""):
    """construct file path"""
    return "./data/" + filename


def writeJsonFile(input, filename, mode="w"):
    """write subtitle dictionary into json format"""
    with open(filename, mode) as fout:
        json.dump(input, fout)


def writeSubtitleFile(input, filename, mode="wt"):
    """write subtitle into subtitle file"""
    try:
        input = input.encode('utf-16')
    except:
        try:
            input = input.encode('utf-8')
        except:
            try:
                input = input.encode('windows-1252')
            except:
                raise Exception

    with open(filename, mode) as fout:
        fout.write(input)



def randomFetch(depth, seed="Radiohead"):
    """fetch subtitles from MusiXmatch through a seed artist"""

    try:
        # print "Step 1"
        artist = ARTIST.search(q_artist=seed)[0]
    except:
        errorMsg = "Cannot get seed artist."
        return errorMsg

    # print "Step 2"
    relatedArtistList = []
    errorMsg = getRelatedArtists(artist, depth, relatedArtistList)
    if errorMsg:
        return errorMsg
    # assert type(relatedArtistList[0]) == ARTIST.Artist
    if not relatedArtistList:
        errorMsg = "Not enough related artists."
        return errorMsg

    # print "Step 3"
    tracks = []
    for artist in relatedArtistList:
        trackList = TRACK.search(q_artist=artist.artistdata["artist_name"],
                                 q_lyrics="and")
        if len(trackList) > 1:
            index = random.randint(0, len(trackList)-1)
            tracks.append(trackList[index])
        elif len(trackList):
            index = 0
            tracks.append(trackList[index])
    if not tracks:
        errorMsg = "Not enough tracks."
        return errorMsg

    # print "Step 4"
    subtitles = []
    names = []
    artistNames = []
    for track in tracks:
        if track.trackdata["has_subtitles"]:
            subtitle = track.subtitles()
            if subtitle and len(subtitle["subtitle_body"]) > 0:  # subtitle is not null
                subtitles.append(subtitle)
                names.append(track.trackdata["track_name"])
                artistNames.append((track.trackdata["artist_name"]))
    if not subtitles:
        errorMsg = "Not enough subtitles."
        return errorMsg

    # print "Step 5"
    fileNames = []
    for i in range(len(subtitles)):
        content = subtitles[i]["subtitle_body"]
        name = names[i]
        artistName = artistNames[i]

        # derive proper file name
        fileName = re.sub(r' ', "0tttt", name)
        fileName = re.sub(r'\W', '', fileName)
        fileName = fileName.replace("0tttt", " ")

        fileName2 = re.sub(r' ', "0tttt", artistName)
        fileName2 = re.sub(r'\W', '', fileName2)
        fileName2 = fileName2.replace("0tttt", " ")
        fileName2 = fileName + "-" + fileName2 + ".subtitle"
        writeSubtitleFile(content, getPath(fileName2))
        fileNames.append(fileName2)

    print fileNames
    return fileNames


def getRelatedArtists(seed, depth, relatedArtistList):
    """get a relation chain of length 'depth'"""

    # print "Depth:", depth
    artist = getOneRelatedArtist(seed)

    count = 0
    while artist in relatedArtistList:  # get different artists
        artist = getOneRelatedArtist(seed)
        count += 1
        if count > 10:
            errorMsg = "Bad seed for getting related artists."
            return errorMsg

    relatedArtistList.append(artist)
    depth -= 1

    # recursion base
    if depth:
        getRelatedArtists(artist, depth, relatedArtistList)


def getOneRelatedArtist(seed):
    """get an artist providing seed"""

    body = util.call('artist.related.get', seed.artistdata)
    artist_list_dict = body["artist_list"]
    if len(artist_list_dict) > 1:
        index = random.randint(0, len(artist_list_dict)-1)
    else:
        index = 0

    return ARTIST.Artist(-1, artistdata=artist_list_dict[index]["artist"])

# print randomFetch(10)


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] in \
            ('help', '-help', '--help', 'h', '-h', '--h'):
        print
        print 'fetchSubtitles.py'
        print 'USAGE'
        print '   python fetchSubtitles.py'
        print '          #download Creep\'s subtitle, used as standard input'
        print '   python fetchSubtitles.py inputSet'
        print '          #download subtitles for standard input set'
        print '   python fetchSubtitles.py genreSet'
        print '          #download subtitles for a specific genre'
        print '          #gerneSet choose from Rock or Pop'
        sys.exit(0)

    # download sample subtitles from song Blank_Space and Creep
    # reason of song choice: To see if American English is needed for matching training model
    if len(sys.argv) < 2:
        trackBS = TRACK.Track(74376920)
        print "*********** TRACK Blank Space ACQUIRED ************"
        trackC = TRACK.Track(20031322)
        print "*********** TRACK Creep ACQUIRED ************"

        # write subtitle to json file
        subtitle_dict_BC = trackBS.subtitles()
        fileName = "default-Blank_Space.json"
        writeJsonFile(subtitle_dict_BC, getPath(fileName))

        subtitle_dict_C = trackC.subtitles()
        fileName = "default-Creep.json"
        writeJsonFile(subtitle_dict_C, getPath(fileName))

        # write subtitle
        subtitleBC = subtitle_dict_BC["subtitle_body"]
        #print subtitle
        fileName = "default-Blank_Space.subtitle"
        writeSubtitleFile(subtitleBC, getPath(fileName))

        # write subtitle
        subtitleC = subtitle_dict_C["subtitle_body"]
        #print subtitle
        fileName = "default-Creep.subtitle"
        writeSubtitleFile(subtitleC, getPath(fileName))

        # exit
        print "*********** DOWNLOAD SUCCEED ************"
        sys.exit(0)

    # download subtitles from mixed genres to create a standard input set
        # NOT IMPLEMENTED
    # download subtitles from a certain genre
    # to show the alignment algorithm's preferences
        # NOT IMPLEMENTED