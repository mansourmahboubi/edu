# https://github.com/openai/whisper/blob/main/model-card.md
import json

import whisper

audio_file = "s1e1.mp3"
data_file = audio_file.replace(".mp3", ".json")
final_data = f"{audio_file.replace('.mp3', '')}-final.json"
srt_file = f"{audio_file.replace('.mp3', '')}-final.srt"


def transcribe_audio(audio_file: str) -> None:
    model = whisper.load_model("turbo")
    result = model.transcribe(audio_file, word_timestamps=True, verbose=False)
    data = json.dumps(result, indent=4)
    with open(data_file, "w") as f:
        f.write(data)


def audiofile_loader(data_file: str) -> None:
    updated_data = []
    with open(data_file, "r") as f:
        data = json.load(f)
    for segment in data["segments"]:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        updated_data.append({"start": start, "end": end, "text": text})
    with open(final_data, "w") as f:
        f.write(json.dumps(updated_data, indent=4))


def convert_to_srt(data_file: str) -> None:
    with open(data_file, "r") as f:
        data = json.load(f)

    srt_file_data = ""
    for index, segment in enumerate(data, 1):  # Start enumeration from 1
        # Convert seconds to SRT time format (HH:MM:SS,mmm)
        start_time = format_timestamp(segment["start"])
        end_time = format_timestamp(segment["end"])
        text = segment["text"]

        # Format each subtitle entry
        srt_file_data += f"{index}\n{start_time} --> {end_time}\n{text}\n\n"

    with open(
        data_file.replace(".json", ".srt"),
        "w",
        encoding="utf-8",
    ) as f:
        f.write(srt_file_data)


def format_timestamp(seconds: float) -> str:
    """Convert seconds to SRT timestamp format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


if __name__ == "__main__":
    # transcription = transcribe_audio(audio_file)
    # audiofile_loader(data_file)
    convert_to_srt(final_data)
    # print(transcription)


if __name__ == "__main__":
    # transcription = transcribe_audio(audio_file)
    # audiofile_loader(data_file)
    convert_to_srt(final_data)
    # print(transcription)
