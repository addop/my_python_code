#write by FH 
#last edit in 20191127
#for Yuqing, for detecting RF of mouse 
#15 vertal bar, 15 horizatial bar, 5 repeats
#cancel the white screen

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.80.03), 2019_11_13_2202
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions

# Store info about the experiment session
expName = 'RF_longbar'  # from the Builder filename that created this script
expInfo = {'participant':'', 'session':'001'}
#dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
#if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName



# Setup filename for saving
filename = 'data/%s_%s_%s' %(expInfo['participant'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=None,
    savePickle=True, saveWideText=True,
    dataFileName=filename)
#save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp

# Start Code - component code to be run before the window creation



vertical_position = [[-28,0],[-24,0],[-20,0],[-16,0],[-12,0],[-8,0],[-4,0],[0,0],[4,0],[8,0],[12,0],[16,0],[20,0],[24,0],[28,0]]
horizontal_position = [[0,-28],[0,-24],[0,-20],[0,-16],[0,-12],[0,-8],[0,-4],[0,0],[0,4],[0,8],[0,12],[0,16],[0,20],[0,24],[0,28]]

# Setup the Window
win = visual.Window(size=(2560, 1600), screen=1, allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    )
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win.getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')

# Initialize components for Routine "vertical"
verticalClock = core.Clock()
verticalbar = visual.Rect(win=win, name='verticalbar',units=u'deg', 
    width=[4, 40][0], height=[4, 40][1],
    ori=0, pos=[0,0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace=u'rgb',
    fillColor=[1,1,1], fillColorSpace=u'rgb',
    opacity=1,interpolate=True)
# Initialize components for Routine "horizatial"
horizatialClock = core.Clock()
horizontalbar = visual.Rect(win=win, name='horizontalbar',units=u'deg', 
    width=[100, 4][0], height=[100, 4][1],
    ori=0, pos=[0,0],
    lineWidth=1, lineColor=[1,1,1], lineColorSpace=u'rgb',
    fillColor=[1,1,1], fillColorSpace=u'rgb',
    opacity=1,interpolate=True)
# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

#------Prepare to start Routine "trial"-------
t = 0
trialClock.reset()  # clock 
frameN = -1
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
trialComponents = []
trialComponents.append(ISI)
for thisComponent in trialComponents:
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED

#-------Start Routine "trial"-------
continueRoutine = True
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = trialClock.getTime()
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    # *ISI* period
    if t >= 0.0 and ISI.status == NOT_STARTED:
        # keep track of start time/frame for later
        ISI.tStart = t  # underestimates by a little under one frame
        ISI.frameNStart = frameN  # exact frame index
        ISI.start(5)
    elif ISI.status == STARTED: #one frame should pass before updating params and completing
        ISI.complete() #finish the static period
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        routineTimer.reset()  # if we abort early the non-slip timer needs reset
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # check for quit (the Esc key)
    if endExpNow or event.getKeys(keyList=["escape"]):
        core.quit()
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

#-------Ending Routine "trial"-------
for thisComponent in trialComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=4, method=u'sequential', 
    extraInfo=expInfo, originPath=None,
    trialList=[None],
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    # set up handler to look after randomisation of conditions etc
    vertical_repeat = data.TrialHandler(nReps=15, method=u'random', 
        extraInfo=expInfo, originPath=None,
        trialList=[None],
        seed=None, name='vertical_repeat')
    thisExp.addLoop(vertical_repeat)  # add the loop to the experiment
    thisVertical_repeat = vertical_repeat.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisVertical_repeat.rgb)
    if thisVertical_repeat != None:
        for paramName in thisVertical_repeat.keys():
            exec(paramName + '= thisVertical_repeat.' + paramName)
    
    
    count=-1 
    for thisVertical_repeat in vertical_repeat:
        count+=1
        currentLoop = vertical_repeat
        # abbreviate parameter names if possible (e.g. rgb = thisVertical_repeat.rgb)
        if thisVertical_repeat != None:
            for paramName in thisVertical_repeat.keys():
                exec(paramName + '= thisVertical_repeat.' + paramName)
        
        #------Prepare to start Routine "vertical"-------
        t = 0
        verticalClock.reset()  # clock 
        frameN = -1
        routineTimer.add(16.000000)
        # update component parameters for each repeat
        verticalbar.setPos(vertical_position[count])
        # keep track of which components have finished
        verticalComponents = []
        verticalComponents.append(verticalbar)
        for thisComponent in verticalComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "vertical"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = verticalClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *verticalbar* updates
            if t >= 15 and verticalbar.status == NOT_STARTED:
                # keep track of start time/frame for later
                verticalbar.tStart = t  # underestimates by a little under one frame
                verticalbar.frameNStart = frameN  # exact frame index
                verticalbar.setAutoDraw(True)
            elif verticalbar.status == STARTED and t >= (5 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left
                verticalbar.setAutoDraw(False)
                
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in verticalComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "vertical"-------
        for thisComponent in verticalComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.nextEntry()
        
    # completed 15 repeats of 'vertical_repeat'
    
    
    # set up handler to look after randomisation of conditions etc
    horizontal_repeat = data.TrialHandler(nReps=15, method=u'random', 
        extraInfo=expInfo, originPath=None,
        trialList=[None],
        seed=None, name='horizontal_repeat')
    thisExp.addLoop(horizontal_repeat)  # add the loop to the experiment
    thisHorizontal_repeat = horizontal_repeat.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb=thisHorizontal_repeat.rgb)
    if thisHorizontal_repeat != None:
        for paramName in thisHorizontal_repeat.keys():
            exec(paramName + '= thisHorizontal_repeat.' + paramName)
    
    
    
    count = -1
    for thisHorizontal_repeat in horizontal_repeat:
        count+=1
        currentLoop = horizontal_repeat
        # abbreviate parameter names if possible (e.g. rgb = thisHorizontal_repeat.rgb)
        if thisHorizontal_repeat != None:
            for paramName in thisHorizontal_repeat.keys():
                exec(paramName + '= thisHorizontal_repeat.' + paramName)
        
        #------Prepare to start Routine "horizatial"-------
        t = 0
        horizatialClock.reset()  # clock 
        frameN = -1
        routineTimer.add(16.000000)
        # update component parameters for each repeat
        horizontalbar.setPos(horizontal_position[count])
        # keep track of which components have finished
        horizatialComponents = []
        horizatialComponents.append(horizontalbar)
        for thisComponent in horizatialComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        
        #-------Start Routine "horizatial"-------
        continueRoutine = True
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = horizatialClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *horizontalbar* updates
            if t >= 15 and horizontalbar.status == NOT_STARTED:
                # keep track of start time/frame for later
                horizontalbar.tStart = t  # underestimates by a little under one frame
                horizontalbar.frameNStart = frameN  # exact frame index
                horizontalbar.setAutoDraw(True)
            elif horizontalbar.status == STARTED and t >= (5 + (1-win.monitorFramePeriod*0.75)): #most of one frame period left   #0.0  1.0
                horizontalbar.setAutoDraw(False)
                
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                routineTimer.reset()  # if we abort early the non-slip timer needs reset
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in horizatialComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        #-------Ending Routine "horizatial"-------
        for thisComponent in horizatialComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        thisExp.nextEntry()
        
    # completed 15 repeats of 'horizontal_repeat'
    
    thisExp.nextEntry()
    
# completed 5 repeats of 'trials'

win.close()
core.quit()
