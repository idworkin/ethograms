#!usr/bin/env python

# This script takes Cody & Abhijna's Jwatcher output .dat files and
# outputs a set of .csv files that ought to facilitate analysis.
# It then combines all the new .csv's into on big file.
# UPDATED version as of 8th May 2013 (by WILL)
# UPDATED by Abhijna on 15th May 2013

# WARNING
# BAD THINGS WILL HAPPEN IF OTHER FILES ARE IN THE FOLDER WHEN YOU RUN THIS SCRIPT!

# code key

# a = approach (state)
# b = pause (event)
# c = circle (state)
# d = wing display (event)
# e = inching (state)
# f = flying (event)
# g = grooming (state)
# h = out of sight
# i = turning (event)
# j = jumping (event)
# o = orientation (event)
# p = pursuit (state)
# q = reverse walk (state)
# r = running (state)
# s = stopping (state)
# w = walking (state)
# y = abdominal lift (event)
# z = capture (event)

# 1 = spider enters (numbers are pred states) [make 1 or 0 spider presence col]
# 2 = attempted strike (pred event)
# 3 = predator within striking distance (pred state)
# 4 = predator present but not within striking distance (pred state)
# 6 = chasing (pred state)
# 7 = chasing ends


########################################


### getting a workspace ready ### edit these dictionaries to recode the output factors

States = { 'a':'approach', 'c':'circle', 'e':'inch', 'g':'groom', 'h':'timeout', 'p':'pursuit', 'q':'revwalk', 'r':'run', 's':'stop', 'w':'walk' }

Events = {  'd':'wingdisp', 'j':'jump', 'o':'orient', 'y':'ablift', 'z':'capture', 'f':'fly', 'b':'pause', 'EOF':'end_trial' } # if you want an end of file event, then add 'EOF':'end_trial' or similar to this dictionary and see below

PredStates = { '3':'close', '4':'far' }

PredEvents = { '6':'chase', '7':'chase' } # start and stop have the same factor level so that chasing will be binary

import sys, re, os, glob


### define functions ###


# this looks on the first line where is specifies what line the data start on, then skips to that and reads the data into a list of lists
# e.g. [ ['5531,', 'g'], ['20532,', 'w'],...]
def pull_out_data( InfileName ):
    with open( InfileName, 'r' ) as Infile:
        datstart = int( Infile.readline().split('=')[1] )
        Data = []
        for i, line in enumerate( Infile ):
            if i >= (datstart - 2):
                line = line.strip().split()
                Data.append( line )
    return Data


# this function grabs the metadata from the top of the file and returns, e.g ['1366998114371', '1366999915150', 'F', '4', 'FVW', 'rep1', '937', '23']
def pull_out_info( InfileName ):
    with open( InfileName, 'r' ) as Infile:
        Info = []
        for line in Infile:
            if line.split('=')[0] == "StartTime":   # start and stop time grepping are fossils, but may be useful at some point WP
                Info.append( line.strip().split('=')[1] )
            elif line.split('=')[0] == "StopTime":
                Info.append( line.strip().split('=')[1] )    
            elif line.split('.')[0] == "Answer":
                Info.append( line.strip().split('=')[1] )
    return Info


# this grabs the 'Data' & 'Info' lists from the 2 functions above and gloms them together into an easy-to-read file for further processing
def make_temp( Data, Info, InfileName ):
    OutfileName = InfileName.replace( '.dat', '.csv' )
    Info = [ str.replace(' ', '_') for str in Info ]
    with open( OutfileName, 'w' ) as Outfile:
        Outfile.write( "days.spider.starved ,age,humidity,pop,rec.time,temp,time.stamp,code\r\n" )
        for i in Data:
            OutLine = ','.join( [ ','.join( Info[2:8] ), ''.join( i ) ] )
            Outfile.write( OutLine + '\r\n' )


# this reads the file written by make_temp looking for '0' timestamps, replacing them with the midpoint of the proceeding and following ones
# it then overwrites to old file with the fixed version
def check_time_stamps( File ):
    with open( File, 'r') as Infile, open( 'temp.txt', 'w') as Outfile:
        lines = [ line.strip().split(',') for line in Infile]
        for i in range( 0, len( lines ) ):
            if lines[i][6] == '0':
                lines[i][6] = str( int(lines[i+1][6]) - int(lines[i-1][6]) /2 + int(lines[i][6]) )
        for line in lines:
            Outfile.write( ','.join(line) + '\r\n' )
    os.rename( 'temp.txt', File )


# this builds the events column; asking at each line if the code is an event, then appends the matching value from the dictionary up top
def reformat_events( File ):
    with open( File, 'r') as Infile, open( 'temp.txt', 'w') as Outfile:
        lines = [ line.strip().split(',') for line in Infile]
        for line in lines:
            E = line[7]
            if E in Events:
                line.append( Events[ E ] )
            else:
                line.append( '0' )
        for line in lines:
            Outfile.write( ','.join(line) + '\r\n' )
    os.rename( 'temp.txt', File )


