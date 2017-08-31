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
pcr.report(landmask, "landmask.map")

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
catchments = pcr.ifthen(pcr.scalar(catchments) > 0.0, catchments)
#~ pcr.aguila(catchments)

# integrate small catchments to their nearest catchments that have been identified - with BIG window_size
number_of_identified_catchments = float(pcr.mapmaximum(pcr.scalar(catchments)))
print(number_of_identified_catchments)
# - window size (in arc degree)
window_size = 2.5
for i_iter in range(0, 20):
    number_of_identified_catchments = float(pcr.mapmaximum(pcr.scalar(catchments)))
    catchments = pcr.cover(catchments, pcr.windowmajority(catchments, window_size))
    catchments = pcr.catchment(ldd_map, catchments)
    catchments = pcr.ifthen(pcr.scalar(catchments) > 0.0, catchments)
    catchments = pcr.clump(catchments)
    catchments = pcr.ifthen(pcr.scalar(catchments) > 0.0, catchments)
    catchments = pcr.ifthen(pcr.areatotal(cellsize, catchments) > minimum_area, catchments)
    newnum_of_identified_catchments = float(pcr.mapmaximum(pcr.scalar(catchments)))
    print(newnum_of_identified_catchments)
catchments = pcr.ifthen(pcr.defined(catchments), catchments)
pcr.aguila(catchments)
pcr.report(catchments, "catchments.map")

# identify cells/islands/basins that have not been identified
not_selected_yet = pcr.ifthenelse(pcr.defined(catchments), pcr.boolean(0.0), pcr.boolean(1.0))
not_selected_yet = pcr.ifthen(landmask, not_selected_yet)
not_selected_yet = pcr.ifthen(not_selected_yet, not_selected_yet)
areas_not_selected_yet = pcr.clump(not_selected_yet)
areas_not_selected_yet = pcr.ifthen(pcr.scalar(areas_not_selected_yet) > 0.0, areas_not_selected_yet)
areas_not_selected_yet = pcr.ifthen(pcr.areatotal(cellsize, areas_not_selected_yet) > minimum_area, areas_not_selected_yet)
areas_not_selected_yet = pcr.ifthen(pcr.defined(areas_not_selected_yet), areas_not_selected_yet)
pcr.aguila(areas_not_selected_yet)
pcr.report(areas_not_selected_yet, "areas_not_selected_yet.map")


# merge "catchments" and "areas_not_selected_yet.map"
catchment_group_scalar = pcr.cover(pcr.scalar(catchments), 0.0)
catchment_group_scalar = pcr.cover(pcr.scalar(areas_not_selected_yet) + pcr.mapmaximum(catchment_group_scalar) * 10.0 + 1.0, 0.0) + catchment_group_scalar
catchment_group_scalar = pcr.ifthen(catchment_group_scalar > 0.0, catchment_group_scalar)
catchment_group_scalar = pcr.ifthen(landmask, catchment_group_scalar)
catchment_group = pcr.clump(pcr.nominal(catchment_group_scalar))
catchment_group = pcr.ifthen(pcr.scalar(catchment_group) > 0.0, catchment_group)
catchment_group = pcr.ifthen(pcr.areatotal(cellsize, catchment_group) > minimum_area, catchment_group)
catchment_group = pcr.ifthen(pcr.defined(catchment_group), catchment_group)
pcr.aguila(catchment_group)
pcr.report(catchment_group, "catchment_group.map")


# integrate small catchments to their nearest catchments that have been identified - with small window_size
catchments = pcr.ifthen(pcr.defined(catchment_group), catchment_group)
number_of_identified_catchments = float(pcr.mapmaximum(pcr.scalar(catchments)))
print(number_of_identified_catchments)
# - window size (in arc degree)
window_size = pcr.celllength() * 1.10
for i_iter in range(0, 10):
    number_of_identified_catchments = float(pcr.mapmaximum(pcr.scalar(catchments)))
    catchments = pcr.cover(catchments, pcr.windowmajority(catchments, window_size))
    catchments = pcr.catchment(ldd_map, catchments)
    catchments = pcr.ifthen(pcr.scalar(catchments) > 0.0, catchments)
    catchments = pcr.clump(catchments)
    catchments = pcr.ifthen(pcr.scalar(catchments) > 0.0, catchments)
    catchments = pcr.ifthen(pcr.areatotal(cellsize, catchments) > minimum_area, catchments)
    newnum_of_identified_catchments = float(pcr.mapmaximum(pcr.scalar(catchments)))
    print(newnum_of_identified_catchments)
catchments = pcr.ifthen(pcr.defined(catchments), catchments)
pcr.aguila(catchments)
pcr.report(catchments, "catchment_group_final.map")
