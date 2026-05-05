---
name: "micromamba-env"
description: "Activate micromamba environments in Trae sandbox. Invoke when you need to use tools from micromamba environments (node, npm, defuddle, pdf-to-markdown, etc.) or when commands fail with 'not recognized' errors."
---

# Micromamba Environment Activation

Provides the correct procedure to activate micromamba environments within the Trae sandbox, where `micromamba activate` and direct PATH access may not work.

## Key Paths

| Item | Path |
|------|------|
| Micromamba executable | `D:\Scoop\apps\micromamba\2.5.0-1\micromamba.exe` |
| llm-wiki environment | `D:\micromamba-envs\llm-wiki\` |
| Node.js (in llm-wiki) | `D:\micromamba-envs\llm-wiki\node.exe` |
| npm (in llm-wiki) | `D:\micromamba-envs\llm-wiki\npm.cmd` |

## Activation Method

The sandbox does not support `micromamba activate` or `conda activate`. Instead, prepend the environment's directory to `$env:PATH`:

```powershell
$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH
```

After this, all tools installed in the `llm-wiki` environment become available:

```powershell
node --version    # v25.8.2
npm --version     # 11.11.1
defuddle --version
pdf-to-markdown --version
```

## Common Tools in llm-wiki Environment

| Tool | Purpose |
|------|---------|
| `node` / `npm` | JavaScript runtime and package manager |
| `defuddle` | Extract clean markdown from web pages (`npm install -g defuddle`) |
| `pdf-to-markdown` | Convert PDF to markdown with images |
| `pdftotext` | Extract plain text from PDF |

## Troubleshooting

### "not recognized" errors

If a command like `node`, `npm`, `defuddle`, or `micromamba` fails with "not recognized", it means the environment is not in PATH. Apply the activation command above.

### micromamba run fails with permission errors

`micromamba run --name llm-wiki` may fail with sandbox permission errors. Use the PATH prepend method instead.

### Finding micromamba executable

```powershell
Get-ChildItem "D:\" -Filter "micromamba.exe" -Recurse -ErrorAction SilentlyContinue -Depth 4 | Select-Object FullName
```

### Listing available environments

```powershell
& "D:\Scoop\apps\micromamba\2.5.0-1\micromamba.exe" env list
```

### Checking packages in an environment

```powershell
& "D:\Scoop\apps\micromamba\2.5.0-1\micromamba.exe" list --name llm-wiki
```

### Finding a specific executable in an environment

```powershell
Get-ChildItem "D:\micromamba-envs\llm-wiki" -Filter "node.exe" -Recurse -ErrorAction SilentlyContinue -Depth 3 | Select-Object FullName
```

## Pattern for Commands

When running a command that requires the micromamba environment, always prepend the PATH activation in the same command:

```powershell
$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH; <your-command>
```

Examples:

```powershell
# Extract markdown from a web page
$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH; defuddle parse "https://example.com" --md -o output.md

# Convert PDF to markdown
$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH; pdf-to-markdown "input.pdf" -o "output.md" --images-dir images --dpi 900 --language en

# Install a global npm package
$env:PATH = "D:\micromamba-envs\llm-wiki;" + $env:PATH; npm install -g defuddle
```
