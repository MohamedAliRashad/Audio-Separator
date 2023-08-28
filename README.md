![audio_sep](https://github.com/MohamedAliRashad/Audio-Separator/blob/main/audio_sep.png)

# <img src = "https://github.com/MohamedAliRashad/Audio-Separator/blob/main/audiomack.svg" alt="Audio Separator" width="35"/> Audio-Separator
Simple [Gradio](https://www.gradio.app/) Application that separates vocals from instruments in an Input Audio (or YouTube Video) 🤠

Try the app here [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/MohamedRashad/Audio-Separator) (Slow) or **Deploy it yourself with your GPU**.

## ✨ How to Run ?
1. Clone the Repo `git clone https://github.com/MohamedAliRashad/Audio-Separator.git`
1. Enter the Repo directory `cd Audio-Separator`
1. Install the requirements `pip install -r requirements.txt`
1. Run the App `python app.py`

**Note:** If anything wrong happened or you are afraid that the applicaition will cause problems for your other projects.
Try and use a [venv](https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/) to setup the app in.

## 👷 How to use ?
- If there is a youtube video you want to separat the vocals and music in. Just add its URL in the first input field.
- If you already have an audio you want to upload for separation. Just upload it in the second input field (Make sure to leave the first field empty).
- The separation models that has the word **Vocal** in it is better in separating the vocals in the audio and vica versa with the word **Inst**

## 📓 Citations
```bibtex
@misc{karaoken92:online,
author = {},
title = {karaokenerds/python-audio-separator: Easy to use vocal separation on CLI or as a python package, using the amazing MDX-Net models from UVR trained by @Anjok07},
howpublished = {\url{https://github.com/karaokenerds/python-audio-separator}},
month = {},
year = {},
note = {(Accessed on 08/26/2023)}
}
```
