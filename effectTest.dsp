import("stdfaust.lib");
N = 1;
fc = hslider("cutoff", 100, 0, 10000, 0.1);
process = fi.lowpass(N,fc);
			
