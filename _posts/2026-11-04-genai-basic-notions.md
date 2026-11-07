---
layout: post
title: "GenAI - Basic Notions"
date: 2026-11-04 00:00:00-0000
audio: true
categories: 
---

A few days ago I took and passed the GCP Generative AI Leader exam. These are my notes from the course.

## **1. Gen AI: Beyond the Chatbot**

* **Generative AI:** A subset of artificial intelligence capable of creating new content and ideas, processing multimodal data such as text, images, and code simultaneously.
* **Core Functional Capabilities:** 
  * **Summarize:** Condense information into concise summaries.
  * **Create:** Generate brand-new content.
  * **Discover:** Retrieve the right information at the right time.
  * **Automate:** Automate previously manual tasks.
* **Foundation Models:** Large AI models trained on massive, diverse datasets that serve as the foundation for generative AI, easily adaptable to specialized domain tasks.
* **Prompting:** The method of interacting with and guiding foundation models through instructions or inputs to produce desired outputs.
* **Gemini Model Family:** Google's core generative AI model that powers solutions across the **Gemini app**, **Google Workspace**, and **Gemini for Google Cloud**.
* **Gen AI Enterprise Strategy:**
  * **Dual Approach:** Combines a top-down leadership vision with bottom-up employee experimentation and feedback.
  * **Strategic Priorities:** Focuses on clear business value, ethical guidelines, responsible AI, resourcing data and talent, measuring business impact, and continuous improvement.

---

## **2. Gen AI: Foundational Concepts**

* **AI Hierarchy:**
  * **Artificial Intelligence (AI):** Building machines to perform tasks requiring human intelligence.
  * **Machine Learning (ML):** A subfield of AI where machines learn from data.
  * **Deep Learning:** A subset of ML utilizing artificial neural networks with many layers to extract complex patterns.
  * **Generative AI:** An application of ML focused specifically on creating original content.
  * **Large Language Models (LLMs):** A type of foundation model engineered to understand and generate human language.
* **Data Fundamentals:**
  * **Structured Data:** Organized, easily searchable data typically stored in relational databases.
  * **Unstructured Data:** Data lacking predefined structure requiring advanced analysis techniques.
  * **Key Data Pillars:** Ensuring high data quality (accurate, complete, consistent) and data accessibility for training.
* **Machine Learning Lifecycle:**
  1. **Data Ingestion & Preparation:** Collecting, cleaning, and transforming raw data.
  2. **Model Training:** Creating the ML model using prepared data.
  3. **Model Deployment:** Making the trained model available for use.
  4. **Model Management:** Maintaining and monitoring models over time.
* **ML Learning Approaches:**
  * **Supervised Learning:** Trains models on labeled data to predict outputs.
  * **Unsupervised Learning:** Uses unlabeled data to uncover natural patterns and groupings.
  * **Reinforcement Learning:** Teaches models through interaction and feedback to maximize rewards.
