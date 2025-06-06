from moviepy.editor import TextClip, AudioFileClip

def generate_highlighted_captions(conversation_lines, font_size=70, normal_color="white", highlight_color="yellow"):
    """
    Generates TextClips for subtitles where each word is highlighted as it is spoken.

    Args:
        conversation_lines (list): List of dicts with 'text', 'audio_file', 'start_time'
        font_size (int): Font size for captions
        normal_color (str): Color for non-highlighted text
        highlight_color (str): Color for highlighted word

    Returns:
        list: List of TextClips with timed highlighting
    """
    caption_clips = []

    for line in conversation_lines:
        text = line["text"]
        start_time = line["start_time"]
        audio_file = line["audio_file"]
        duration = AudioFileClip(audio_file).duration

        words = text.split()
        if not words:
            continue

        word_duration = duration / len(words)

        for i, word in enumerate(words):
            before_words = " ".join(words[:i])
            after_words = " ".join(words[i+1:])

            # Build full text string with current word highlighted
            display_text = f"{before_words} {word} {after_words}".strip()

            word_clip = (
                TextClip(
                    txt=display_text,
                    fontsize=font_size,
                    font="Arial-Bold",
                    color=highlight_color,  # highlight current word
                    stroke_color="black",
                    stroke_width=2,
                    size=(1000, None),
                    method="caption"
                )
                .set_start(start_time + i * word_duration)
                .set_duration(word_duration)
                .set_position(("center", 1600))
            )

            caption_clips.append(word_clip)

    return caption_clips
