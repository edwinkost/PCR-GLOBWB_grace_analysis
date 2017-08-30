#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import pcraster as pcr

# make an output directory and go to there
output_directory = "/scratch-shared/edwinhs/basin_for_grace_evaluation/"
try:
    os.makedirs(output_directory) 
except:
    os.system('rm -r ' + output_directory + "/*")
os.chdir(output_directory) 

# set clone, as well as ldd, landmask and cell size maps that will be used
ldd_map_file_name                          = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map"
pcr.setclone(ldd_map_file_name)
ldd_map  = pcr.readmap(ldd_map_file_name)
cell_size_file_name                        = "/projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map"
cellsize = pcr.readmap(cell_size_file_name)

# minimum catchment size (m2) - GRACE resolution products
minimum_area = 300. * 300. * 1000. * 1000. 
# TODO: Shall we also set the maximum size?

# derive landmask
landmask = pcr.ifthen(pcr.defined(ldd_map), pcr.boolean(1.0))
# - remove all islands smaller than the minimum size
islands  = pcr.clump(landmask)
islands  = pcr.ifthen(pcr.areatotal(cellsize, islands) > minimum_area, islands)
landmask = pcr.ifthen(pcr.defined(islands), pcr.boolean(1.0))
#~ pcr.aguila(landmask)

# redefine ldd, landmask and cell size maps that will be used
cellsize = pcr.ifthen(landmask, cellsize)
landmask = pcr.ifthen(landmask, landmask)
ldd_map  = pcr.ifthen(landmask, ldd_map)
# - repair ldd # TODO: Check whether we really need this?
ldd_map  = pcr.lddrepair(ldd_map)
ldd_map  = pcr.lddrepair(ldd_map)

# derive catchments
catchments = pcr.catchment(ldd_map, pcr.pit(ldd_map))
# - remove all catchments smaller than the minimum size
catchments = pcr.ifthen(pcr.areatotal(cellsize, catchments) > minimum_area, catchments)
catchments = pcr.clump(catchments)
#~ pcr.aguila(catchments)

# integrate the near
number_of_identified_catchments = float(pcr.mapmaximum(pcr.scalar(catchments)))
print(number_of_identified_catchments)
newnum_of_identified_catchments = 0.0
# - window size (in arc degree)
window_size = 2.5
while newnum_of_identified_catchments != number_of_identified_catchments: 
    number_of_identified_catchments = float(pcr.mapmaximum(pcr.scalar(catchments)))
    catchments = pcr.cover(catchments, pcr.windowmajority(catchments, window_size))
    catchments = pcr.catchment(ldd_map, catchments)
    catchments = pcr.ifthen(pcr.scalar(catchments) gt 0.0, catchments)
    catchments = pcr.ifthen(pcr.areatotal(cellsize, catchments) > minimum_area, catchments)
    catchments = pcr.clump(catchments)
    pcr.aguila(catchments)
    newnum_of_identified_catchments = float(pcr.mapmaximum(pcr.scalar(catchments)))
    print(newnum_of_identified_catchments)


#~ 
    #~ catchments = pcr.clump(catchments)
    

#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
#~ 
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, windowmajority(extended_selected_catchment_lddsound_05min.map, 2.5))"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, windowmajority(extended_selected_catchment_lddsound_05min.map, 2.5))"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, windowmajority(extended_selected_catchment_lddsound_05min.map, 2.5))"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
#~ 
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if( defined(lddsound_05min.map), catchment(lddsound_05min.map, extended_selected_catchment_lddsound_05min.map))"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if(scalar(extended_selected_catchment_lddsound_05min.map) gt 0, extended_selected_catchment_lddsound_05min.map)"
#~ 
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
#~ 
#~ # 1
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, windowmajority(extended_selected_catchment_lddsound_05min.map, celllength() * 1.5))"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
#~ 
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if( defined(lddsound_05min.map), catchment(lddsound_05min.map, extended_selected_catchment_lddsound_05min.map))"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if(scalar(extended_selected_catchment_lddsound_05min.map) gt 0, extended_selected_catchment_lddsound_05min.map)"
#~ 
#~ pcrcalc not_selected_yet.map = "if(defined(extended_selected_catchment_lddsound_05min.map), nominal(0), selected_catchment_lddsound_05min.map)"
#~ pcrcalc catchment_not_selected_yet.map = "if(scalar(not_selected_yet.map) gt 0, windowmajority(extended_selected_catchment_lddsound_05min.map, celllength() * 1.5))"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, catchment_not_selected_yet.map)"
#~ 
#~ 
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
#~ aguila extended_selected_catchment_lddsound_05min.map
#~ 
#~ 
