from moviepy.editor import ImageClip, AudioFileClip
import os

def create_character_image_clip(character_image_path, audio_file_path, start_time, position=("left", "bottom"), height=400):
    """
    Creates an ImageClip for a character that appears at start_time
    and lasts as long as the associated audio file.

    Args:
        character_image_path (str): Path to the character image (png)
        audio_file_path (str): Path to the audio file (mp3)
        start_time (float): Start time (in seconds) for image appearance
        position (tuple): Position on screen (default left/bottom or right/bottom)
        height (int): Height to resize image to (maintains aspect ratio)

    Returns:
        ImageClip: Configured image clip object
    """
    if not os.path.exists(audio_file_path):
        raise FileNotFoundError(f"Audio file not found: {audio_file_path}")
    
    if not os.path.exists(character_image_path):
        raise FileNotFoundError(f"Image file not found: {character_image_path}")

    duration = AudioFileClip(audio_file_path).duration
    
    image_clip = (
        ImageClip(character_image_path, transparent=True)
        .set_start(start_time)
        .set_duration(duration)
        .resize(height=height)
        .set_position(position)
    )

    return image_clip

def generate_character_image_clips(conversation_lines, image_map):
    """
    Given conversation lines and a mapping of character names to image paths,
    create timed ImageClips for each line's character.

    Args:
        conversation_lines (list): List of dicts with 'character', 'audio_file', 'start_time'
        image_map (dict): Mapping of character names to image paths

    Returns:
        list: List of ImageClips
    """
    image_clips = []

    for line in conversation_lines:
        character = line["character"]
        audio_file = line["audio_file"]
        start_time = line["start_time"]

        if character not in image_map:
            continue  # skip if no image available

        position = ("left", "bottom") if character == "Peter" else ("right", "bottom")

        clip = create_character_image_clip(
            character_image_path=image_map[character],
            audio_file_path=audio_file,
            start_time=start_time,
            position=position
        )
        image_clips.append(clip)

    return image_clips
