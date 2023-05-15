

# PCR-GLOBWB
cdo -L trend -yearavg -selyear,2003/2015 totalWaterStorageThickness_monthAvg_output_2000-01-31_to_2015-12-31.nc totalWaterStorageThickness_annuaAvg_output_2003-2015_trend_intercept.nc totalWaterStorageThickness_annuaAvg_output_2003-2015_trend_slope.nc
ncatted -O -a units,"total_thickness_of_water_storage",m,c,"m.year-1" totalWaterStorageThickness_annuaAvg_output_2003-2015_trend_slope.nc
gdal_translate -of PCRaster totalWaterStorageThickness_annuaAvg_output_2003-2015_trend_slope.nc totalWaterStorageThickness_annuaAvg_output_trend_slope.map
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map .
cp /scratch-shared/edwinhs/basin_for_grace_evaluation/catchment_group_final.map .
mapattr -c lddsound_05min.map *.map
# for the PCR-GLOBWB resolution
pcrcalc totalWaterStorageThickness_annuaAvg_output_trend_slope.map = "if(defined(lddsound_05min.map), totalWaterStorageThickness_annuaAvg_output_trend_slope.map)"
# for the catchment/basin resolution
pcrcalc cellsize05min.correct.map = "if(defined(catchment_group_final.map), cellsize05min.correct.map)"
pcrcalc cellsize05min.correct.map = "if(defined(totalWaterStorageThickness_annuaAvg_output_trend_slope.map), cellsize05min.correct.map)"
pcrcalc totalWaterStorageThickness_annuaAvg_output_trend_slope_catchment.map = "areatotal(cellsize05min.correct.map * totalWaterStorageThickness_annuaAvg_output_trend_slope.map, catchment_group_final.map) / areatotal(cellsize05min.correct.map, catchment_group_final.map)"

