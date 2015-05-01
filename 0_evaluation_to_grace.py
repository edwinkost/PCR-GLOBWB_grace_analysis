#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# pcraster dynamic framework is used:
from pcraster.framework import DynamicFramework

# classes used in this script
from dynamic_upscaling_framework import UpscalingFramework
from grace_evaluation import GraceEvaluation

# time object
from currTimeStep import ModelTime

# utility module:git@github.com:edwinkost/PCR-GLOBWB_grace_analysis.git
import virtualOS as vos

# input files:
input_files = {}
#
# - total thickness of water storage, from PCR-GLOBWB
#~ model_output_folder                                       = '/scratch/edwin/05min_runs_results/2015-03-27_and_2015-04-01/non-natural_2015-03-27/global/'
model_output_folder                                          = '/projects/0/wtrcycle/users/edwinhs/05min_runs/27april2015/non_natural/global/'
input_files["model_total_water_storage"]                     = model_output_folder+'/netcdf/totalWaterStorageThickness_monthAvg_output_2000to2010.nc'               # unit: meter
input_files["model_total_water_storage_variable_name"]       = "total_thickness_of_water_storage"
#
# - cell area for the model (unit: m2, depending on PCR-GLOBWB resolution)
input_files["model_cell_area"]                               = '/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map' 
#~ input_files["model_cell_area"]                            = '/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input30min/routing/cellarea30min.map' 
#
# - catchment/basin/aquifer classification (please provide the input map in a 30 arc-minute resolution)  
#~ input_files["basin30minmap"]                              = '/home/edwinhs/data/basin_and_grace_from_yoshi/globalcat.map' 
#~ input_files["basin30minmap"]                              = '/home/edwinhs/data/processing_whymap/version_19september2014/major_aquifer_30min.extended.map'
input_files["basin30minmap"]                                 = '/home/edwinhs/data/data_from_jt/mask_nominal_halfdegree.map'
# - cell area for the catchment/basin/aquifer classification (unit: m2, 30 arc-minute resolution)  
input_files["area30min_map"]                                 = '/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input30min/routing/cellarea30min.map' 
#                                                            
# - grace input files (unit cm, resolution: one arc-degree)                                       
input_files["grace_total_water_storage_original"]            = '/projects/0/wtrcycle/users/edwinhs/observation_data/grace/source/GRCTellus.CSR.200204_201403.LND.RL05.DSTvSCS1401.nc'   # unit: cm
input_files["grace_scale_factor"]                            = '/projects/0/wtrcycle/users/edwinhs/observation_data/grace/source/CLM4.SCALE_FACTOR.DS.G300KM.RL05.DSTvSCS1401.nc'
# - one degree cell classification (for GRACE)
input_files["one_degree_id"]                                 = '/projects/0/dfguu/data/hydroworld/others/irrigationZones/one_arc_degree/uniqueIds60min.map' 
                                                             
