
cdo sellonlatbox,-180,180,-90,90 netcdf/CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.nc                   edwin-netcdf/CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.edwin.nc
cdo sellonlatbox,-180,180,-90,90 netcdf/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.nc edwin-netcdf/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.edwin.nc

# GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02
rm -rf annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02
mkdir annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02
cdo -L selyear,2003/2015 -mul -selname,lwe_thickness edwin-netcdf/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.edwin.nc -selname,scale_factor edwin-netcdf/CLM4.SCALE_FACTOR.JPL.MSCNv01CRIv01.edwin.nc annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.edwin.scaled_2003-2015.nc
cdo -L trend -mulc,0.01 -yearavg -selyear,2003/2015 annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.edwin.scaled_2003-2015.nc annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.edwin.scaled_2003-2015_trend_intercept.nc annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.edwin.scaled_2003-2015_trend_slope.nc
gdal_translate -of PCRaster annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02.edwin.scaled_2003-2015_trend_slope.nc annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.tif
gdalwarp -tr 0.08333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333 0.08333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333 annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.tif annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.05min.tif
gdal_translate -of PCRaster annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.05min.tif annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02/GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.05min.map
cd annual_trend_2003-2015_GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map .
cp /scratch-shared/edwinhs/basin_for_grace_evaluation/catchment_group_final.map .
mapattr -c lddsound_05min.map *.map
# for the GRACE resolution
pcrcalc GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.05min.map = "if(defined(lddsound_05min.map), GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.05min.map)"
aguila GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.05min.map
# for the catchment/basin resolution
pcrcalc cellsize05min.correct.map = "if(defined(catchment_group_final.map), cellsize05min.correct.map)"
pcrcalc cellsize05min.correct.map = "if(defined(GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.05min.map), cellsize05min.correct.map)"
pcrcalc GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.05min_catchment.map = "areatotal(cellsize05min.correct.map * GRCTellus.JPL.200204_201701.GLO.RL05M_1.MSCNv02CRIv02_trend_slope.05min.map, catchment_group_final.map) / areatotal(cellsize05min.correct.map, catchment_group_final.map)"

