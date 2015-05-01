# for calculating groundwater depletion

cdo setunit,"m.year-1" -yearsum -selyear,2000/2008 ../../netcdf/fossilGroundwaterAbstraction_monthTot_output.nc fossilGroundwaterAbstraction_annuaTot_2000to2008.nc
cdo timavg fossilGroundwaterAbstraction_annuaTot_2000to2008.nc fossilGroundwaterAbstraction_annuaTot_avg2000to2008.nc
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .
pcrcalc fossilGroundwaterAbstraction_annuaTot_avg2000to2008.map = "scalar(fossilGroundwaterAbstraction_annuaTot_avg2000to2008.nc)"
mapattr -c cellsize05min.correct.map fossilGroundwaterAbstraction_annuaTot_avg2000to2008.map
pcrcalc fossilGroundwaterAbstraction_annuaTot_avg2000to2008_km3_total.map = "maptotal(fossilGroundwaterAbstraction_annuaTot_avg2000to2008.map * cellsize05min.correct.map)/1000000000."
mapattr -p fossilGroundwaterAbstraction_annuaTot_avg2000to2008_km3_total.map
