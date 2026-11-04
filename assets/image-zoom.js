(() => {
  'use strict';

  const MIN_SCALE = 0.1;
  const MAX_SCALE = 12;
  const ZOOM_STEP = 1.25;
  let overlay;
  let canvas;
  let viewerImage;
  let closeButton;
  let scale = 1;
  let fitScale = 1;
  let offsetX = 0;
  let offsetY = 0;
  let naturalWidth = 0;
  let naturalHeight = 0;
  let previousFocus;
  let drag;
  let suppressBackdropClose = false;
  let gestureScale = 1;

  function constrainOffset() {
    const renderedWidth = naturalWidth * scale;
    const renderedHeight = naturalHeight * scale;
    const maxX = Math.max(0, (renderedWidth - canvas.clientWidth) / 2);
    const maxY = Math.max(0, (renderedHeight - canvas.clientHeight) / 2);
    offsetX = Math.max(-maxX, Math.min(maxX, offsetX));
    offsetY = Math.max(-maxY, Math.min(maxY, offsetY));
  }

  function render() {
    constrainOffset();
    viewerImage.style.width = `${naturalWidth * scale}px`;
    viewerImage.style.height = `${naturalHeight * scale}px`;
    viewerImage.style.transform = `translate(calc(-50% + ${offsetX}px), calc(-50% + ${offsetY}px))`;
  }

  function setScale(nextScale, clientX = window.innerWidth / 2, clientY = window.innerHeight / 2) {
    const boundedScale = Math.max(MIN_SCALE, Math.min(MAX_SCALE, nextScale));
    if (boundedScale === scale) return;

    // Preserve the pixel underneath the pointer while zooming.
    const rect = canvas.getBoundingClientRect();
    const pointX = clientX - rect.left - rect.width / 2;
    const pointY = clientY - rect.top - rect.height / 2;
    const ratio = boundedScale / scale;
    offsetX = pointX - (pointX - offsetX) * ratio;
    offsetY = pointY - (pointY - offsetY) * ratio;
    scale = boundedScale;
    render();
  }

  function resetView() {
    scale = fitScale;
    offsetX = 0;
    offsetY = 0;
    render();
  }

  function close() {
    if (!overlay || overlay.hidden) return;
    overlay.classList.remove('is-open');
    window.setTimeout(() => {
      overlay.hidden = true;
      viewerImage.removeAttribute('src');
      previousFocus?.focus();
    }, 180);
  }

  function open(source, trigger) {
    previousFocus = trigger;
    viewerImage.onload = () => {
      naturalWidth = viewerImage.naturalWidth;
      naturalHeight = viewerImage.naturalHeight;
      fitScale = Math.min(
        (canvas.clientWidth * 0.94) / naturalWidth,
        (canvas.clientHeight * 0.9) / naturalHeight,
        1
      );
      resetView();
      overlay.classList.add('is-open');
      closeButton.focus();
    };
    overlay.hidden = false;
    viewerImage.src = source;
  }

  function buildViewer() {
    overlay = document.createElement('div');
    overlay.className = 'image-zoom-overlay';
    overlay.hidden = true;
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');
    overlay.setAttribute('aria-label', 'Image zoom viewer');
    overlay.innerHTML = `
      <div class="image-zoom-canvas">
        <img class="image-zoom-image" alt="">
      </div>
      <div class="image-zoom-controls" role="toolbar" aria-label="Image viewer controls">
        <button type="button" data-zoom-out aria-label="Zoom out">−</button>
        <button type="button" data-zoom-reset aria-label="Reset zoom">↺</button>
        <button type="button" data-zoom-in aria-label="Zoom in">+</button>
        <button type="button" data-zoom-close aria-label="Close image viewer">×</button>
      </div>`;
    overlay.insertAdjacentHTML('beforeend', `
      <div class="image-zoom-gesture-hint" aria-label="Viewer gestures">
        <span><b aria-hidden="true">↕</b> Scroll to zoom</span>
        <span><b aria-hidden="true">✥</b> Drag to pan</span>
        <span><b aria-hidden="true">Esc</b> Close</span>
      </div>`);
    document.body.append(overlay);
    canvas = overlay.querySelector('.image-zoom-canvas');
    viewerImage = overlay.querySelector('.image-zoom-image');
    viewerImage.draggable = false;
    closeButton = overlay.querySelector('[data-zoom-close]');

    overlay.addEventListener('click', (event) => {
      if (event.target === overlay) close();
    });
    closeButton.addEventListener('click', close);
    overlay.querySelector('[data-zoom-in]').addEventListener('click', () => setScale(scale * ZOOM_STEP));
    overlay.querySelector('[data-zoom-out]').addEventListener('click', () => setScale(scale / ZOOM_STEP));
    overlay.querySelector('[data-zoom-reset]').addEventListener('click', resetView);

    canvas.addEventListener('wheel', (event) => {
      event.preventDefault();
      // Browser trackpad pinches are normally exposed as Ctrl+wheel events.
      // They need a higher multiplier than a physical mouse wheel to feel natural.
      const sensitivity = event.ctrlKey ? 0.01 : 0.002;
      setScale(scale * Math.exp(-event.deltaY * sensitivity), event.clientX, event.clientY);
    }, { passive: false });
    // Safari exposes trackpad pinches through these gesture events rather than wheel.
    canvas.addEventListener('gesturestart', (event) => {
      event.preventDefault();
      gestureScale = scale;
    }, { passive: false });
    canvas.addEventListener('gesturechange', (event) => {
      event.preventDefault();
      setScale(gestureScale * event.scale, event.clientX, event.clientY);
    }, { passive: false });
    canvas.addEventListener('click', (event) => {
      // The canvas is the visible dark backdrop around the image.
      if (event.target === canvas && !suppressBackdropClose) close();
    });
    canvas.addEventListener('dblclick', (event) => {
      event.preventDefault();
      setScale(scale * 1.75, event.clientX, event.clientY);
    });
    canvas.addEventListener('pointerdown', (event) => {
      if (event.button !== 0) return;
      event.preventDefault();
      drag = { x: event.clientX, y: event.clientY, offsetX, offsetY };
      suppressBackdropClose = false;
      canvas.classList.add('is-panning');
      canvas.setPointerCapture(event.pointerId);
    });
    canvas.addEventListener('pointermove', (event) => {
      if (!drag) return;
      event.preventDefault();
      if (Math.abs(event.clientX - drag.x) > 3 || Math.abs(event.clientY - drag.y) > 3) {
        suppressBackdropClose = true;
      }
      offsetX = drag.offsetX + event.clientX - drag.x;
      offsetY = drag.offsetY + event.clientY - drag.y;
      render();
    });
    const stopDragging = () => {
      drag = undefined;
      canvas.classList.remove('is-panning');
      // A browser emits `click` after pointerup. Keep that synthetic click from
      // closing the viewer after a real pan, then re-enable backdrop closing.
      if (suppressBackdropClose) {
        window.setTimeout(() => { suppressBackdropClose = false; }, 0);
      }
    };
    canvas.addEventListener('pointerup', stopDragging);
    canvas.addEventListener('pointercancel', stopDragging);
  }

  document.addEventListener('DOMContentLoaded', () => {
    if (!document.querySelector('.post-content')) return;
    buildViewer();
    document.addEventListener('click', (event) => {
      const image = event.target.closest('.post-content img');
      if (!image || !image.src) return;
      event.preventDefault();
      open(image.src, image);
    });
    document.addEventListener('keydown', (event) => {
      if (event.key === 'Escape') close();
    });
    window.addEventListener('resize', () => {
      if (overlay && !overlay.hidden && naturalWidth) {
        fitScale = Math.min((canvas.clientWidth * 0.94) / naturalWidth, (canvas.clientHeight * 0.9) / naturalHeight, 1);
        render();
      }
    });
  });
})();