# this does a similar thing for states, then goes back and replaces zero values with the last non-zero so that when states change they are 'sticky' until the next change
def reformat_states( File ):
    with open( File, 'r') as Infile, open( 'temp.txt', 'w') as Outfile:
        lines = [ line.strip().split(',') for line in Infile]
        for line in lines:
            E = line[7]
            if E in States:
                line.append( States[ E ] )
            else:
                line.append( '0' )
        for i in range( 0, len( lines )):
            if lines[i][9] == '0':
                lines[i][9] = lines[i-1][9]
        for line in lines:
            Outfile.write( ','.join(line) + '\r\n' )
    os.rename( 'temp.txt', File )


# this function makes 3 passes; 1st makes a strike column ('0' or 'strike', then makes a pred. state col, then goes over that col to make states 'sticky'
def reformat_predator( File ):
    with open( File, 'r') as Infile, open( 'temp.txt', 'w') as Outfile:
        lines = [ line.strip().split(',') for line in Infile]
        for line in lines:
            if line[7] == '2':
                line.append( 'strike' )
            else:
                line.append( '0' )
        for line in lines:
            if line[7] in PredStates:
                line.append( PredStates[ line[7] ] )
            else:
                line.append( '0' )
        for i in range( 0, len( lines )):
            if lines[i][11] == '0':
                lines[i][11] = lines[i-1][11]
        for line in lines:
            Outfile.write( ','.join(line) + '\r\n' )
    os.rename( 'temp.txt', File )


## this is a fossil from the first version of this script ##
# def reformat_modifier( File ):
#     with open( File, 'r') as Infile, open( 'temp.txt', 'w') as Outfile:
#         lines = [ line.strip().split(',') for line in Infile]
#         for line in lines:
#             if line[7] == '5':
#                 line.append( '5' )
#             else:
#                 line.append( '0' )
#         for line in lines:
#             Outfile.write( ','.join(line) + '\r\n' )
#     os.rename( 'temp.txt', File )


# this replaces the above - it makes a chase column and makes chasing (but not stopping) a 'sticky' state
def reformat_chasing( File ):
    with open( File, 'r') as Infile, open( 'temp.txt', 'w') as Outfile:
        lines = [ line.strip().split(',') for line in Infile]
        for line in lines:
            if line[7] in PredEvents:
                line.append( line[7] )
            else:
                line.append( '0' )
        for i in range( 0, len( lines )):
            if lines[i][12] == '0' and lines[i-1][12] != '7':
                lines[i][12] = lines[i-1][12]
        for line in lines:
            if line[12] in PredEvents:
                line[12] = PredEvents[ line[12] ]
        for line in lines:
            Outfile.write( ','.join(line) + '\r\n' )
    os.rename( 'temp.txt', File )


# this just overwrites the nonsense header that has accreted thus far with a sensible one
def fix_header( File ):
    with open( File, 'r') as Infile, open( 'temp.txt', 'w') as Outfile:
        Infile.readline()
        lines = [ line.strip().split(',') for line in Infile]
        Outfile.write( "days.spider.starved,age,humidity,pop,rec.time,temp,time.stamp,code,event,state,strike,pred.state,chasing\r\n" )
        for line in lines:
            Outfile.write( ','.join(line) + '\r\n' )
    os.rename( 'temp.txt', File )


# ...and lastly this takes all the files, tosses the header line and gloms them together, throwing out the EOF line and reporting an error if any lines are the wrong length
def write_big_csv( Infile_List, BigFileName ):
    with open( BigFileName, 'w' ) as Outfile:
        Outfile.write( "file,days.spider.starved,age,humidity,pop,rec.time,temp,time.stamp,code,event,state,strike,pred.state,chasing\r\n" )
        for file in Infile_List:
            Infile = open( file, 'r' )
            Infile.readline()
            for line in Infile:
                line = line.strip()
                if len( line.split(',') ) != 13:
                    print "problem line in %s!" %file
                else: # line.split(',')[ 7 ] != 'EOF': # remove this elif if you want to keep the EOF line
                    Outfile.write( ','.join( [file, line] ) + '\r\n' )


#### work area

# glob list of input files

FileList = glob.glob( '*.dat' )
Nfiles = len( FileList )

# get info. from the user

BigFileName = raw_input('Specify output filename.csv --> ')

# make individual easy-to-read .csv's

for File in FileList:
    make_temp( pull_out_data( File ), pull_out_info( File ), File )

# repeatedly parse each .csv to reformat the data

for File in glob.glob( '*.csv' ):
    check_time_stamps( File )
    reformat_events( File )
    reformat_states( File )
    reformat_predator( File )
    reformat_chasing( File )
    fix_header( File )

# glom all the smaller .csv's into 1 big 1

write_big_csv( glob.glob( '*.csv' ), BigFileName )

# Report!!

print '%i Jwatcher files processed' %Nfiles
