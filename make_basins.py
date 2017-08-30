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
# remove all islands smaller than the minimum size
islands     = pcr.clump(landmask)
islands     = pcr.ifthen(pcr.areatotal(cellsize, islands) > minimum_area, islands)
pcr.aguila(islands)

#~ # derive catchments and their sizes:
#~ catchments = "catchment(lddsound_05min.map, pit(lddsound_05min.map))" 
#~ catchments = "areatotal(cellsize05min.correct.map, catchment_lddsound_05min.map)"



#~ 
#~ 
#~ pcrcalc catchment_lddsound_05min.map = "catchment(lddsound_05min.map, pit(lddsound_05min.map))" 
#~ pcrcalc catchment_size_m2_lddsound_05min.map = "areatotal(cellsize05min.correct.map, catchment_lddsound_05min.map)"
#~ 
#~ pcrcalc selected_catchment_lddsound_05min.map = "if(catchment_size_m2_lddsound_05min.map ge 300 * 300 * 1000 * 1000, catchment_lddsound_05min.map)"
#~ 
#~ pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(selected_catchment_lddsound_05min.map, windowmajority(selected_catchment_lddsound_05min.map, 2.5))"
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
