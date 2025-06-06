from scripts.script_generation import generate_conversation
from scripts.tts_conversion import text_to_speech
from scripts.character_images import generate_character_image_clips
from scripts.caption_generation import generate_highlighted_captions
from scripts.audio_video_stitching import combine_audio_video
import os
from moviepy.editor import TextClip
import moviepy.config as mpy_conf
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

mpy_conf.change_settings({"IMAGEMAGICK_BINARY": "C:/Program Files/ImageMagick-7.1.1-Q16-HDRI/magick.exe"})

AUDIO_DIR = "assets/audio"
VIDEO_PATH = "assets/parkour_video.mp4"
IMAGE_MAP = {
    "Peter": "assets/peter.png",
    "Stewie": "assets/stewie.png"
}
FINAL_VIDEO_PATH = "final_videos/final_output.mp4"

def main():
    logging.info("Starting main process.")
    os.makedirs(AUDIO_DIR, exist_ok=True)
    convo = generate_conversation()
    logging.info(f"Generated conversation with {len(convo)} lines.")

    current_time = 0
    conversation_lines = []
    audio_files = []

    for idx, line in enumerate(convo):
        audio_file = f"{AUDIO_DIR}/line_{idx}_{line['character']}.mp3"
        if os.path.exists(audio_file):
            logging.info(f"Audio already exists for {line['character']}: '{audio_file}', skipping TTS.")
        else:
            logging.info(f"Generating TTS for {line['character']}: '{line['text']}' -> {audio_file}")
            text_to_speech(line['character'], line['text'], audio_file)

        from moviepy.editor import AudioFileClip
        duration = AudioFileClip(audio_file).duration
        logging.info(f"Audio duration for line {idx}: {duration:.2f}s")

        conversation_lines.append({
            "character": line['character'],
            "text": line['text'],
            "audio_file": audio_file,
            "start_time": current_time,
            "duration": duration
        })
        audio_files.append(audio_file)
        current_time += duration

    logging.info("Generating character image clips.")
    image_clips = generate_character_image_clips(conversation_lines, IMAGE_MAP)
    logging.info("Generating highlighted captions.")
    caption_clips = generate_highlighted_captions(conversation_lines)

    logging.info("Combining audio, video, images, and captions.")
    combine_audio_video(VIDEO_PATH, audio_files, image_clips, caption_clips, FINAL_VIDEO_PATH)
    logging.info(f"✅ Video created: {FINAL_VIDEO_PATH}")

if __name__ == "__main__":
    main()
