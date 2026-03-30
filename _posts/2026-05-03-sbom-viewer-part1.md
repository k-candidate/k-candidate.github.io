---
layout: post
title: "SBOM Viewer - What is SBOM, the MVP Design Pattern for GUIs, Making a Cross-Platform Desktop GUI with Python's Tkinter"
date: 2026-05-03 00:00:00-0000
categories: 
---

[https://github.com/k-candidate/sbom-viewer](https://github.com/k-candidate/sbom-viewer)

## What's the project? and why do it?

There's no desktop GUI that displays SBOMs.

![perplexity saying that there are no desktop gui sbom viewers]({{ site.baseurl }}/assets/images/sbom-viewer-post01-01.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

![google saying that there are no desktop gui sbom viewers]({{ site.baseurl }}/assets/images/sbom-viewer-post01-02.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

Sure there are TUIs and web apps, but no desktop GUI.

It's a gap in the market and I am happy to fill it: [https://github.com/k-candidate/sbom-viewer](https://github.com/k-candidate/sbom-viewer)

## What is SBOM?

This looks good: [https://github.com/resources/articles/what-is-an-sbom-software-bill-of-materials](https://github.com/resources/articles/what-is-an-sbom-software-bill-of-materials)

I do not want to re-write what's already out there.

## What is MVP?

MVP (Model-View-Presenter) is a design pattern for GUIs.  
This looks good: [https://medium.com/@li.ying.explore/looking-into-gui-architecture-design-patterns-f87d72751099](https://medium.com/@li.ying.explore/looking-into-gui-architecture-design-patterns-f87d72751099).

Basically:
- Model = app data
- View = the graphical part (in my case the Tk widgets)
- Presenter = app behavior

The app `sbom-viewer` is structured around MVP:
- The Model lives in `app/models.py`. Its job is to hold normalized SBOM data and answer questions about it: metadata, components, dependencies, filtering, and component lookup. It does not know anything about Tkinter widgets or button clicks.
- The View lives in `app/view.py`. This is the Tkinter window. It creates the widgets, tables, tabs, search boxes, and status label, and exposes simple methods like `set_metadata(...)`, `set_component_rows(...)`, `set_dependency_rows(...)`, and `show_error(...)`. In MVP terms, the view is intentionally "dumb": it renders data and forwards user actions, but it does not decide "business" behavior.
- The Presenter lives in `app/presenter.py`. This is the coordinator. It reacts to user actions such as opening a file, reloading, filtering, or selecting a component. It calls the parser layer, loads data into the model, asks the formatter for GUI-friendly rows, and then updates the view. This is the layer that connects "what the user did" to "what the app should show."

The flow is:
- `main.py` creates `SBOMPresenter`
- `main.py` creates `MainView`
- the presenter attaches to the view
- user actions in the view call presenter methods
- the presenter loads or filters data via the model
- the presenter sends display-ready results back to the view

And then there are some supporting pieces:
- parsers in `app/parsers/` convert CycloneDX, SPDX, and SWID files into one normalized internal shape
- formatting in `app/presentation.py` turns model data into rows and detail text for the GUI

Why do it this way?  
I think it makes these things easier:
- testing, because most behavior lives outside the GUI
- refactoring, because parsing, state, and rendering are separated
- understanding it, because each layer has a clear responsibility

## What the first release looks like

On Ubuntu:

![SBOM Viewer on Ubuntu]({{ site.baseurl }}/assets/images/sbom-viewer-post01-03.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

On Windows:

![SBOM Viewer on Windows]({{ site.baseurl }}/assets/images/sbom-viewer-post01-04.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}