#!/bin/bash

/usr/local/bin/ffmpeg -i rtmp://192.168.100.29:1936/live/veneza -filter_complex '[0:v] format=pix_fmts=yuv420p, extractplanes=y+u+v [y][u][v]; [y] sr=dnn_backend=tensorflow:scale_factor=2:model=/models/espcn.pb [y_scaled]; [u] scale=iw*2:ih*2 [u_scaled]; [v] scale=iw*2:ih*2 [v_scaled]; [y_scaled][u_scaled][v_scaled] mergeplanes=0x001020:yuv420p [merged]' -map [merged] -sws_flags lanczos -c:v libx264 -crf 17 -c:a $

