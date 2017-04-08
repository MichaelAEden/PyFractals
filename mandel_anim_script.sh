#!/bin/sh
ffmpeg -framerate 20 -i anim/frame_%00d.png -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p anim.mp4