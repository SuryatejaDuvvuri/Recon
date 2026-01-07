# Project Recon(WIP)

> An agentic code reviewer that scouts your PR, gathers context, and tells humans where to focus. Project is work in progress.

## Quick Start
```bash
# Clone
git clone https://github.com/YOUR_USERNAME/recon.git
cd recon

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
uvicorn src.main:app --reload
```

## Project Structure
```
src/
├── agent/      # Agent logic and tools
├── review/     # Review processing
├── webhook/    # GitHub webhook handling
├── main.py     # FastAPI entry point
└── config.py   # Configuration
```

## License

MIT