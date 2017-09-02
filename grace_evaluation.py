#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import datetime
import calendar

import pcraster as pcr
from pcraster.framework import DynamicModel

from outputNetcdf import OutputNetcdf
import virtualOS as vos

class GraceEvaluation(DynamicModel):

    def __init__(self, input_files,\
                       output_files,\
                       modelTime,\
                       main_tmp_dir = "/dev/shm/"):
        DynamicModel.__init__(self) 

        self.input_files  = input_files
        self.output_files = output_files 

        self.modelTime = modelTime

        # main temporary directory 
        self.main_tmp_dir = main_tmp_dir+"/"+vos.get_random_word()
        # make the temporary directory if not exist yet 
        try: 
            os.makedirs(self.main_tmp_dir)
        except:
            os.system('rm -r '+str(self.main_tmp_dir)+'*')
            os.makedirs(self.main_tmp_dir)

        # clone map for pcraster process - depend on the resolution of PCR-GLOBWB model
        pcr.setclone(self.input_files["model_cell_area"]) 
        self.clone_map = pcr.boolean(1.0)
        #
        # catchment id map
        self.catchment = pcr.nominal(\
                         pcr.readmap(self.input_files["basin"]))
        self.catchment = pcr.ifthen(pcr.scalar(self.catchment) > 0.0,\
                                    self.catchment)
        # cell area map
        self.cell_area = pcr.cover(pcr.readmap(self.input_files["model_cell_area"]), 0.0)
        self.cell_area = pcr.ifthen(pcr.defined(self.catchment), self.catchment)
        
        # prepare model monthly and annual anomaly time series
        self.pre_process_model_file()

        # prepare grace monthly and annual anomaly time series
        self.pre_process_grace_file("scale_factor")

        # prepare object for writing netcdf files:
        self.output = OutputNetcdf(self.input_files["model_cell_area"])
        self.output.createNetCDF(self.output_files['basinscale_tws_month_anomaly']['grace'], "lwe_thickness", "m")
        self.output.createNetCDF(self.output_files['basinscale_tws_month_anomaly']['model'], "pcrglobwb_tws", "m")
        self.output.createNetCDF(self.output_files['basinscale_tws_annua_anomaly']['grace'], "lwe_thickness", "m")
        self.output.createNetCDF(self.output_files['basinscale_tws_annua_anomaly']['model'], "pcrglobwb_tws", "m")

    def pre_process_grace_file(self, variable_name_for_scale_factor = "SCALE_FACTOR"): 
        
        # using the scale factor to correct the original monthly grace file and use only the selected years
        # - input files - unit: cm
        grace_file  = self.input_files["grace_total_water_storage_original"]
        scale_file  = self.input_files["grace_scale_factor"]                
        # - period of interest 
        start_year  = str(self.modelTime.startTime.year)
        end_year    =   str(self.modelTime.endTime.year)
        # - output file - unit: m
        output_file = self.output_files['originalscale_original_value']['grace'] 
        #
        print("\n")
        print("Using the given factor to scale the original GRACE time series and focusing on the selected years only.")
        cdo_command = "cdo -L setunit,m -invertlat -selyear,"+str(start_year)+"/"+str(end_year)+\
                      " -sellonlatbox,-180,180,-90,90"+\
                      " -mulc,0.01"+\
                      " -mul -selname,lwe_thickness "+str(grace_file)+\
                      " -selname," + str(variable_name_for_scale_factor) + " " + str(scale_file)+\
                      " "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n") 
        
        # calculate monthly anomaly:  
        input_file  = self.output_files['originalscale_original_value']['grace']
        output_file = self.output_files['originalscale_month_anomaly' ]['grace']
        print("\n")
        print("Calculate the monthly anomaly time series of GRACE.")
        cdo_command = "cdo -L sub "+str(input_file)+" -timmean"+" "+str(input_file)+" "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n") 

    def pre_process_model_file(self): 
        
        # focusing on the selected years only
        # - input fils - unit: m
        input_file  = self.input_files["model_total_water_storage"]
        # - period of interest 
        start_year  = str(self.modelTime.startTime.year)
        end_year    =   str(self.modelTime.endTime.year)
        # - output file - unit: m
        output_file = self.output_files['originalscale_original_value']['model'] 
        print("\n")
        print("Using only the selected years of PCR-GLOBWB time series.")
        cdo_command = "cdo -L selyear,"+str(start_year)+"/"+str(end_year)+\
                      " "+ str(input_file) +\
                      " "+ str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n") 

        # calculate monthly anomaly:
        input_file  = self.output_files['originalscale_original_value']['model']
        output_file = self.output_files['originalscale_month_anomaly' ]['model']
        print("\n")
        print("Calculate the monthly anomaly time series of PCR-GLOBWB.")
        cdo_command = "cdo -L sub "+str(input_file)+" -timmean"+" "+str(input_file)+" "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n") 
 
    def initial(self): 
        pass

    def dynamic(self):
        
        # re-calculate model time using current pcraster timestep value
        self.modelTime.update(self.currentTimeStep())

        # at the end of every month:
        # - aggregate/average the value at basin scale:
        # - then report it to the netcdf file:
        if self.modelTime.endMonth == True:

            # values from grace:
            print("Upscaling GRACE to the basin resolution.")
            grace_value = pcr.cover(vos.netcdf2PCRobjClone(\
                          self.output_files['originalscale_month_anomaly']['grace'],\
                          "lwe_thickness",\
                          str(self.modelTime.fulldate), "mid-month",\
                          self.input_files["model_cell_area"]), 0.0)
            grace_value = pcr.ifthen(pcr.defined(self.catchment), grace_value)
            #
            basin_grace = pcr.areatotal(self.cell_area * grace_value, self.catchment)/\
                          pcr.areatotal(self.cell_area, self.catchment)

            # values from pcr-globwb simulation:
            print("Upscaling PCR-GLOBWB to the basin resolution.")
            model_value = pcr.cover(vos.netcdf2PCRobjClone(\
                          self.output_files['originalscale_month_anomaly']['model'],\
                          "pcrglobwb_tws",\
                          str(self.modelTime.fulldate), "end-month",\
                          self.input_files["model_cell_area"]), 0.0)
            model_value = pcr.ifthen(pcr.defined(self.catchment), model_value)
            #
            basin_model = pcr.areatotal(self.cell_area * model_value, self.catchment)/\
                          pcr.areatotal(self.cell_area, self.catchment)

            # reporting
            timeStamp = datetime.datetime(self.modelTime.year,\
                                          self.modelTime.month,\
                                          self.modelTime.day,0)
            # write grace 
            self.output.data2NetCDF(self.output_files["basinscale_tws_month_anomaly"]['grace'],\
                                    "lwe_thickness",\
                                    pcr.pcr2numpy(basin_grace,vos.MV),\
                                    timeStamp)
            # write model
            self.output.data2NetCDF(self.output_files["basinscale_tws_month_anomaly"]['model'],\
                                    "pcrglobwb_tws",\
                                    pcr.pcr2numpy(basin_model,vos.MV),\
                                    timeStamp)

        # at the last dynamic time step 
        # - prepare annual anomaly time series
        # - evaluate the pcr-globwb model results to grace time series (monthly and annual)
        if self.modelTime.currTime == self.modelTime.endTime:

            # prepare annual anomaly time series
            self.prepare_annual_anomaly()

            # evaluate the pcr-globwb model results to grace time series 
            # (monthly & annual resolution - basin & one degree scale)
            self.evaluate_to_grace_data()


    def prepare_annual_anomaly(self): 
        
        # calculate yearly anomaly of GRACE:  
        input_file  = self.output_files['originalscale_month_anomaly' ]['grace']
        output_file = self.output_files['originalscale_annua_anomaly' ]['grace']
        print("\n")
        print("Calculate the annual anomaly time series of GRACE.")
        cdo_command = "cdo -L yearmean "+str(input_file)+" "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n") 

        # prepare basin scale - grace - annual anomaly time series
        input_file  = self.output_files["basinscale_tws_month_anomaly"]['grace']
        output_file = self.output_files["basinscale_tws_annua_anomaly"]['grace']
        print("\n")
        cdo_command = "cdo -L yearmean "+str(input_file)+" "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n") 

        # calculate yearly anomaly of PCR-GLOBWB:  
        input_file  = self.output_files['originalscale_month_anomaly' ]['model']
        output_file = self.output_files['originalscale_annua_anomaly' ]['model']
        print("\n")
        print("Calculate the annual anomaly time series of PCR-GLOBWB.")
        cdo_command = "cdo -L yearmean "+str(input_file)+" "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n") 

        # prepare basin scale - model - annual anomaly time series
        input_file  = self.output_files["basinscale_tws_month_anomaly"]['model']
        output_file = self.output_files["basinscale_tws_annua_anomaly"]['model']
        print("\n")
        cdo_command = "cdo -L yearmean "+str(input_file)+" "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n") 


    def evaluate_to_grace_data(self): 

        # basin and monthly resolution
        print("\n")
        print("Evaluate the MONTHLY time series at the basin resolution.")
        self.evaluation(self.output_files['basinscale_tws_month_anomaly']['model'],\
                        self.output_files['basinscale_tws_month_anomaly']['grace'],\
                           self.output_files['basinscale_month_analyses'])

        # basin and annual resolution
        print("\n")
        print("Evaluate the ANNUAL time series at the basin resolution.")
        self.evaluation(self.output_files['basinscale_tws_annua_anomaly']['model'],\
                        self.output_files['basinscale_tws_annua_anomaly']['grace'],\
                           self.output_files['basinscale_annua_analyses'])

    def evaluation(self,model_file,grace_file,output_files): 

        # bias
        output_file = output_files['bias']
        print("\n")
        cdo_command = "cdo -L sub -timmean "+str(model_file)+" -timmean "+str(grace_file)+" "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n") 

        # mae
        output_file = output_files['mae']
        print("\n")
        cdo_command = "cdo -L timmean -abs -sub "+str(model_file)+" "+str(grace_file)+" "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n")

        # correlation
        output_file = output_files['correlation']
        print("\n")
        cdo_command = "cdo -L setunit,1 -timcor "+str(grace_file)+" "+str(model_file)+" "+str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n")
        
        # relative interquantile range error
        model_range_file = output_files['rel_iqtil_error']+".inter_qtile.model.nc"
        print("\n")
        cdo_command = "cdo -L sub "+\
                      "-timpctl,95 "+str(model_file)+" "+\
                      "-timmin "    +str(model_file)+" "+\
                      "-timmax "    +str(model_file)+" "+\
                      "-timpctl,5  "+str(model_file)+" "+\
                      "-timmin "    +str(model_file)+" "+\
                      "-timmax "    +str(model_file)+" "+model_range_file
        print(cdo_command); os.system(cdo_command); print("\n")
        grace_range_file = output_files['rel_iqtil_error']+".inter_qtile.grace.nc"
        cdo_command = "cdo -L sub "+\
                      "-timpctl,95 "+str(grace_file)+" "+\
                      "-timmin "    +str(grace_file)+" "+\
                      "-timmax "    +str(grace_file)+" "+\
                      "-timpctl,5  "+str(grace_file)+" "+\
                      "-timmin "    +str(grace_file)+" "+\
                      "-timmax "    +str(grace_file)+" "+grace_range_file
        print(cdo_command); os.system(cdo_command); print("\n")
        output_file = output_files['rel_iqtil_error']
        print("\n")
        cdo_command = "cdo -L setunit,1 -div "+\
                      "-sub "+model_range_file+" "+grace_range_file+" "+\
                      " "+grace_range_file+" "+output_file
        print(cdo_command); os.system(cdo_command); print("\n")

        # relative mae
        mae_file = output_files['mae']
        grace_range_file = output_files['rel_iqtil_error']+".inter_qtile.grace.nc"
        output_file = output_files['relative_mae']
        print("\n")
        cdo_command = "cdo -L div "+\
                      str(mae_file)+" "+\
                      str(grace_range_file)+" "+\
                      str(output_file)
        print(cdo_command); os.system(cdo_command); print("\n")
