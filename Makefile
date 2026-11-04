POST ?=
UV ?= uv

.PHONY: audio audio-all audio-install

audio:
	$(UV) run python scripts/generate_audio.py $(if $(POST),--post "$(POST)")

audio-all:
	$(UV) run python scripts/generate_audio.py --force

audio-install:
	$(UV) sync
