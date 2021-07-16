"""
Model exported as python.
Name : directories
Group : 
With QGIS : 31607
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
import processing

"""
 Change C:/Users/Dell/Desktop/ProjName into the location of your project results directory
"""

class Directories(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        pass

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Rasters
        alg_params = {
            'PATH': 'C:/Users/Dell/Desktop/ProjName/Hillshade'
        }
        outputs['Rasters'] = processing.run('native:createdirectory', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Contour
        alg_params = {
            'PATH': 'C:/Users/Dell/Desktop/ProjName/Contour'
        }
        outputs['Contour'] = processing.run('native:createdirectory', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'directories'

    def displayName(self):
        return 'directories'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Directories()
