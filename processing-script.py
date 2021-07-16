"""
Model exported as python.
Name : secondattempt
Group : 
With QGIS : 31607
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterRasterLayer
from qgis.core import QgsProcessingParameterVectorDestination
from qgis.core import QgsProcessingParameterRasterDestination
import processing

#Run after creating directories

class Secondattempt(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('rasterinput', 'raster_input', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Contour', 'contour', type=QgsProcessing.TypeVectorLine, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Hill', 'hill', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
        results = {}
        outputs = {}

        # Create Hillshade directory
        alg_params = {
            'PATH': 'C:/Users/Dell/Desktop/Hillshade'
        }
        outputs['CreateHillshadeDirectory'] = processing.run('native:createdirectory', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Hillshade
        alg_params = {
            'AZIMUTH': 300,
            'INPUT': parameters['rasterinput'],
            'V_ANGLE': 40,
            'Z_FACTOR': 1,
            'OUTPUT': parameters['Hill']
        }
        outputs['Hillshade'] = processing.run('native:hillshade', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Hill'] = outputs['Hillshade']['OUTPUT']

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Contour
        alg_params = {
            'PATH': 'C:/Users/Dell/Desktop/Contour'
        }
        outputs['Contour'] = processing.run('native:createdirectory', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Contour
        alg_params = {
            'BAND': 1,
            'CREATE_3D': False,
            'EXTRA': '',
            'FIELD_NAME': 'ELEV',
            'IGNORE_NODATA': False,
            'INPUT': outputs['Hillshade']['OUTPUT'],
            'INTERVAL': 10,
            'NODATA': None,
            'OFFSET': 0,
            'OUTPUT': parameters['Contour']
        }
        outputs['Contour'] = processing.run('gdal:contour', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Contour'] = outputs['Contour']['OUTPUT']
        return results

    def name(self):
        return 'secondattempt'

    def displayName(self):
        return 'secondattempt'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Secondattempt()
