import re

input_path = "pw.txt"
output_path = "pw_processed.txt"

with open(input_path, encoding="utf-8") as f:
    lines = f.readlines()

# 1. From "Real-World Problem or Opportunity Identified in Project & Rationale":
#    - Cut next 3 lines
#    - Cut everything before it (keep this line and everything after, minus the next 3 lines)
start_idx = None
for i, line in enumerate(lines):
    if line.strip().lower() == "real-world problem or opportunity identified in project & rationale".lower():
        start_idx = i
        break

if start_idx is not None:
    # Skip the next 3 lines after the found line
    lines = lines[start_idx:start_idx+1] + lines[start_idx+4:]

# 6. Delete everything after line "reference list"
trimmed_lines = []
for line in lines:
    if line.strip().lower().startswith("reference list"):
        break
    trimmed_lines.append(line)
lines = trimmed_lines

# 2. Clear specific lines
clear_lines = [
    "Target Group of Project & Rational",
    "Proposed Ideas & Rationale",
    "Aim(s) of Project",
]
for i, line in enumerate(lines):
    if any(line.strip().lower().startswith(cl.lower()) for cl in clear_lines):
        lines[i] = "\n"

# 3. Clear any lines starting with "fig."
lines = ["" if line.strip().lower().startswith("fig.") else line for line in lines]

# 4. Delete any bracket () with a comma, year in it, OR it has "fig." in it,
# but do NOT remove brackets with a single word or number (no spaces) inside.
def remove_special_brackets(text):
    def replacer(match):
        content = match.group(1)
        # Only keep if it's a single word/number (no spaces)
        if re.fullmatch(r"\w+", content):
            return f"({content})"
        # Remove if it has a comma, year, or "fig."
        if ("," in content or
            re.search(r"\b\d{4}\b", content) or
            re.search(r"fig\.", content, re.IGNORECASE)):
            return ""
        return f"({content})"
    return re.sub(r"\(([^()]*)\)", replacer, text)

lines = [remove_special_brackets(line) for line in lines]

# 5. Delete any lines without a ".", "?", or "!" in them
lines = [line for line in lines if any(p in line for p in ".?!")]

with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(lines)

print(f"Processed file written to {output_path}")