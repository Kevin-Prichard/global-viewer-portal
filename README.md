# Global Viewer Portal SPA

This project includes a single-file HTML SPA generated from the spec in `spec-build/spec-0f9bc8e6241718da3039.xml`.

## Generated Artifact

- `index001.html` (numbered output artifact per RQ4)

## Quick Run

Serve the folder locally, then open `index001.html` in your browser:

```bash
cd /home/kev/projs/thucy/portal
python3 -m http.server 8000
```

Then visit:

- `http://localhost:8000/index001.html`

## Notes

- Uses MapLibre GL JS via CDN.
- Uses Babel + core-js via CDN for broad compatibility.
- Persists `GLOBAL_VIEWER_UUID` and `GLOBAL_VIEWER_STATE` cookies.
