
# for calculating groundwater depletion
pwd 
cdo setunit,"m.year-1" -yearsum -selyear,2000/2008 ../../netcdf/fossilGroundwaterAbstraction_monthTot_output.nc fossilGroundwaterAbstraction_annuaTot_2000to2008.nc
cdo timavg fossilGroundwaterAbstraction_annuaTot_2000to2008.nc fossilGroundwaterAbstraction_annuaTot_avg2000to2008.nc
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .
pcrcalc fossilGroundwaterAbstraction_annuaTot_avg2000to2008.map = "scalar(fossilGroundwaterAbstraction_annuaTot_avg2000to2008.nc)"
mapattr -c cellsize05min.correct.map fossilGroundwaterAbstraction_annuaTot_avg2000to2008.map
pcrcalc fossilGroundwaterAbstraction_annuaTot_avg2000to2008_km3_total.map = "maptotal(fossilGroundwaterAbstraction_annuaTot_avg2000to2008.map * cellsize05min.correct.map)/1000000000."
mapattr -p fossilGroundwaterAbstraction_annuaTot_avg2000to2008_km3_total.map

# for calculating total abstraction
pwd
cdo setunit,"m.year-1" -yearsum -selyear,2000/2008 ../../netcdf/totalAbstraction_monthTot_output.nc totalAbstraction_annuaTot_2000to2008.nc
cdo timavg totalAbstraction_annuaTot_2000to2008.nc totalAbstraction_annuaTot_avg2000to2008.nc
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .
pcrcalc totalAbstraction_annuaTot_avg2000to2008.map = "scalar(totalAbstraction_annuaTot_avg2000to2008.nc)"
mapattr -c cellsize05min.correct.map totalAbstraction_annuaTot_avg2000to2008.map
pcrcalc totalAbstraction_annuaTot_avg2000to2008_km3_total.map = "maptotal(totalAbstraction_annuaTot_avg2000to2008.map * cellsize05min.correct.map)/1000000000."
mapattr -p totalAbstraction_annuaTot_avg2000to2008_km3_total.map

# for calculating total nonIrrGrossDemand
pwd
cdo setunit,"m.year-1" -yearsum -selyear,2000/2008 ../../netcdf/nonIrrGrossDemand_monthTot_output.nc nonIrrGrossDemand_annuaTot_2000to2008.nc
cdo timavg nonIrrGrossDemand_annuaTot_2000to2008.nc nonIrrGrossDemand_annuaTot_avg2000to2008.nc
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .
pcrcalc nonIrrGrossDemand_annuaTot_avg2000to2008.map = "scalar(nonIrrGrossDemand_annuaTot_avg2000to2008.nc)"
mapattr -c cellsize05min.correct.map nonIrrGrossDemand_annuaTot_avg2000to2008.map
pcrcalc nonIrrGrossDemand_annuaTot_avg2000to2008_km3_total.map = "maptotal(nonIrrGrossDemand_annuaTot_avg2000to2008.map * cellsize05min.correct.map)/1000000000."
mapattr -p nonIrrGrossDemand_annuaTot_avg2000to2008_km3_total.map

# for calculating total irrGrossDemand
pwd
cdo setunit,"m.year-1" -yearsum -selyear,2000/2008 ../../netcdf/irrGrossDemand_monthTot_output.nc irrGrossDemand_annuaTot_2000to2008.nc
cdo timavg irrGrossDemand_annuaTot_2000to2008.nc irrGrossDemand_annuaTot_avg2000to2008.nc
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .
pcrcalc irrGrossDemand_annuaTot_avg2000to2008.map = "scalar(irrGrossDemand_annuaTot_avg2000to2008.nc)"
mapattr -c cellsize05min.correct.map irrGrossDemand_annuaTot_avg2000to2008.map
pcrcalc irrGrossDemand_annuaTot_avg2000to2008_km3_total.map = "maptotal(irrGrossDemand_annuaTot_avg2000to2008.map * cellsize05min.correct.map)/1000000000."
mapattr -p irrGrossDemand_annuaTot_avg2000to2008_km3_total.map
