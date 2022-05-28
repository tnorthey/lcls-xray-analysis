def safe_get(det, evt):
  try:
    return det.get(evt)
  except Exception:
    return None