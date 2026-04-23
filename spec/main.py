
from libspec import Spec
from . import global_viewer_portal

class GlobalViewerPortal(Spec):
    def modules(self):
        return [global_viewer_portal]


if __name__ == "__main__":
    GlobalViewerPortal().write_xml("spec-build")
