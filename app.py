import time
from pathlib import Path

import gradio as gr
import onnxruntime as rt
from audio_separator import Separator
from pydub import AudioSegment
from pytube import YouTube

available_model = ["UVR-MDX-NET-Inst_HQ_3", "UVR-MDX-NET-Voc_FT", "UVR_MDXNET_KARA_2", "Kim_Vocal_2", "UVR_MDXNET_Main"]
base_path = Path(__file__).parent

def reduce_audio_size(audio_path):
    s1 = AudioSegment.from_file(audio_path)
    s1.export(audio_path, format="mp3", bitrate="64k")


def audio_sep(youtube_url, audio_path, separation_model, separation_mode, progress=gr.Progress()):
    out_folder = base_path / "audio_filtered"
    out_folder.mkdir(exist_ok=True)
    temp_folder = base_path / "tmp"
    temp_folder.mkdir(exist_ok=True)

    print(youtube_url)
    print(audio_path)
    print(separation_model)
    print(separation_mode)

    youtube_url = youtube_url.strip()
    if youtube_url is not None and youtube_url != "":
        try:
            print("Downloading YouTube audio...")
            yt = YouTube(youtube_url)
            video_id = yt.video_id
            save_audio_path = temp_folder / f"{video_id}.mp3"
            if yt.length > 5 * 60:
                raise gr.Error("Video too long. Please use a video shorter than 5 minutes.")
            stream = yt.streams.filter(only_audio=True).order_by("abr").desc().first()
            stream.download(filename=str(save_audio_path))
            audio_path = str(save_audio_path)
            print("Downloaded YouTube audio")
        except:
            gr.Info("Something went wrong. Skipping to second input.")

    if audio_path is None:
        gr.Info("Please input an audio file or YouTube URL.")
        return None, None

    if len(separation_mode) == 1:
        separation_mode = separation_mode[0]
    elif len(separation_mode) == 0:
        return None, None
    else:
        separation_mode = None
    progress(0, desc="Starting...")
    separator = Separator(
        audio_path,
        model_name=separation_model,
        use_cuda=True if rt.get_device() == "GPU" else False,
        output_dir=str(out_folder),
        output_single_stem=separation_mode,
    )
    for i in progress.tqdm(range(50)):
        time.sleep(0.01)

    results = [out_folder / p for p in separator.separate()]
    print(results)

    for i in progress.tqdm(range(50, 100)):
        time.sleep(0.01)

    if separation_mode == "Instrument":
        instrument_stem_path = str(results[0])
        reduce_audio_size(instrument_stem_path)
        vocal_stem_path = None
    elif separation_mode == "Vocal":
        instrument_stem_path = None
        vocal_stem_path = str(results[0])
        reduce_audio_size(vocal_stem_path)
    else:
        if "_(Instrumental)_" in str(results[0]):
            instrument_stem_path = str(results[0])
            reduce_audio_size(instrument_stem_path)
            vocal_stem_path = str(results[1])
            reduce_audio_size(vocal_stem_path)
        else:
            vocal_stem_path = str(results[0])
            reduce_audio_size(vocal_stem_path)
            instrument_stem_path = str(results[1])
            reduce_audio_size(instrument_stem_path)
    return instrument_stem_path, vocal_stem_path


gr.Interface(
    audio_sep,
    [
        gr.Textbox(
            label="YouTube video URL (No videos more than 5 mins)",
            placeholder="https://www.youtube.com/watch?v=XXXXXXXXXXX",
        ),
        gr.Audio(label="Audio Input", type="filepath"),
        gr.Dropdown(available_model, label="Separation Model", value="UVR_MDXNET_KARA_2"),
        gr.CheckboxGroup(choices=["Instrument", "Vocal"], label="Separation Mode", value=["Instrument", "Vocal"]),
    ],
    [gr.Audio(label="Music/Instrument Output", type="filepath"), gr.Audio(label="Vocal Output", type="filepath")],
    title="Audio Separator",
    description="<center>Separate the music and vocal from the input audio</center>",
    allow_flagging=False,
).queue().launch(share=False, favicon_path=base_path / "audiomack.svg")
