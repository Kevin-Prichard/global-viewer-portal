PY=uv run python

SPEC_BUILD=spec-build

.PHONY: spec
spec: $(SPECS)
	$(PY) -m spec.main_spec

.PHONY: diff
diff:
	$(PY) -m libspec.spec_diff $(SPEC_BUILD) 
