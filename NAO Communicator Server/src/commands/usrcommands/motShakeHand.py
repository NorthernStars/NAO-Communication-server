'''
Created on 06.01.2013

@author: hannes
'''
from settings.Settings import Settings

class motShakeHand(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        pass
        
    def initHand(self):
        # Choregraphe bezier export in Python.
        from naoqi import ALProxy
        
        names = list()
        times = list()
        keys = list()

        names.append("RElbowRoll")
        times.append([ 0.80000])
        keys.append([ [ 0.46945, [ 3, -0.26667, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        names.append("RElbowYaw")
        times.append([ 0.80000])
        keys.append([ [ 1.12438, [ 3, -0.26667, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        names.append("RHand")
        times.append([ 0.80000])
        keys.append([ [ 0.01745, [ 3, -0.26667, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        names.append("RShoulderPitch")
        times.append([ 0.80000])
        keys.append([ [ 0.39888, [ 3, -0.26667, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        names.append("RShoulderRoll")
        times.append([ 0.80000])
        keys.append([ [ -0.05220, [ 3, -0.26667, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        names.append("RWristYaw")
        times.append([ 0.80000])
        keys.append([ [ 0.08279, [ 3, -0.26667, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        try:
            motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
            motion.angleInterpolationBezier(names, times, keys);
        except BaseException, err:
            print err
            
        
    def shakeHand(self):
        from naoqi import ALProxy
        
        names = list()
        times = list()
        keys = list()

        names.append("RElbowRoll")
        times.append([ 0.48000, 1.00000, 1.48000, 2.00000, 2.48000, 3.00000])
        keys.append([ [ 0.49092, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.48785, [ 3, -0.17333, 0.00000], [ 3, 0.16000, 0.00000]], [ 0.49092, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.48939, [ 3, -0.17333, 0.00000], [ 3, 0.16000, 0.00000]], [ 0.49246, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.49092, [ 3, -0.17333, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        names.append("RElbowYaw")
        times.append([ 0.48000, 1.00000, 1.48000, 2.00000, 2.48000, 3.00000])
        keys.append([ [ 1.12438, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ 1.13512, [ 3, -0.17333, 0.00000], [ 3, 0.16000, 0.00000]], [ 1.13512, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ 1.13052, [ 3, -0.17333, 0.00239], [ 3, 0.16000, -0.00221]], [ 1.12131, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ 1.12285, [ 3, -0.17333, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        names.append("RShoulderPitch")
        times.append([ 0.48000, 1.00000, 1.48000, 2.00000, 2.48000, 3.00000])
        keys.append([ [ 0.58450, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.84528, [ 3, -0.17333, 0.00000], [ 3, 0.16000, 0.00000]], [ -0.08126, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.91277, [ 3, -0.17333, 0.00000], [ 3, 0.16000, 0.00000]], [ -0.02143, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ 0.37741, [ 3, -0.17333, 0.00000], [ 3, 0.00000, 0.00000]]])
        
        names.append("RShoulderRoll")
        times.append([ 0.48000, 1.00000, 1.48000, 2.00000, 2.48000, 3.00000])
        keys.append([ [ -0.03993, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ -0.06140, [ 3, -0.17333, 0.00000], [ 3, 0.16000, 0.00000]], [ -0.05987, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ -0.05987, [ 3, -0.17333, 0.00000], [ 3, 0.16000, 0.00000]], [ -0.06447, [ 3, -0.16000, 0.00000], [ 3, 0.17333, 0.00000]], [ -0.06294, [ 3, -0.17333, 0.00000], [ 3, 0.00000, 0.00000]]])
                
        try:
            motion = ALProxy("ALMotion", Settings.naoHostName, Settings.naoPort)
            motion.angleInterpolationBezier(names, times, keys);
        except BaseException, err:
            print err
