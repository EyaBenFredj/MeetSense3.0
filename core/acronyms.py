# core/acronyms.py
import json, re
from pathlib import Path
from typing import Dict

_ARABIC_BLOCK = "\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF"
_WORD_CHARS = rf"0-9A-Za-z_{_ARABIC_BLOCK}"

def _load_registry() -> Dict[str, str]:
    project_root = Path(__file__).resolve().parents[1]
    path = project_root / "data" / "acronyms.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    # fallback to seed if JSON missing
    from tools.acronym_seed import ACRONYMS
    return {x["short"]: x["long"] for x in ACRONYMS}

class AcronymExpander:
    def __init__(self, reg: Dict[str, str]):
        self.reg = dict(reg)
        # sort by length desc to avoid partial overlaps
        keys = sorted(self.reg.keys(), key=len, reverse=True)
        if not keys:
            # match nothing
            self._rx = re.compile(r"^\b\B$")
        else:
            # unicode-aware boundaries (simple): not letter/number/underscore/Arabic around
            left  = rf"(?<![{_WORD_CHARS}])"
            right = rf"(?![{_WORD_CHARS}])"
            joined = "|".join(map(re.escape, keys))
            self._rx = re.compile(left + rf"({joined})" + right)

    def expand(self, text: str) -> str:
        """First mention: 'Long (SHORT)'; subsequent mentions: 'Long'."""
        if not text or not self.reg:
            return text

        seen = set()

        def repl(m: re.Match) -> str:
            short = m.group(1)
            long = self.reg.get(short, short)
            if short in seen:
                return long
            seen.add(short)
            # avoid double-expanding if already "long (short)" present
            return f"{long} ({short})"

        return self._rx.sub(repl, text)

# singleton (import and use everywhere)
_registry = _load_registry()
expander = AcronymExpander(_registry)
