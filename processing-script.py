"""
Model exported as python.
Name : model
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


class Model(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterRasterLayer('raster', 'raster', defaultValue=None))
        self.addParameter(QgsProcessingParameterVectorDestination('Counter', 'counter', type=QgsProcessing.TypeVectorLine, createByDefault=True, defaultValue=None))
        self.addParameter(QgsProcessingParameterRasterDestination('Hillshaded', 'Hillshaded', createByDefault=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(2, model_feedback)
        results = {}
        outputs = {}

        # Hillshade
        alg_params = {
            'AZIMUTH': 300,
            'INPUT': parameters['raster'],
            'V_ANGLE': 40,
            'Z_FACTOR': 1,
            'OUTPUT': parameters['Hillshaded']
        }
        outputs['Hillshade'] = processing.run('native:hillshade', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Hillshaded'] = outputs['Hillshade']['OUTPUT']

        feedback.setCurrentStep(1)
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
            'OUTPUT': parameters['Counter']
        }
        outputs['Contour'] = processing.run('gdal:contour', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Counter'] = outputs['Contour']['OUTPUT']
        return results

    def name(self):
        return 'model'

    def displayName(self):
        return 'model'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Model()
