python ~/git/scripts/hs_plot.py
cd tiff
python2 ~/git/scripts/gwy_convert_tiff.py
cd processed_data
cd line_int
python3 ~/git/scripts_open/plot_lines.py
cd ..
cd fft_diff
python3 ~/git/scripts_open/plot_ED_XRD.py
cd ..
cd ..
python3 ~/git/scripts_open/combine.py
mv processed_data/ ./..
cd ..
rm -rf ./tiff
