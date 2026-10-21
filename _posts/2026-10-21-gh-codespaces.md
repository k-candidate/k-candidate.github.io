---
layout: post
title: "GitHub Codespaces"
date: 2026-10-21 00:00:00-0000
categories:
---

Just taking GitHub Codespaces for a ride.

## Quickstart

- GitHub Codespaces lets you create a cloud-hosted development environment for a repository or template. GitHub runs it on a VM and creates your configured development container inside it.
- When you create a Codespace from a repository, GitHub clones the repository into it. You can also start from a template, and prebuilds can reduce setup time.
- By default, the browser version of Visual Studio Code is the initial editor, but you can connect from other editors, including VS Code Desktop.

## Browser vs. Local Desktop

- **Browser (GitHub.com):** Your browser is the local client. You do not need local development tools or background services to use the Codespace. If you run a web or app server, GitHub forwards the relevant TCP port so you can open the application from your local browser.
- **VS Code Desktop:** Your local VS Code application connects to the remote Codespace. This requires the **GitHub Codespaces** extension and authentication with your GitHub account. When a process inside the Codespace listens on a forwarded port, you can access it locally; for a private port opened through VS Code Desktop, GitHub also exposes it at a localhost address such as `127.0.0.1:8888`.

## Configuration

Configuration relies on **`.devcontainer/devcontainer.json`** to manage the container image, tools and features, editor extensions, forwarded ports, and lifecycle commands such as `postCreateCommand`. If a repository has no configuration, Codespaces uses a default image with many common languages and tools.

Example for a Python Data Science environment using `uv` and Jupyter Lab: [https://github.com/k-candidate/codespaces](https://github.com/k-candidate/codespaces).  
You need `.devcontainer/devcontainer.json` (for the codespace container config), `.vscode/tasks.json` (to show the jupyter url with the token), and a script to start jupyter `.devcontainer/start-jupyter.sh`.

## Operations and Security

- By default, a Codespace stops after 30 minutes of inactivity. You can change your personal default timeout in GitHub settings, and the allowed range is 5 to 240 minutes.
- Files in an existing Codespace (including a virtual environment under `${workspaceFolder}/.venv`) are preserved while that Codespace exists. Deleting the Codespace removes its storage.
- Setting `"UV_LINK_MODE": "copy"` tells `uv` to copy files rather than use hard links, which can avoid link-related issues in containerized environments.
- Store sensitive values as Codespaces development-environment secrets in **Settings** → **Secrets and variables** → **Codespaces**, rather than hardcoding them into repository files. Secrets are exposed to the Codespace as environment variables when it is created or resumed.
- You made changes to `.devcontainer/devcontainer.json`. Go to the command palette and choose "Codespaces: Rebuild Container", and you're ready to roll. If the file is saved, it takes effect, no need to commit and push beforehand. If you don't have "autosave" in your VSCode then enable it. I tested this from the desktop app with the codespaces extension.
- Command palette --> "Codespaces: View Creation Log" if you need to troubleshoot.
- Command palette --> "Codespaces: Stop Current Codespace".