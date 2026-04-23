"""Specification file for Global Viewer Portal for Thucy Aero"""

from .err import Feat, Req

from libspec import Feature, Constraint, Requirement, DataSchema, Spec

from .err import Feat, Req, Err


class GlobalViewerPortalState(DataSchema):
    '''A data class to specify what data fields will be stored for remembering cookied user's current state within the app, during and between sessions.'''
    longitude: float = -122.4192398965667
    longitude_note: str = "The user's view portal's center point longitude in decimal form"
    latitude: float = 37.77929461695388
    latitude_note: str = "The user's view portal's center point latitude in decimal form"
    altitude_m: float = 100
    altitude_m_note: str = "The user's portal altitude from earth mean surface level"
    base_map: str  # the base map tile set name from upstream provider

    def model_name(self):
        return "globe-viewer-state"

"""
class _(Requirement):
    def req_id(self):  return "RQ"
    def title(self):   return ""
    def actor(self):   return ""
    def action(self):  return ""
    def benefit(self): return ""
"""

## --- REQUIREMENTS ---
class TargetMapLibreGLJS(Requirement):
    def req_id(self):  return "RQ0"
    def title(self):   return "Make use of MapeLibre GL JS open-source library"
    def actor(self):   return "LLM"
    def action(self):  return "provides core map and globe visualization software and tile data"
    def benefit(self): return "provides a software base that handles an estimated 99% of this app's needs"

class SingleFile(Requirement):
    def req_id(self):  return "RQ1"
    def title(self):   return "one-source-html-file"
    def actor(self):   return "LLM"
    def action(self):  return "The LLM should generate all the source in a single HTML file, including ECMAscript"
    def benefit(self): return "Simplify this project at its early stages, while still evaluating libspec and MapLibre GL JS"

class TargetCompatibleECMAScript(Requirement):
    def req_id(self):  return "RQ2"
    def title(self):   return "target-compatible-ecmascript"
    def actor(self):   return "LLM"
    def action(self):  return "The LLM should generate code compatible with modern browsers, and use Babel & core-js to ensure as wide of an audience as possible via transpiling and/or polyfilling"
    def benefit(self): return "Ensure this web app runs on as many devices as possible"

class UseMIMETypesForCDNs(Requirement):
    def req_id(self):  return "RQ3"
    def title(self):   return "specify-mimetype-for-cdn-scripts"
    def actor(self):   return "LLM"
    def action(self):  return "When generating <Script> tags for CDN resources, the LLM should generate <script> tags that specify mime-types, otherwise browser error handlers will throw errors and prevent the page from rendering."
    def benefit(self): return "Ensure this web app runs when using CDN-loaded resources"

class SpecifyIncrementalOutputFilename(Requirement):
    def req_id(self):  return "RQ4"
    def title(self):   return "specify-numbered-output-filenames"
    def actor(self):   return "LLM"
    def action(self):  return "When writing generated index.html, use the format index%03d.html and increment the number each time, so that previous versions are preserved."
    def benefit(self): return "Ensure this web app runs when using CDN-loaded resources"


## --- FEATURES ---
DATE_VER_0_0_0 = "2026-04-22"

'''
class _(Feature):
    def feature_name(self): return ""
    def date(self):         return DATE_VER_0_0_0
    def description(self):  return """_"""
'''

class OnVisit(Feature):
    def feature_name(self): return "on-visit"
    def date(self):         return DATE_VER_0_0_0
    def description(self):  return """When a user opens the site in a web browser, perform all software tasks necessary to load MapLibre GL JS's libraries, set the map/globe view portal up, initialize the portal to the default longitude, latitude and altitude"""

class OnFirstVisit(Feature):
    def feature_name(self): return "on-first-visit"
    def date(self):         return DATE_VER_0_0_0
    def description(self):  return """1. When a user visits for the very first time, generate a cookie called GLOBAL_VIEWER_UUID (containing a UUID) to know that they've visited.  Generate a second cookie named GLOBAL_VIEWER_STATE to contain GlobalViewerPortalState's values, stored as JSON that's been URI-encoded; LLM will provide code that performs the encodeURIComponent(JSON.stringify(GlobalViewerPortalState instance)) and cookie decoding e.g. JSON.parse(decodeURIComponent(cookie value)).  2. Perform the steps in OnVisit(Feature) to intialize the portal display."""

class OnVisitTermination(Feature):
    def feature_name(self): return "on-visit-close"
    def date(self):         return DATE_VER_0_0_0
    def description(self):  return """1. Ensure that when the current browser tab or window closes, that the current GlobalViewerPortalState values are written to GLOBAL_VIEWER_STATE one last time. 2. Then perform all steps necessary to shut down MapLibre GL JS's currently running code, unload allocated objects -whatever's recommended by that project."""

class OnReturnVisit(Feature):
    def feature_name(self): return "on-return-visit"
    def date(self):         return DATE_VER_0_0_0
    def description(self): return """1. Check for GLOBAL_VIEWER_UUID, and if GLOBAL_VIEWER_STATE restore its encoded values to the GlobalViewerPortalState instance. 2. Perform the steps in OnVisit(Feature) to intialize the portal display"""
