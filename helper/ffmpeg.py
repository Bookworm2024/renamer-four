import subprocess, json
from helper.utils import metadata_text


def change_metadata(input_file, output_file, metadata):
    author, title, video_title, audio_title, subtitle_title = metadata_text(metadata)

    # Probe streams once so we can target per-stream titles.
    try:
        output = subprocess.check_output(
            ['ffprobe', '-v', 'error', '-show_streams', '-print_format', 'json', input_file]
        )
        streams = json.loads(output).get('streams', [])
    except Exception as e:
        print("ffprobe error:", e)
        streams = []

    cmd = [
        'ffmpeg', '-y',
        '-i', input_file,
        '-map', '0',
        '-c', 'copy',          # stream-copy everything → no re-encode → instant
        '-metadata', f'title={title}',
        '-metadata', f'author={author}',
    ]

    for stream in streams:
        idx = stream.get('index')
        codec = stream.get('codec_type')
        if codec == 'video' and video_title:
            cmd += [f'-metadata:s:{idx}', f'title={video_title}']
        elif codec == 'audio' and audio_title:
            cmd += [f'-metadata:s:{idx}', f'title={audio_title}']
        elif codec == 'subtitle' and subtitle_title:
            cmd += [f'-metadata:s:{idx}', f'title={subtitle_title}']

    cmd += ['-metadata', 'comment=Renamed via Trinity Mods · @trinityXmods']
    cmd += ['-f', 'matroska']   # container that accepts all stream types
    cmd.append(output_file)

    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print("FFmpeg error:", e.stderr)
        return False
