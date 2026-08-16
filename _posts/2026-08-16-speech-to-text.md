---
layout: post
title: "Self-Hosted STT: Parakeet ASR, and Transcript Post-Processing via Gemma 3"
date: 2026-08-16 00:00:00-0000
categories: 
---

I have a blog post coming up that will be very long, and I don't want to type all of it out.

My laptop has a built-in GPU, so why not set up a small local pipeline? I don't want my voice or the transcript going to a third-party server. Privacy and low latency are key.

I want to speak my text while also using dictation commands like "new line", "new paragraph" or "bullet point".

To achieve this, the pipeline needs 2 main pieces:
1. **Automatic Speech Recognition (ASR)** to generate a literal transcript.
2. **Transcript post-processing** to transform spoken commands like "new paragraph" into actual formatting.

## STT vs ASR

STT (Speech-To-Text) and ASR (Automatic Speech Recognition) are used interchangeably.

But there's a slight distinction:
- ASR is the core underlying technology. It focuses on the machine's ability to "hear" audio, "recognize" acoustic patterns, and identify the exact spoken words.
- STT is the broader task or application. It takes the words recognized by the ASR model and outputs them as a readable text format.

## Finding the Right Tools

Before diving headfirst into writing custom Python code, I wanted to see if tools already existed to save me time. Fortunately, others have had the exact same need and created user-friendly programs.

After exploring a few options, I chose [Handy](https://github.com/cjpais/handy) because it fits my needs, and is actively maintained.

## My Working Config

Here's the combination that ended up working best for my setup:

- OS: Ubuntu Noble
- GPU: built-in NVIDIA with `4096MiB` VRAM (Quadro P2000 mobile).
- NVIDIA Driver: 580
- Handy Settings:
  - Version: v0.9.4
  - Model: `Parakeet Unified EN 0.6B`
  - Unload Model: Immediately
  - Paste method: Clipboard (Ctrl+V)
  - Clipboard Handling: Don't Modify Clipboard
- Post-Processing via Ollama
  - `nvidia-container-toolkit` installed
  - Ollama runs inside a container: 
    ```bash
    docker run \
    -d \
    --gpus=all \
    -e OLLAMA_KEEP_ALIVE=0 \
    -v ollama:/root/.ollama \
    -p 11434:11434 \
    --name ollama \
    ollama/ollama
    ```
  - Gemma 3 (`gemma3:4b`) pulled via Ollama: `docker exec -d ollama ollama pull gemma3:4b`
- Post-Processing Setup in Handy:
  - Provider: Custom
  - Base URL: `http://localhost:11434/v1`
  - API Key: Can be anything (not validated)
  - Model: `gemma3:4b`
  - Prompt instructions:
    ```text
    You are an expert real-time dictation assistant. Fix the transcription provided below.

    # MANDATORY INSTRUCTIONS:
    - ONLY output the final corrected text. Do NOT add intros, outros, explanations, or quotes.
    - Preserve the exact meaning, word order, and intent. Do NOT summarize or rephrase.
    - Strip out verbal filler words (e.g., "um", "uh", "like", "you know").

    # FORMATTING & PUNCTUATION RULES:
    - Convert spoken headings directly into Markdown hashes. Delete the spoken phrase completely (e.g., if the text says "heading two", replace those words entirely with "## " and apply standard capitalization to the words that follow it).
    - Convert spoken lists into clean Markdown lists. If I say "bullet point" or "bullet", delete those words, start a new line, and use a hyphen followed by a space ("- ").
    - If I say "numbered list" or "next item", start a new line with the next logical number (e.g., "1. ", "2. ").
    - Automatically add natural commas, periods, question marks, and capitalization.
    - If the text contains the word "colon", convert it into the literal punctuation symbol (:).
    - If the text contains the words "new line", delete those words and create an actual physical line break by pressing enter once.
    - If the text contains the words "new paragraph", delete those words and create a physical blank line gap between the paragraphs by pressing enter twice.
    - Convert spoken numbers and currency to digits (e.g., "twenty five" to "25", "ten dollars" to "$10").

    # TRANSCRIPTION TEXT TO FIX:
    ${output}
    ```

## How It Works

1. I enable Handy
2. The Parakeet loads into the GPU
3. I speak then stop recording
4. My speech is converted to text and Parakeet immediately unloads from the GPU
5. Handy sends the transcript to Ollama with the prompt
6. Gemma loads into the GPU and post-processes the text and sends it back to Handy
7. Gemma unloads from the GPU
8. Handy pastes the formatted text wherever my cursor is.

This is the most comfortable and accurate combination I have been able to run on this GPU.

I tried various combinations of models, model sizes, loading/unloading strategies to fit both pieces into the GPU simultaneously (or offload parts to the CPU), but they either dropped accuracy too much, or caused the laptop to overheat. After hours of tinkering, I decided to skip further tweaks via Modelfile and start reaping the ROI right away.

I'm content with the result: all of my data stays locally on my laptop, I avoid internet latency, and it's going to save me a significant amount of time when writing long texts!