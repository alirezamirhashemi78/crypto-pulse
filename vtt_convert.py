import re
import os
import glob

def vtt_to_text(vtt_path, output_path=None):
    parts = []
    last_line = None

    with open(vtt_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()

            # Skip headers
            if not line:
                continue
            if line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
                continue

            # Skip timestamp lines
            if "-->" in line:
                continue

            # Remove YouTube karaoke tags <...>
            clean = re.sub(r"<[^>]+>", "", line).strip()
            if not clean:
                continue

            # Skip duplicate consecutive lines
            if clean == last_line:
                continue

            parts.append(clean)
            last_line = clean

    # Final joined text
    final_text = " ".join(parts)

    # If no output path was given, auto-generate it
    if output_path is None:
        base = os.path.splitext(vtt_path)[0]
        output_path = base + ".txt"

    # Save the output file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(final_text)

    return output_path


