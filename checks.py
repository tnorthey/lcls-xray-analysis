"""various checks, returns False if any fail."""
from load_get_functions import safe_get

def checks(_evt, evr, x_ray, electron, diode_downstream, XRAYOFF, det_z):
    """various checks, returns False if any fail."""
    ########################################################
    ### BEGIN CHECKS
    if _evt is None:
        return False
    evrcodes = evr(_evt)
    if evrcodes is None:
        return False
    if XRAYOFF in evrcodes:
        return False
    evt_xray_pull = safe_get(x_ray, _evt)
    if evt_xray_pull is None:
        return False
    #x-ray intensity in mJ
    #evt_xray = evt_xray_pull.f_21_ENRC()
    #print('evt_xray: ' + str(evt_xray))
    # electron pull?
    evt_electron_pull = safe_get(electron, _evt)
    if evt_electron_pull is None:
        return False
    #evt_electron = evt_electron_pull.ebeamCharge()
    #print('evt_electron: ' + str(evt_electron))
    # position in space of Jungfrau (distance from cell)
    evt_det_z = det_z(_evt)
    if evt_det_z is None:
        return False
    evt_xint_pulldown = safe_get(diode_downstream, _evt)
    if evt_xint_pulldown is None:
        return False
    #evt_diode_downstream = evt_xint_pulldown.TotalIntensity()
    #print('evt_diode_downstream: ' + str(evt_diode_downstream))
    return True
    ### END CHECKS
    ########################################################
