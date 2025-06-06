import logging
from moviepy.editor import TextClip
import unicodedata
import re
import multiprocessing

def normalize_text(text):
    # Replace em dashes and en dashes with periods
    text = text.replace("—", ".").replace("–", ".")
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # Remove any remaining non-ASCII characters
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    # Remove invisible control characters
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
    return text

def _create_textclip_safe(args):
    # Helper for multiprocessing timeout
    chunk_text, font_size, normal_color, video_height, chunk_start, chunk_duration = args
    try:
        clip = (
            TextClip(
                txt=chunk_text,
                fontsize=font_size,
                font="DejaVu-Sans",
                color=normal_color,
                stroke_color="black",
                stroke_width=2,
                size=(1000, None),
                method="caption"
            )
            .set_start(chunk_start)
            .set_duration(chunk_duration)
            # DO NOT call .set_position() here!
        )
        return clip
    except Exception as e:
        return e

def generate_highlighted_captions(conversation_lines, font_size=70, normal_color="white", highlight_color="yellow", video_height=1920, timeout=10):
    """
    Generates TextClips for subtitles, displaying three words at a time, with duration weighted by character count and an enlarging animation.
    """
    logging.info("Generating 3-word captions for %d lines.", len(conversation_lines))
    caption_clips = []

    for line_idx, line in enumerate(conversation_lines):
        text = normalize_text(line["text"])
        start_time = line["start_time"]
        duration = line['duration']

        words = text.split()
        if not words:
            logging.warning("Line %d is empty, skipping.", line_idx)
            continue

        total_chars = sum(len(word) for word in words)
        logging.info("Line %d: '%s' (%d words, %d chars, %.2fs)", line_idx, text, len(words), total_chars, duration)

        # Calculate per-word durations
        word_durations = [
            duration * (len(word) / total_chars) if total_chars > 0 else 0
            for word in words
        ]

        chunk_start = start_time
        i = 0
        while i < len(words):
            chunk_words = words[i:i+3]
            chunk_duration = sum(word_durations[i:i+3])

            # Before creating the TextClip, always normalize:
            chunk_text = " ".join(normalize_text(w) for w in chunk_words)

            # Log the normalized text
            logging.debug("Normalized chunk text: %r", chunk_text)

            # Skip empty or whitespace-only chunks
            if not chunk_text.strip():
                logging.warning("Chunk text is empty after normalization, skipping. Line %d, words %d-%d", line_idx, i, i+len(chunk_words)-1)
                chunk_start += chunk_duration
                i += 3
                continue

            try:
                word_clip = (
                    TextClip(
                        txt=chunk_text,
                        fontsize=font_size,
                        font="Arial",
                        color=normal_color,
                        stroke_color="black",
                        stroke_width=2,
                        size=(1000, None),
                        method="caption"
                    )
                    .set_start(chunk_start)
                    .set_duration(chunk_duration)
                    .set_position(("center", int(video_height * 0.18)))
                    .resize(lambda t: 1 + 0.1 * min(t, 0.3) / 0.3)
                )
                caption_clips.append(word_clip)
                logging.info("Created TextClip for chunk '%s' (line %d, words %d-%d)", chunk_text, line_idx, i, i+len(chunk_words)-1)
            except Exception as e:
                logging.error("Failed to create TextClip for chunk '%s' (line %d, words %d-%d): %s", chunk_text, line_idx, i, i+len(chunk_words)-1, e)

            chunk_start += chunk_duration
            i += 3

    logging.info("Generated %d caption clips.", len(caption_clips))
    return caption_clips