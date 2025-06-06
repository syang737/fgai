from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_audioclips, CompositeVideoClip

def combine_audio_video(bg_video_path, audio_files, image_clips, caption_clips, output_path):
    video = VideoFileClip(bg_video_path)

    # Combine all audio tracks into one
    audio_clips = [AudioFileClip(a) for a in audio_files]
    total_audio = concatenate_audioclips(audio_clips)

    # Resize video to vertical (1080x1920) and match duration to audio
    video = video.set_audio(total_audio).subclip(0, total_audio.duration)
    video = video.resize(height=1920).crop(x_center=video.w / 2, width=1080)

    # Combine video, image overlays, and captions
    final_video = CompositeVideoClip([video] + image_clips + caption_clips, size=(1080, 1920))

    # Export final video
    final_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
