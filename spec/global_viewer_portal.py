"""Specification file for Global Viewer Portal for Thucy Aero"""

from libspec import Feature, Constraint, Requirement, DataSchema, Spec

from err import Feat, Req, Err


class GlobalViewerPortalState(DataSchema):
    '''A data class to specify what data fields will be stored for remembering cookied user's current state within the app, during and between sessions.'''
    longitude: float = -122.4192398965667
    longitude_note: str = "The user's view portal's center point longitude in decimal form"
    latitude: float = 37.77929461695388
    latitude_note: str = "The user's view portal's center point latitude in decimal form"
    altitude_m: float = 5000000
    altitude_m_note: str = "The user's portal altitude from earth mean surface level"
    base_map: str = 'satellite-roads'  # the base map tile set name from upstream provider

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
class TargetMapLibreGLJS(Req):
    def actor(self):   return "LLM"
    def action(self):  return "provides core map and globe visualization software and tile data"
    def benefit(self): return "provides a software base that handles an estimated 99% of this app's needs"

class SingleFile(Req):
    def actor(self):   return "LLM"
    def action(self):  return "The LLM should generate all the source in a single HTML file, including ECMAscript"
    def benefit(self): return "Simplify this project at its early stages, while still evaluating libspec and MapLibre GL JS"

class TargetCompatibleECMAScript(Req):
    def actor(self):   return "LLM"
    def action(self):  return "The LLM should generate code compatible with modern browsers, and use Babel & core-js to ensure as wide of an audience as possible via transpiling and/or polyfilling"
    def benefit(self): return "Ensure this web app runs on as many devices as possible"

class UseMIMETypesForCDNs(Req):
    def actor(self):   return "LLM"
    def action(self):  return "When generating <Script> tags for CDN resources, the LLM should generate <script> tags that specify mime-types, otherwise browser error handlers will throw errors and prevent the page from rendering."
    def benefit(self): return "Ensure this web app runs when using CDN-loaded resources"

class SpecifyIncrementalOutputFilename(Req):
    def actor(self):   return "LLM"
    def action(self):  return "When writing generated index.html, use the format index%03d.html and increment the number each time, so that previous versions are preserved."
    def benefit(self): return "Ensure this web app runs when using CDN-loaded resources"

class MapLibreGlobeProjection(Req):
    def actor(self):   return "LLM"
    def action(self):  return "Use MapLibre GL JS >= 5.0.0 and call map.setProjection({type:'globe'}) inside the map load event."
    def benefit(self): return "Provides a 3D globe visualization instead of a flat 2D map."

class SupportPMTiles(Req):
    def actor(self):   return "LLM"
    def action(self):  return "Load the pmtiles.js library via CDN and register the 'pmtiles://' protocol with maplibregl."
    def benefit(self): return "Allows rendering single-file PMTiles map tile archives."

class SupportCloudOptimizedGeoTIFF(Req):
    def actor(self):   return "LLM"
    def action(self):  return "Load geotiff.js via CDN and implement a custom 'cog://' protocol handler that downloads, normalizes, and color-maps GeoTIFF windows on-the-fly to XYZ canvas blobs. It should support a '?colormap=' query parameter to apply different manually generated colormaps (e.g. viridis, inferno, plasma, turbo, grey)."
    def benefit(self): return "Enables direct-in-browser rendering of massive remote sensing raster files without a backend server, with advanced color mapping capabilities."

## --- FEATURES ---

'''
class _(Feat):
    def feature_name(self): return ""
    def date(self):         return DATE_VER_0_0_0
    def description(self):  return """_"""
'''

class OnVisit(Feat):
    def description(self):  return """When a user opens the site in a web browser, perform all software tasks necessary to load MapLibre GL JS's libraries, set the map/globe view portal up, initialize the portal to the default longitude, latitude and altitude. Also include MapLibre GL JS NavigationControl (with pitch visualization) and ScaleControl, and enable tile boundary debugging."""

class OnFirstVisit(Feat):
    def description(self):  return """1. When a user visits for the very first time, generate a cookie called GLOBAL_VIEWER_UUID (containing a UUID) to know that they've visited.  Generate a second cookie named GLOBAL_VIEWER_STATE to contain GlobalViewerPortalState's values, stored as JSON that's been URI-encoded; LLM will provide code that performs the encodeURIComponent(JSON.stringify(GlobalViewerPortalState instance)) and cookie decoding e.g. JSON.parse(decodeURIComponent(cookie value)).  2. Perform the steps in OnVisit(Feature) to intialize the portal display."""

class OnVisitTermination(Feat):
    def description(self):  return """1. Ensure that when the current browser tab or window closes, that the current GlobalViewerPortalState values are written to GLOBAL_VIEWER_STATE one last time. 2. Then perform all steps necessary to shut down MapLibre GL JS's currently running code, unload allocated objects -whatever's recommended by that project."""

class OnReturnVisit(Feat):
    def description(self): return """1. Check for GLOBAL_VIEWER_UUID, and if GLOBAL_VIEWER_STATE restore its encoded values to the GlobalViewerPortalState instance. 2. Perform the steps in OnVisit(Feature) to intialize the portal display"""

class WatermarkBranding(Feat):
    def description(self):  return """Add translucent 'THUCYDIDES AEROSPACE' watermark bars locked to the top and bottom of the app layout window."""

class ControlPanelUI(Feat):
    def description(self):  return """Provide a floating control panel that displays: the user's UUID, current live longitude, latitude, and altitude. When altitude is below 1,000 meters, it's displayed with meters as units. When altitude exceeds 1000m, it displays in km units, with one decimal place of fraction.  Also provide interactive buttons to 'Reset Default View' and 'Save State' (manually override/save cookie state)."""

class ControlPanelUISelfHides(Feat):
    def description(self): return """The control panel box will self-hide after N seconds of no direct user interactivity (no hover, click or drag actions within the panel; interactions with the globe / map won't affect this), minimizing the box to one line: "Lat: x.xxx, Lon: y.yyy, Alt: zm.  When a hover or click occurs on the minimized box, the panel will restore to its normal full display.  The self-hide timeout will be a constant, let's set it to 10 seconds for now."""

class OnViewPositionChange(Feat):
    def description(self): return """Whenever the user interacts with the portal viewer causing the view position or zoom level to change, this will be reflected in the panel defined in ControlPanelUI."""

class StatusBarUI(Feat):
    def description(self):  return """Provide a floating status bar in the bottom-left corner to show portal loading logs, errors, and interaction status messages."""

class BaseMapSelection(Feat):
    def description(self):  return """Add a dropdown to the control panel allowing the user to select between 'Satellite + Roads (Esri)', 'Street Map — Liberty', and 'Street Map — Bright'. When switched, tear down and rebuild the map state retaining the camera viewport. For the Satellite option, implement a complex tear-down that strips open-source vector layers while preserving sky layers, and injects ESRI World Imagery and Transportation rasters."""

class CustomDataOverlay(Feat):
    def description(self):  return """Add an 'Overlay' section to the control panel where users can paste a custom map URL (XYZ, pmtiles://, or cog://), toggle its visibility on/off via a switch, and adjust its transparency using a 0-100% opacity slider."""