# output files:                                              
output_files = {}                                            
output_files['output_folder']                                = model_output_folder+"/analysis/grace/aquifer_jt/"
#~ output_files['output_folder']                             = "/scratch/edwin/05min_runs_results/2015-03-27_and_2015-04-01/non-natural_2015-04-01/global/analysis/grace/"
#~ output_files['output_folder']                             = "/scratch/edwin/test_grace/"
cleanOutputFolder = True                                     
#                                                            
output_files['one_degree_tws'] = {}                          
output_files['one_degree_tws']['model']                      = output_files['output_folder']+"model_tws_at_one_degree_month.nc"
output_files['one_degree_tws']['grace']                      = output_files['output_folder']+"grace_tws_at_one_degree_month.nc"
#                                                            
output_files['one_degree_tws_month_anomaly'] = {}            
output_files['one_degree_tws_month_anomaly']['model']        = output_files['output_folder']+"model_tws_at_one_degree_month_anomaly.nc"
output_files['one_degree_tws_month_anomaly']['grace']        = output_files['output_folder']+"grace_tws_at_one_degree_month_anomaly.nc"
#                                                            
output_files['one_degree_tws_annua_anomaly'] = {}            
output_files['one_degree_tws_annua_anomaly']['model']        = output_files['output_folder']+"model_tws_at_one_degree_annua_anomaly.nc"
output_files['one_degree_tws_annua_anomaly']['grace']        = output_files['output_folder']+"grace_tws_at_one_degree_annua_anomaly.nc"
#                                                            
output_files['basinscale_tws_month_anomaly'] = {}            
output_files['basinscale_tws_month_anomaly']['model']        = output_files['output_folder']+"model_tws_at_basinscale_month_anomaly.nc" 
output_files['basinscale_tws_month_anomaly']['grace']        = output_files['output_folder']+"grace_tws_at_basinscale_month_anomaly.nc"
#                                                            
output_files['basinscale_tws_annua_anomaly'] = {}            
output_files['basinscale_tws_annua_anomaly']['model']        = output_files['output_folder']+"model_tws_at_basinscale_annua_anomaly.nc"
output_files['basinscale_tws_annua_anomaly']['grace']        = output_files['output_folder']+"grace_tws_at_basinscale_annua_anomaly.nc"
#                                                            
output_files['one_degree_month_analyses'] = {}               
output_files['one_degree_month_analyses']['bias']            = output_files['output_folder']+"one_degree_month_bias.nc"
output_files['one_degree_month_analyses']['mae' ]            = output_files['output_folder']+"one_degree_month_mae.nc"
output_files['one_degree_month_analyses']['correlation']     = output_files['output_folder']+"one_degree_month_correlation.nc"
output_files['one_degree_month_analyses']['rel_iqtil_error'] = output_files['output_folder']+"one_degree_month_rel_iqtil_error.nc"
output_files['one_degree_month_analyses']['relative_mae']    = output_files['output_folder']+"one_degree_month_relative_mae.nc"
#                                                                                               
output_files['basinscale_month_analyses'] = {}                                                  
output_files['basinscale_month_analyses']['bias']            = output_files['output_folder']+"basinscale_month_bias.nc"
output_files['basinscale_month_analyses']['mae' ]            = output_files['output_folder']+"basinscale_month_mae.nc"
output_files['basinscale_month_analyses']['correlation']     = output_files['output_folder']+"basinscale_month_correlation.nc"
output_files['basinscale_month_analyses']['rel_iqtil_error'] = output_files['output_folder']+"basinscale_month_rel_iqtil_error.nc"
output_files['basinscale_month_analyses']['relative_mae']    = output_files['output_folder']+"basinscale_month_relative_mae.nc"
#                                                                                                     
output_files['one_degree_annua_analyses'] = {}                                                        
output_files['one_degree_annua_analyses']['bias']            = output_files['output_folder']+"one_degree_annua_bias.nc"
output_files['one_degree_annua_analyses']['mae' ]            = output_files['output_folder']+"one_degree_annua_mae.nc"
output_files['one_degree_annua_analyses']['correlation']     = output_files['output_folder']+"one_degree_annua_correlation.nc"
output_files['one_degree_annua_analyses']['rel_iqtil_error'] = output_files['output_folder']+"one_degree_annua_rel_iqtil_error.nc"
output_files['one_degree_annua_analyses']['relative_mae']    = output_files['output_folder']+"one_degree_annua_relative_mae.nc"
#                                                                                                     
output_files['basinscale_annua_analyses'] = {}                                                        
output_files['basinscale_annua_analyses']['bias']            = output_files['output_folder']+"basinscale_annua_bias.nc"
output_files['basinscale_annua_analyses']['mae' ]            = output_files['output_folder']+"basinscale_annua_mae.nc"
output_files['basinscale_annua_analyses']['correlation']     = output_files['output_folder']+"basinscale_annua_correlation.nc"
output_files['basinscale_annua_analyses']['rel_iqtil_error'] = output_files['output_folder']+"basinscale_annua_rel_iqtil_error.nc"
output_files['basinscale_annua_analyses']['relative_mae']    = output_files['output_folder']+"basinscale_annua_relative_mae.nc"
#


# make an output folder
try:
    os.makedirs(output_files['output_folder'])
    cleanOutputFolder = False
except:
    if cleanOutputFolder: 
        os.system('rm -r '+str(output_files['output_folder'])+"/*")

# make a temporary folder 
tmpDir = output_files['output_folder']+"/"+"tmp/"
try:
    os.makedirs(tmpDir)
except:
    pass

def main():
    
    startDate = "2003-01-01" #YYYY-MM-DD
    endDate   = "2010-12-31" #YYYY-MM-DD
    
    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate,endDate)
    #
    # upscaling the PCR-GLOBWB results from five minute to one degree:
    upscalingModel = UpscalingFramework(input_files,\
                                        output_files,\
                                        modelTime,\
                                        tmpDir)
    dynamic_framework = DynamicFramework(upscalingModel,\
                                         modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()

    # reset time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate,endDate)
    #
    # evaluate model results to grace product
    graceEvaluation = GraceEvaluation(input_files,\
                                      output_files,\
                                      modelTime,\
                                      tmpDir)
    dynamic_framework = DynamicFramework(graceEvaluation,\
                                         modelTime.nrOfTimeSteps)
    dynamic_framework.setQuiet(True)
    dynamic_framework.run()
                                      

if __name__ == '__main__':
    sys.exit(main())
