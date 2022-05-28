def load_diode_adu_thresholds():
 #These diode values are from the diode which measures the pulse by pulse X-ray pulse intensity. 
 diode_avg = 25000
 lower_threshold = 10
 upper_threshold = 50000
 # Each pixel threshold; ADU or keV units 
 lb = 2	# lower bound (ADU) for a hit
 ub = 80    # Upper bound (ADU) for a hit
 return diode_avg,lower_threshold,upper_threshold,lb,ub