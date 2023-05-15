

# PCR-GLOBWB
cdo -L trend -yearavg -selyear,2003/2015 totalWaterStorageThickness_monthAvg_output_2000-01-31_to_2015-12-31.nc totalWaterStorageThickness_annuaAvg_output_2003-2015_trend_intercept.nc totalWaterStorageThickness_annuaAvg_output_2003-2015_trend_slope.nc
ncatted -O -a units,"total_thickness_of_water_storage",m,c,"m.year-1" totalWaterStorageThickness_annuaAvg_output_2003-2015_trend_slope.nc
gdal_translate -of PCRaster totalWaterStorageThickness_annuaAvg_output_2003-2015_trend_slope.nc totalWaterStorageThickness_annuaAvg_output_trend_slope.map
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .
cp /scratch-shared/edwinhs/basin_for_grace_evaluation/catchment_group_final.map .
mapattr -c /scratch-shared/edwinhs/basin_for_grace_evaluation/catchment_group_final.map *.map
pcrcalc totalWaterStorageThickness_annuaAvg_output_trend_slope_catchment.map = "areatotal(cellsize05min.correct.map * totalWaterStorageThickness_annuaAvg_output_trend_slope.map, catchment_group_final.map) / areatotal(cellsize05min.correct.map, catchment_group_final.map)"


# GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409
mkdir annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409
cdo -L selyear,2003/2015 -mul -selname,lwe_thickness edwin-netcdf/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409.edwin.nc -selname,SCALE_FACTOR edwin-netcdf/CLM4.SCALE_FACTOR.DS.G300KM.RL05.DSTvSCS1409.edwin.nc annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409.edwin.scaled_2003-2015.nc
cdo -L trend -mulc,0.01 -yearavg -selyear,2003/2015 annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409.edwin.scaled_2003-2015.nc annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409.edwin.scaled_2003-2015_trend_intercept.nc annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409.edwin.scaled_2003-2015_trend_slope.nc
gdal_translate -of PCRaster annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409.edwin.scaled_2003-2015_trend_slope.nc annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409_trend_slope.tif
gdalwarp -tr 0.08333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333 0.08333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333 annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409_trend_slope.tif annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409_trend_slope.05min.tif
gdal_translate -of PCRaster annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409_trend_slope.05min.tif annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409/GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409_trend_slope.05min.map
#
cd annual_trend_2003-2015_GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map .
cp /scratch-shared/edwinhs/basin_for_grace_evaluation/catchment_group_final.map .
mapattr -c /scratch-shared/edwinhs/basin_for_grace_evaluation/catchment_group_final.map *.map
pcrcalc GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409_trend_slope.05min.map           = "if( defined(lddsound_05min.map), GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409_trend_slope.05min.map)"
pcrcalc GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409_trend_slope.05min_catchment.map = "areatotal(cellsize05min.correct.map * GRCTellus.CSR.200204_201701.LND.RL05.DSTvSCS1409_trend_slope.05min.map, catchment_group_final.map) / areatotal(cellsize05min.correct.map, catchment_group_final.map)"

# GRCTellus.GFZ.200204_201701.LND.RL05.DSTvSCS1409

# GRCTellus.JPL.200204_201701.LND.RL05_1.DSTvSCS1411

