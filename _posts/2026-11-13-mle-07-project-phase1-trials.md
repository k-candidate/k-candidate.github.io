---
layout: post
title: "Machine Learning Engineering - 07- Project: Biotech Venture Catalyst"
date: 2026-11-13 00:00:00-0000
categories: 
---

As part of my ongoing **Machine Learning Engineering** series, I built **Biotech Venture Catalyst**, an end-to-end machine learning project that predicts whether a Phase 1 clinical trial will succeed or fail based strictly on its operational design metadata.

Rather than duplicating the setup instructions and curl commands already documented in the [GitHub repository](https://github.com/k-candidate/biotech-venture-catalyst), this post highlights the modeling findings, key architectural decisions, and how to navigate the codebase.

## Walkthrough Video

<div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; margin: 1.5rem 0;">
  <iframe 
    src="https://www.youtube.com/embed/qqN5eXiKUrU" 
    title="Biotech Venture Catalyst | Machine Learning Engineering Project Demo"
    style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; border: 0;" 
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
    allowfullscreen>
  </iframe>
</div>

---

## The Problem & Data Insights

Roughly half of investigational drugs fail during Phase 1 clinical trials. While preclinical biology plays a major role, many failures stem from operational and structural flaws: overly restrictive patient eligibility criteria, unrealistic trial timelines, or complex multi-condition study designs.

Using historical Phase 1 trial records from the **[Therapeutics Data Commons (TDC)](https://tdcommons.ai/)**, I engineered seven operational signals without relying on proprietary molecular data:

* **Temporal Dynamics (`start_year`, `start_month`, `duration_days`):** Parsing raw start and completion dates into total operational lifespan captures study complexity and historical regulatory eras.
* **Indication Structure (`num_conditions`, `primary_disease_chapter`):** Splitting double-underscore-delimited ICD-10 codes quantifies patient co-morbidity burden while isolating the top-level disease chapter.
* **Protocol Text Density (`criteria_word_count`, `exclusion_keyword_count`):** Measuring total word count and scanning for restrictive terms (`exclude`, `exclusion`, `no history`, `prior concurrent`) acts as a lightweight proxy for recruitment bottlenecks.

### The Best Performing Model

In `notebook.ipynb`, I benchmarked **Logistic Regression**, **Random Forest**, and **XGBoost** using a reproducible 60/20/20 train/validation/test split.

Random Forest won, achieving a hold-out test ROC AUC of 0.633.

I will revisit this project in the future. There are a few skills that I want to pick up and apply to see if I can make a better model.

---

## Engineering and Product Trade-Offs

Beyond model selection, several deliberate design choices shaped how the system was packaged:

1. **Keeping Financial Modeling Out of the UI:** In venture capital due diligence, a trial's **Probability of Success (PoS)** feeds into a Risk-Adjusted Net Present Value (**rNPV**) calculation. Rather than cluttering the web interface with arbitrary discount rates and market-size assumptions, I kept the app focused strictly on predicting `PoS` and documented the rNPV formula in the `README.md`.
2. **Continuous Probabilities Over Arbitrary Cutoffs:** Instead of hardcoding a binary *"Low Risk / High Risk"* threshold (like `0.55`) without proprietary fund cost matrices, the dashboard outputs the raw calibrated probability so investment teams can apply their own risk appetite.
3. **Lean Production Containers:** Using `uv` dependency groups in `pyproject.toml`, exploration tools (`jupyterlab`, `matplotlib`, `seaborn`, `pytdc`) stay isolated in `dev`, allowing the `Dockerfile` (`uv sync --frozen --no-install-project --no-dev`) to build a minimal inference image.

---

## How to Navigate the Repository

If you want to explore the project, here is the recommended order:

1. **Start with [`README.md`](https://github.com/k-candidate/biotech-venture-catalyst/blob/main/README.md):** Covers the domain context, local environment setup with `uv`, pre-built Docker Hub image instructions (`kcandidate/biotech-venture-catalyst:v1`), and sample API payloads.
2. **Explore [`notebook.ipynb`](https://github.com/k-candidate/biotech-venture-catalyst/blob/main/notebook.ipynb):** Walks through the exploratory data analysis, missing-value handling, feature engineering experiments, and model comparisons.
3. **Inspect the Python Modules:**
   * [`train.py`](https://github.com/k-candidate/biotech-venture-catalyst/blob/main/train.py): Reproduces the exact data split, fits the `DictVectorizer` + `RandomForestClassifier` pipeline, verifies hold-out ROC AUC, and serializes `model.bin`.
   * [`model.py`](https://github.com/k-candidate/biotech-venture-catalyst/blob/main/model.py): Defines the Pydantic input schema (`RawTrialInput`) and the deterministic raw-to-feature transformation logic.
   * [`predict.py`](https://github.com/k-candidate/biotech-venture-catalyst/blob/main/predict.py): Exposes the trained pipeline as a FastAPI microservice (`/predict` and `/health`) tested via [`test.sh`](https://github.com/k-candidate/biotech-venture-catalyst/blob/main/test.sh).
   * [`app.py`](https://github.com/k-candidate/biotech-venture-catalyst/blob/main/app.py): Powers the interactive Streamlit dashboard.
4. **Try the Live Web Applications:**
   * **Streamlit Cloud Dashboard (Python Backend):** [https://biotech-venture-catalyst.streamlit.app/](https://biotech-venture-catalyst.streamlit.app/)
   * **GitHub Pages Static Demo (In-Browser Inference):** [https://k-candidate.github.io/biotech-venture-catalyst/](https://k-candidate.github.io/biotech-venture-catalyst/)

---

*I will publish a separate post diving into how I exported the scikit-learn model to ONNX and ran client-side inference in the browser using WebAssembly (WASM).*