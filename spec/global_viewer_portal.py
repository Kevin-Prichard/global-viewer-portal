"""Specification file for Global Viewer Portal for Thucy Aero"""

from .err import Feat, Req
from libspec import DataSchema


class GlobalViewerPortalState(DataSchema):
    '''A data class to specify what data fields will be stored for
    remembering cookied user's current state within the app, during
    and between sessions.
    '''
    
    longitude: float = -122.4192398965667
    longitude_note: str = "The user's view portal's center point longitude in decimal form"
    latitude: float = 37.77929461695388
    latitude_note: str = "The user's view portal's center point latitude in decimal form"
    altitude_m: float = 100
    altitude_m_note: str = "The user's portal altitude from earth mean surface level"
    base_map: str  # the base map tile set name from upstream provider

    def model_name(self):
        return "globe-viewer-state"

## --- REQUIREMENTS ---
class TargetMapLibreGLJS(Req):
    '''Make use of MapeLibre GL JS open-source library
    
    - provides core map and globe visualization software and tile data
    - provides a software base that handles an estimated 99% of this
      app's needs"
    '''
    
class SingleFile(Req):
    '''Instruction: Generate all the source in a single HTML file,
    including ECMAscript"

    Simplify this project at its early stages, while still evaluating
    libspec and MapLibre GL JS
    '''

class TargetCompatibleECMAScript(Req):
    '''
    The LLM should generate code compatible with modern browsers,
    and use Babel & core-js to ensure as wide of an audience as
    possible via transpiling and/or polyfilling

    Ensure this web app runs on as many devices as possible
    '''


class OnVisit(Feat):
    '''When a user opens the site in a web browser, perform all
    software tasks necessary to load MapLibre GL JS's libraries, set
    the map/globe view portal up, initialize the portal to the default
    longitude, latitude and altitude'''


class OnFirstVisit(Feat):
    '''
    1. When a user visits for the very first time, generate a cookie
    called GLOBAL_VIEWER_UUID (containing a UUID) to know that they've
    visited.  Generate a second cookie named GLOBAL_VIEWER_STATE to
    contain GlobalViewerPortalState's values, stored as JSON that's
    been URI-encoded; LLM will provide code that performs the:
    encodeURIComponent(JSON.stringify(GlobalViewerPortalState instance))  
    and cookie decoding e.g. JSON.parse(decodeURIComponent(cookie value)).
    
    2. Perform the steps in OnVisit(Feature) to intialize
    the portal display.
    '''

class OnVisitTermination(Feat):
    '''1. Ensure that when the current browser tab or window closes,
    that the current GlobalViewerPortalState values are written to
    GLOBAL_VIEWER_STATE one last time. 2. Then perform all steps
    necessary to shut down MapLibre GL JS's currently running code,
    unload allocated objects -whatever's recommended by that project.'''


class OnReturnVisit(Feat):
    '''1. Check for GLOBAL_VIEWER_UUID, and if GLOBAL_VIEWER_STATE
    restore its encoded values to the GlobalViewerPortalState
    instance. 2. Perform the steps in OnVisit(Feature) to intialize
    the portal display'''