* **Responsible AI:** Focuses on **Secure AI** (protecting applications from harm) and **Ethical AI** (ensuring non-harmful, fair use), guided by the **[Secure AI Framework (SAIF)](https://safety.google/intl/en/safety/saif/)**.

---

## **3. Gen AI: the Landscape**

* **The Gen AI Tech Stack:** Divided into five key layers: Infrastructure, Model, Platform, Agent, and Gen-AI-powered applications.
* **Google Cloud Agent Platform:** A unified ML platform streamlining the complete ML workflow.
  * **Model Garden:** Allows picking existing models from Google, open-source, or third-party providers.
  * **Model Builder:** Allows custom model training via ML frameworks or minimal-code AutoML.
* **Infrastructure Layer:** The core hardware (servers, GPUs, TPUs) and software required to train, store, and run AI models.
* **AI on the Edge:** Running models locally on hardware devices close to action using tools like **Lite Runtime (LiteRT)** and efficient models like **Gemini Nano**.
* **Project Assessment Factors:**
  * **Needs:** Evaluating scale, customization, user interaction, privacy, latency, and connectivity.
  * **Resources:** Evaluating available talent (people), budget (money), and project timelines (time).

---

## **4. Gen AI Apps: Transform Your Work**

* **Personal Productivity Suite:**
  * **Gemini App:** Generative chatbot for writing, planning, and learning.
  * **Google Workspace with Gemini:** Integrates AI into Gmail, Slides, Meet, and Docs.
  * **Gemini for Google Cloud:** AI assistant for writing/debugging code, BigQuery analysis, and cloud security.
  * **Gemini Notebook:** Research assistant grounded in uploaded user files.
* **Prompting Techniques:**
  * **Zero-Shot:** Asking the model to complete a task with no examples.
  * **One-Shot:** Providing one example for the model to follow.
  * **Few-Shot:** Providing multiple examples for model learning.
  * **Role Prompting:** Assigning a persona to guide style, tone, and focus.
* **Streamlining Workflows:**
  * **Prompt Chaining:** Maintaining conversational back-and-forth context.
  * **Gems:** Personalized AI assistants tailored with specific instructions and prompt templates.
* **Output Grounding & RAG:** Connecting outputs to verifiable data sources using **Retrieval-Augmented Generation (RAG)**.

---

## **5. Gen AI Agents: Transform Your Organization**

* **Gen AI Agent:** An application that works toward a goal by observing its environment and taking action using available tools.
* **Core Agent Architecture:**
  * **Model:** The core algorithms and logic.
  * **Reasoning Loop:** Iterative cycle of observing, interpreting, reasoning, and acting.
  * **Tools:** Functionalities enabling system and data interaction.
* **Agent Tooling Types:**
  * **Extensions:** Connect to external services via APIs.
  * **Functions:** Execute specific actions or tasks.
  * **Data Stores:** Provide access to knowledge bases.
  * **Plugins:** Add new skills and integrations.
* **Agent Categories:**
  * **Deterministic:** Traditional agents operating on predefined paths.
  * **Generative:** Conversational agents powered by natural language LLMs.
* **Reasoning Loop Techniques:**
  * **ReAct (Reason and Act):** Combines reasoning steps with action execution.
  * **Chain-of-Thought (CoT):** Guides models using step-by-step intermediate reasoning examples.
  * **Metaprompting:** Prompts used to generate, modify, or interpret other prompts.
* **RAG Process Steps:**
  1. **Retrieval:** Fetching relevant data from external stores.
  2. **Augmentation:** Incorporating retrieved data into the prompt.
  3. **Generation:** Producing the output based on augmented context.
  4. **Iteration (Optional):** Repeating retrieval steps if necessary.
* **Enterprise CX Solutions:** **Gemini Enterprise for CX** built on CCaaS, offering **CX Agent Studio**, **Agent Assist**, and **CX Insights**.

***

## **6. Model Hyperparameters & Control Settings**

* **Temperature:** Controls the degree of randomness/creativity in model responses.
  * **Low Temperature (0.0 – 0.2):** Produces deterministic, precise, and consistent outputs. Ideal for factual Q&A, code generation, and structured data extraction.
  * **High Temperature (0.7 – 1.0+):** Produces more creative, varied, and unexpected outputs. Ideal for brainstorming, creative writing, and poetry.
* **Top-K:** Limits the model's token selection pool to the top *K* most probable next words/tokens. 
  * A lower Top-K (e.g., 1) forces the model to pick only the single most likely token (greedy decoding).
* **Top-P (Nucleus Sampling):** Selects tokens from a candidate set whose cumulative probability reaches the threshold *P* (e.g., 0.9 for the top 90% probability mass). 
  * Top-P dynamically expands or contracts the token choices depending on the model's confidence.
* **Max Output Tokens:** Sets the hard upper limit on the maximum number of tokens (words/sub-words) the model can generate in a single response.
* **Stop Sequences:** Specific characters or text strings that instruct the model to stop generating output immediately when encountered.
* **Safety Settings:** Configurable thresholds (e.g., block few, block many, block none) used to filter out potentially harmful content, such as hate speech, harassment, or explicit material.

***

## **7. Mind Map**

![mind map]({{ site.baseurl }}/assets/images/gen-ai-mindmap.png){:style="display:block; margin-left:auto; margin-right:auto; width:100.00%"}

***

## **8. Video Summary**

<iframe width="100%" height="400" src="https://www.youtube.com/embed/8BB-SX3k_Zw" frameborder="0" allowfullscreen></iframe>

***

## **9. Final Thoughts**

This field is constantly evolving. Some of the things you have just read might be obsolete in six months. Fall in love with continuous learning. Adaptability is the only tech stack that won't go obsolete.
