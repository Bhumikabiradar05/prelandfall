param([switch]$Demo, [int]$Port = 8000)
$ErrorActionPreference = 'Stop'
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
  throw 'Python 3.11+ is required. Install it from python.org, then rerun this command.'
}
if (-not (Test-Path '.venv')) { python -m venv .venv }
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
if ($Demo) { & .\.venv\Scripts\python.exe app.py --demo --port $Port } else { & .\.venv\Scripts\python.exe app.py --port $Port }
