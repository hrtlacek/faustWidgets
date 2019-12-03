#!/usr/bin/env python
#title           : faustWidgets.py
#description     : create jupyter Widgets from faust code using FAUSTpy.
#author          : Patrik Lechner <ptrk.lechner@gmail.com>
#date            : Nov 2019
#version         : 0.1
#usage           :
#notes           :
#python_version  : 3.6.3 | packaged by conda-forge | (default, Oct  5 2017, 14:07:33) \n[GCC 4.8.2 20140120 (Red Hat 4.8.2-15)]'
#=======================================================================

import ipywidgets as widgets
import matplotlib.pyplot as plt
import FAUSTPy
import numpy as np

def __faustObjToParamDicts(faustObject):
    """Takes a FAUSTpy.FAUST object and extracts its parameters. 

    Arguments:
        faustObject {FAUSTpy.FAUST} -- [description]
    
    Returns:
        [list] -- a list of dictionaries containing information for each param.
    """
    objName = faustObject.dsp.metadata[b'name'].decode()
    params = []
    for member in dir(eval('faustObject.dsp.b_' + objName)):
        if 'p_' in member:
            paramName = member

            vMin = eval('faustObject.dsp.b_' + objName + '.' + paramName +
                        '.min')
            vMax = eval('faustObject.dsp.b_' + objName + '.' + paramName +
                        '.max')
            vStep = eval('faustObject.dsp.b_' + objName + '.' + paramName +
                         '.step')
            vDefault = eval('faustObject.dsp.b_' + objName + '.' + paramName +
                            '.default')
            params.append({
                'name': paramName,
                'min': vMin,
                'max': vMax,
                'step': vStep,
                'default': vDefault
            })
    return params


def __paramDictsToSliders(params):
    sliders = []
    for paramDict in params:
        sliders.append(
            widgets.FloatSlider(
                value=paramDict['default'],
                min=paramDict['min'],
                max=paramDict['max'],
                step=paramDict['step'],
                description=paramDict['name'],
                continuous_update=True,
                orientation='horizontal',
                readout=True,
                readout_format='.1f', ))
    return sliders



def __valChangeCallback(change):
    """The callback function for the GUI changes. For now calls the faust Program and produces a short timedomain  plot.
    
    Arguments:
        change {[type]} -- [description]
    """

    with guiOut:
        for par in thisUI.children:
            name = par.description
            faustPar = eval('thisfaustObject.dsp.b_' + thisObjName + '.' +
                            name)
            faustPar.zone = par.value
            # print(faustPar.zone)
        if type(xIn) != type(None):
            op = thisfaustObject.compute(xIn)
        else:
            op = thisfaustObject.compute(numSamps)
        plotFunction(op.T)
    guiOut.clear_output(wait=True)

    return

def simplePlot(x):
    plt.plot(x)
    plt.ylim([-1, 1])
    plt.grid()
    plt.show()
    return


def getWidgets(faustObject, x = None, plotFun=None, nSamps=100):
    """Main Function. Pass in FAUSTpy.FAUST object and get a Jupyter widget-GUI and a simple plot.
    
    Arguments:
        faustObject {[type]} -- [description]
    
    Keyword Arguments:
        x {[np.array]} -- [inout array for dsp effect] (default: {None})
        plotFun {[callable]} -- [plot function taking one argument which is the array to be plotted] (default: {None})
        nSamps {int} -- [number of samples to compute for a dsp synth] (default: {100})
    """


    # All these globals are a bit ugly but seem necessary to get data into the callback.
    # Maybe pack them into a single global class or dictionary.

    global thisfaustObject
    global thisObjName
    global thisUI
    global guiOut
    global plotFunction
    global numSamps
    global xIn

    numSamps = nSamps
    if type(x) != type(None):
        xIn = x.astype(np.float32)

    if type(plotFun)==type(None):
        plotFunction = simplePlot
    else:
        plotFunction = plotFun
    guiOut = widgets.Output()

    thisfaustObject = faustObject
    thisObjName = faustObject.dsp.metadata[b'name'].decode()

    params = __faustObjToParamDicts(faustObject)
    sliders = __paramDictsToSliders(params)
    thisUI = widgets.HBox(sliders)



    guiOut = widgets.Output()
    for child in thisUI.children:
        child.unobserve_all()
        child.observe(__valChangeCallback, names='value')

    display(thisUI, guiOut)

    return
