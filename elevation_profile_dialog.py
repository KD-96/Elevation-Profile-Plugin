import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets

import processing
import matplotlib.pyplot as plt
from qgis.core import QgsVectorLayer,QgsDistanceArea
import time

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'elevation_profile_dialog_base.ui'))

class ElevationProfileDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(ElevationProfileDialog, self).__init__(parent)

        self.setupUi(self)
        self.pb1.clicked.connect(self.Run)
        self.pb2.clicked.connect(self.CloseWindow)
        self.progressBar.setValue(0)

###################################
###         Main Program        ###
###################################
    def Run(self):
        print('Programe trigered')

# inputs
        dem = self.MapLayer1.currentLayer()
        points = self.MapLayer2.currentLayer()
        intvl = self.spBox.value()
        point_interval = intvl / 110500 # convert to meters 


        ## message for wrong files -to do


        results = processing.run("qgis:pointstopath", {'INPUT':points,'CLOSE_PATH':False,'ORDER_FIELD':'id','GROUP_FIELD':'','DATE_FORMAT':'','OUTPUT':'TEMPORARY_OUTPUT'})
        line = results['OUTPUT']
        self.progressBar.setValue(10)

        results = processing.run("native:pointsalonglines", {'INPUT':line,'DISTANCE':point_interval,'START_OFFSET':0,'END_OFFSET':0,'OUTPUT':'TEMPORARY_OUTPUT'})
        line_points = results['OUTPUT']
        self.progressBar.setValue(50)

        results = processing.runAndLoadResults("saga:addrastervaluestopoints", {'SHAPES':line_points,'GRIDS':[dem],'RESAMPLING':0,'RESULT':'TEMPORARY_OUTPUT'})
        points_z = results['RESULT'] 
        self.progressBar.setValue(60)

# getting elevations from point layer
        z_layer=QgsVectorLayer(points_z,'ogr')

        features=z_layer.getFeatures()
        first_feat=next(features)
        first_point=first_feat.geometry().asPoint()
        first_z=first_feat.attributes()[-1]
        self.progressBar.setValue(70)

# lists initialize for plot graph
        point_dict={'from':'','to':''}
        point_dict['from']=first_point
        list_distance=[0]
        z_list=[first_z]

# initialize distance calculator
        d=QgsDistanceArea()
        d.setEllipsoid('WGS84')

# getting information for plot the graph
        for f in features:
            z=f.attributes()[-1]
            z_list.append(z)
            xy_to=f.geometry().asPoint()
            point_dict['to']=xy_to
            distance=d.measureLine(point_dict['from'],point_dict['to'])
            segment_line=distance+list_distance[-1]
            list_distance.append(segment_line)
            point_dict['from']=point_dict['to']
        
        self.progressBar.setValue(50)

# plot the graph
        min_z=round(min(z_list),3)
        max_z=round(max(z_list),3)
        mean_z=round(sum(z_list)/len(z_list),3)
        d_max=list_distance[-1]
        plt.figure(figsize=(10,4))
        plt.plot(list_distance,z_list)
        plt.plot([0,d_max],[min_z,min_z],'g--',label='Min. : '+str(min_z))
        plt.plot([0,d_max],[max_z,max_z],'r--',label='Max. : '+str(max_z))
        plt.plot([0,d_max],[mean_z,mean_z],'y--',label='Mean : '+str(mean_z))
        plt.grid()
        plt.legend(loc=1)
        plt.xlabel("Distance(ft)")
        plt.ylabel("Elevation(ft)")
        plt.fill_between(list_distance,z_list,min_z,alpha=0.1)
        plt.show()

        self.progressBar.setValue(100)
        time.sleep(1)
        self.progressBar.reset()

###################################
###    Terminate the program    ###
###################################
    def CloseWindow(self):
        print('closing window')
        self.progressBar.setValue(100)
        self.close()
