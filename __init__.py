def classFactory(iface): 
    from .elevation_profile import ElevationProfile
    return ElevationProfile(iface)
