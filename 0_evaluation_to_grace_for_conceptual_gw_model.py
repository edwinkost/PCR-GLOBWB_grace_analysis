#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys

# pcraster dynamic framework is used:
from pcraster.framework import DynamicFramework

from grace_evaluation import GraceEvaluation

# time object
from currTimeStep import ModelTime

# utility module
import virtualOS as vos

# input files:
input_files = {}
#
# - total thickness of water storage, from PCR-GLOBWB - unit: m
model_output_folder                                          = "/scratch/depfg/sutan101/pcrglobwb_gmd_paper/05min/netcdf/monthly/"
input_files["model_total_water_storage"]                     = model_output_folder + 'totalWaterStorageThickness_monthAvg_output_1958-01-31_to_2015-12-31.zip.nc'               # unit: meter
input_files["model_total_water_storage_variable_name"]       = "total_thickness_of_water_storage"
#
# - cell area for the model (unit: m2, depending on PCR-GLOBWB resolution)
input_files["model_cell_area"]                               = '/scratch/depfg/sutan101/data/pcrglobwb2_input_release/version_2019_11_beta_extended/pcrglobwb2_input/global_05min/routing/ldd_and_cell_area/cellsize05min.correct.map' 
#
# - catchment/basin/aquifer classification  
# ~ input_files["basin"]                                     = '/scratch-shared/edwinhs/basin_for_grace_evaluation/catchment_group_final.map' 
# - using aquifer class map
input_files["basin"]                                         = '/scratch/depfg/sutan101/data/processing_whymap/version_19september2014/major_aquifer_30min.extended.map' 
#                                                            
# - grace input files (must be resampled first to the PCR-GLOBWB resolution and its latitutde orientation must be consistent to the PCR-GLOBWB's) - unit: cm                                    
input_files["grace_total_water_storage_original"]            = '/scratch/depfg/sutan101/data/observation_data/grace_data_downloaded_29aug2017/jpl_global_mascons/CRI/edwin-netcdf-05min/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.edwin.05min.nc'
input_files["grace_scale_factor"]                            = '/scratch/depfg/sutan101/data/observation_data/grace_data_downloaded_29aug2017/jpl_global_mascons/CRI/edwin-netcdf-05min/CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.edwin.05min.nc'

input_files["grace_total_water_storage_original"]            = '/scratch/depfg/sutan101/validation_for_gw_conceptual_model/grace_data_used/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_05min.nc'
input_files["grace_scale_factor"]                            = '/scratch/depfg/sutan101/validation_for_gw_conceptual_model/grace_data_used/CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01_05min.nc'

# ~ sutan101@gpu040.cluster:/scratch/depfg/sutan101/validation_for_gw_conceptual_model/grace_data_used$ ls -lah
# ~ total 23G
# ~ drwxr-xr-x 2 sutan101 depfg    8 Nov 13 12:00 .
# ~ drwxr-xr-x 4 sutan101 depfg    2 Nov 13 11:54 ..
# ~ -rwxr-xr-x 1 sutan101 depfg 2.0M Aug 29  2017 CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.nc
# ~ -rw-r--r-- 1 sutan101 depfg  72M Nov 13 11:58 CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01_05min.nc
# ~ -rwxr-xr-x 1 sutan101 depfg 629M Aug 29  2017 GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.nc
# ~ -rw-r--r-- 1 sutan101 depfg  23G Nov 13 12:05 GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_05min.nc
# ~ -rw-r--r-- 1 sutan101 depfg  108 Nov 13 11:55 SOURCE.TXT
# ~ -rwxr-xr-x 1 sutan101 depfg  36M Nov 11  2019 cellsize05min.correct.map
# ~ -rw-r--r-- 1 sutan101 depfg  36M Nov 14  2019 cellsize05min.correct.nc
# ~ -rw-r--r-- 1 sutan101 depfg  330 Nov 13 11:57 griddes_cellsize05min.correct.nc.txt

                                                             
# output files:                                              
output_files = {}                                            
output_files['output_folder']                                = "/scratch/depfg/sutan101/grace_analysis/"
cleanOutputFolder = True                                     
#                                                            
output_files['originalscale_original_value'] = {}            
output_files['originalscale_original_value']['model']        = output_files['output_folder'] + "model_tws.nc" 
output_files['originalscale_original_value']['grace']        = output_files['output_folder'] + "grace_tws.nc"
#                                                            
output_files['originalscale_month_anomaly'] = {}            
output_files['originalscale_month_anomaly']['model']         = output_files['output_folder'] + "model_tws_month_anomaly.nc" 
output_files['originalscale_month_anomaly']['grace']         = output_files['output_folder'] + "grace_tws_month_anomaly.nc"
#
output_files['originalscale_annua_anomaly'] = {}            
output_files['originalscale_annua_anomaly']['model']         = output_files['output_folder'] + "model_tws_annua_anomaly.nc" 
output_files['originalscale_annua_anomaly']['grace']         = output_files['output_folder'] + "grace_tws_annua_anomaly.nc"
#
output_files['basinscale_tws_month_anomaly'] = {}            
output_files['basinscale_tws_month_anomaly']['model']        = output_files['output_folder'] + "model_tws_at_basinscale_month_anomaly.nc" 
output_files['basinscale_tws_month_anomaly']['grace']        = output_files['output_folder'] + "grace_tws_at_basinscale_month_anomaly.nc"
#                                                                                              
output_files['basinscale_tws_annua_anomaly'] = {}                                              
output_files['basinscale_tws_annua_anomaly']['model']        = output_files['output_folder'] + "model_tws_at_basinscale_annua_anomaly.nc"
output_files['basinscale_tws_annua_anomaly']['grace']        = output_files['output_folder'] + "grace_tws_at_basinscale_annua_anomaly.nc"
#                                                            
output_files['basinscale_month_analyses'] = {}                                                  
output_files['basinscale_month_analyses']['bias']            = output_files['output_folder'] + "basinscale_month_bias.nc"
output_files['basinscale_month_analyses']['mae' ]            = output_files['output_folder'] + "basinscale_month_mae.nc"
output_files['basinscale_month_analyses']['correlation']     = output_files['output_folder'] + "basinscale_month_correlation.nc"
output_files['basinscale_month_analyses']['rel_iqtil_error'] = output_files['output_folder'] + "basinscale_month_rel_iqtil_error.nc"
output_files['basinscale_month_analyses']['relative_mae']    = output_files['output_folder'] + "basinscale_month_relative_mae.nc"
#                                                                                                     
output_files['basinscale_annua_analyses'] = {}                                                        
output_files['basinscale_annua_analyses']['bias']            = output_files['output_folder'] + "basinscale_annua_bias.nc"
output_files['basinscale_annua_analyses']['mae' ]            = output_files['output_folder'] + "basinscale_annua_mae.nc"
output_files['basinscale_annua_analyses']['correlation']     = output_files['output_folder'] + "basinscale_annua_correlation.nc"
output_files['basinscale_annua_analyses']['rel_iqtil_error'] = output_files['output_folder'] + "basinscale_annua_rel_iqtil_error.nc"
output_files['basinscale_annua_analyses']['relative_mae']    = output_files['output_folder'] + "basinscale_annua_relative_mae.nc"
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
    endDate   = "2015-12-31" #YYYY-MM-DD
    
    # time object
    modelTime = ModelTime() # timeStep info: year, month, day, doy, hour, etc
    modelTime.getStartEndTimeSteps(startDate,endDate)

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
