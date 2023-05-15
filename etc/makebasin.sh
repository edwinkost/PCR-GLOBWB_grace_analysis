
rm *.map

cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/lddsound_05min.map .
cp /projects/0/dfguu/data/hydroworld/PCRGLOBWB20/input5min/routing/cellsize05min.correct.map .

pcrcalc catchment_lddsound_05min.map = "catchment(lddsound_05min.map, pit(lddsound_05min.map))" 
pcrcalc catchment_size_m2_lddsound_05min.map = "areatotal(cellsize05min.correct.map, catchment_lddsound_05min.map)"

pcrcalc selected_catchment_lddsound_05min.map = "if(catchment_size_m2_lddsound_05min.map ge 300 * 300 * 1000 * 1000, catchment_lddsound_05min.map)"

pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(selected_catchment_lddsound_05min.map, windowmajority(selected_catchment_lddsound_05min.map, 2.5))"
pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"

pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, windowmajority(extended_selected_catchment_lddsound_05min.map, 2.5))"
pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, windowmajority(extended_selected_catchment_lddsound_05min.map, 2.5))"
pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, windowmajority(extended_selected_catchment_lddsound_05min.map, 2.5))"
pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"

pcrcalc extended_selected_catchment_lddsound_05min.map = "if( defined(lddsound_05min.map), catchment(lddsound_05min.map, extended_selected_catchment_lddsound_05min.map))"
pcrcalc extended_selected_catchment_lddsound_05min.map = "if(scalar(extended_selected_catchment_lddsound_05min.map) gt 0, extended_selected_catchment_lddsound_05min.map)"

pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"

# 1
pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, windowmajority(extended_selected_catchment_lddsound_05min.map, celllength() * 1.5))"
pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"

pcrcalc extended_selected_catchment_lddsound_05min.map = "if( defined(lddsound_05min.map), catchment(lddsound_05min.map, extended_selected_catchment_lddsound_05min.map))"
pcrcalc extended_selected_catchment_lddsound_05min.map = "if(scalar(extended_selected_catchment_lddsound_05min.map) gt 0, extended_selected_catchment_lddsound_05min.map)"

pcrcalc not_selected_yet.map = "if(defined(extended_selected_catchment_lddsound_05min.map), nominal(0), selected_catchment_lddsound_05min.map)"
pcrcalc catchment_not_selected_yet.map = "if(scalar(not_selected_yet.map) gt 0, windowmajority(extended_selected_catchment_lddsound_05min.map, celllength() * 1.5))"
pcrcalc extended_selected_catchment_lddsound_05min.map = "cover(extended_selected_catchment_lddsound_05min.map, catchment_not_selected_yet.map)"


pcrcalc extended_selected_catchment_lddsound_05min.map = "clump(extended_selected_catchment_lddsound_05min.map)"
pcrcalc extended_selected_catchment_lddsound_05min.map = "if(areatotal(cellsize05min.correct.map, extended_selected_catchment_lddsound_05min.map) ge 300 * 300 * 1000 * 1000, extended_selected_catchment_lddsound_05min.map)"
aguila extended_selected_catchment_lddsound_05min.map


