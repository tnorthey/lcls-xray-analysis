def get_xint():
  evt_xint_pull = safe_get(diode_upstream, evt)
  if evt_xint_pull is None: return False
  xint = evt_xint_pull.TotalIntensity() #; print('xint: ' + str(xint))
  if (xint < lower_threshold) or (xint >= upper_threshold): return False
  return xint