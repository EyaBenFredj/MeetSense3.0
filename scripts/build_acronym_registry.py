# scripts/build_acronym_registry.py
import json
from pathlib import Path
from tools.acronym_seed import ACRONYMS

def main():
    project_root = Path(__file__).resolve().parents[1]
    data_dir = project_root / "data"
    data_dir.mkdir(exist_ok=True)

    # validate & normalize to dict short->long
    reg = {}
    for item in ACRONYMS:
        short = str(item["short"]).strip()
        long  = str(item["long"]).strip()
        if not short or not long:
            continue
        reg[short] = long

    out = data_dir / "acronyms.json"
    out.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Wrote {out} with {len(reg)} acronyms")

if __name__ == "__main__":
    main()
