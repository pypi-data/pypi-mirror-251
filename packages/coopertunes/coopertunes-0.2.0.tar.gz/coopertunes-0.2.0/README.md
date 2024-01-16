# coopertunes
Hub for music machine learning  generating audio

Amazing README coming soon!

# Installation

It is recommended to use conda environment for setup `coopertunes` module. To install conda on your machine follow [this](https://conda.io/projects/conda/en/stable/user-guide/install/linux.html) instruction. If you already have conda installed create a virtual environment"

`conda create -n coopertunes python=3.10`

and activate it:

`conda activate coopertunes`

Clone coopertunes repository:

`git clone git@github.com:Szakulli07/coopertunes.git`
`cd coopertunes`
`conda develop .`

Before install `coopertunes` module you need to install `pytorch` framework. It is recommended to install version `2.0.1`:

`pip install torch==2.0.1 torchaudio==2.0.2 --index-url https://download.pytorch.org/whl/cu118`

Now you need to install `coopertunes` module:

`pip install -e .`

# Knowledge

There are some things worth acknowledging before starting to work with "coopertunes". We will list most relevant

## Repo concepts

Generally we try to make clean structure which will be similar for all models.

1. HParams - those are classes where all your hyper parameters should be stored. It is beneficiall to have it in one place because it allows you for easy tracking. Both in debugging you don't need to go through 4 classes before finding out from when some hparam is and in anaylising. You simply dump hparam to file and that's all what you need to describe your experiment for reproducibility.
2. Models - files with models architecture. Try to have all thing connected with one model in one module or if possible in one file. Like in [hugging face transformers](https://huggingface.co/docs/transformers/index). It also allows for easier debugging and make models less dependent. For example many models might have ResidualLayer but probably everywhere it would look different.
3. Datasets - nothing fancy there. Just classes allowing working with data. Generally don't be afraid to make as many specific datasets as you need.
4. Supervisors - clue of this repo. Those are classes that allows models training. Their task is to load data, train models, save checkpoints logg metrics ang generally everything that is needed for training model. Having such class separate from model itself make further inferencing model less clutered.
5. Datatools - som functions and tools in general for managing datasets for given model. By using this, You should be able to download and preprocess dataset for given models. 

## Repo automation

The basis of the effective work is automation. For now there are not many but still try to use it and upgrade it.

1. Code quality - [pylint](https://pypi.org/project/pylint/), [pycodestyle](https://pypi.org/project/pycodestyle/), [mypy](https://pypi.org/project/mypy/). They all help you in making code prettier. What's more it allows for finding out errors before them happened (What makes python beutifull is dynamic typing. What makes python horrible is dynamic typing)
2. Versioning - [release-please](https://github.com/google-github-actions/release-please-action) is a pipe that create changelog based on your [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/). When you want to change repo version simply commit `fix`, `feat` or `!`. 

In the future there should be pipes like automatic tests, building dokcer images, serving models and so on.

## Libriaries

We take advantage of many python libs. Some of them are worth mentioning and spending some time learning.

1. [torch-summary](https://pypi.org/project/torch-summary/) - easiest from the list. It allows you for pretty logging your model. All its layers, parameters and others. It's nice get first insides.
2. [einops](https://einops.rocks/) - if you do not like `x.view(0, 2, 3, 1)` this lib is for you. It allows for many nicer operations for example `rearrange`. You can change shape like `x, 'b c t -> 1 b (c t)`. Simply you won't need all those comments you wrote near those pesky operations to keep in mind what is tensor shape at this moment.
3. [librosa](https://librosa.org/doc/main/index.html) - audio bible. Everything you need with audio (unless you want to propagate audio through it...). Simply all data preparations and visualizations is possible thx to it. It is also standard lib that most big research center uses.
4. [deepspeed](https://github.com/microsoft/DeepSpeed) - multi gpu training, multi node training, multiple precisions, ZeRO optimizations and many more. Generally when you start training models that can't be trained during 1.5h on google collab you will probably need it.
5. [pretty_midi](https://pypi.org/project/pretty_midi/) - library designed for handling MIDI (Musical Instrument Digital Interface) files in a user-friendly and efficient manner. It allows us to easily manipulate MIDI data, including reading, writing, and visualizing MIDI files, as well as extracting musical information such as notes, instruments, and timing details.

## Models

For now we included/are including 5 models. Some inside about them.

* MelSpecVAE - we used [moisehorta](https://github.com/moiseshorta/MelSpecVAE) (the classic one) implementation as the baseline. Originally it was some autogenerated notebooks in tensorflow. Now it is biggest [VAE](https://medium.com/@rekalantar/variational-auto-encoder-vae-pytorch-tutorial-dce2d2fe0f5f) ever existed. We make it torch. We add it some nice features like [gradient cliping](https://medium.com/@nerdjock/deep-learning-course-lesson-10-6-gradient-clipping-694dbb1cca4c), [gradient accumulation](https://lightning.ai/blog/gradient-accumulation/), [lr scheduler](https://www.google.com/search?q=learning+rate+scheduler&oq=learning+rate+s&gs_lcrp=EgZjaHJvbWUqBwgAEAAYgAQyBwgAEAAYgAQyBwgBEAAYgAQyBggCEEUYOTIICAMQABgWGB4yCAgEEAAYFhgeMggIBRAAGBYYHjIICAYQABgWGB4yCAgHEAAYFhgeMggICBAAGBYYHjIICAkQABgWGB7SAQg1MzUyajBqNKgCALACAA&sourceid=chrome&ie=UTF-8)... And it is still not working. It is just simple VAE that generate mel spectrograms from noise. It assumes that if something is near in latent space it will be near in mel spec space. And this assumption is just bad. Mayby you can use it to really easy techno but that's all.
* MelSpecVQVAE - it is addition we propose to normal MelSpecVAE that utilize [VQ](https://en.wikipedia.org/wiki/Vector_quantization). It is nice technique that says hey mayby world does not need to be as much contigues. Generally now it is common trend and its more complicated variations (RVQ and friends) are used in all SOTA networks like [Soundstream](https://blog.research.google/2021/08/soundstream-end-to-end-neural-audio.html) or [Encodec](https://github.com/facebookresearch/encodec). For now it can be used like MelSpecVAE - generate mels from noise but we think it could be used in style transfer with more success.
* MelGAN - very good vocoder. It is used to create raw audio from mel spectrograms. There are better options like [HiFiGAN](https://github.com/jik876/hifi-gan) and many more complicated but MelGAN advantage is its simplicity. Many vocoders utilize [GAN](https://machinelearningmastery.com/what-are-generative-adversarial-networks-gans/) ideas so it is worth knowing this approach. To run succesfull training you will probably one about 10-60h and 2 weeks of GPU. Just remember you will quickly hear MelGAN producing "good" results but put on speakers and listen carefully because we are aiming for "very good"
* PerformanceRNN - As said in original publicztion: ..."Performance RNN, an LSTM-based recurrent neural network designed to model polyphonic music with expressive timing and dynamics.". It is able to recreate sequences learned from midi files, and create guided midis itself. Main backbone of this network is Gated Recurent Unit.
* PerformanceRNNattentive - As PerformanceRNN is generating note after note for each context, we utilized self attention module to all GRU's inputs. It allowed model to create music with more "piano keys pressed" at the same time, and overall better quality (in our opinion) in the same number of epochs as PerformanceRNN. 
* GANSynth - based on [GANSynth](https://arxiv.org/pdf/1902.08710.pdf) which is [PGGAN](https://arxiv.org/pdf/1710.10196.pdf)
used for generating spectrograms from noise for music with [ACGAN](https://arxiv.org/pdf/1610.09585.pdf) pitch conditioning.
Author's implementation is part of [Google Magenta](https://magenta.tensorflow.org/) which is developed using tensorflow. This 
project should be one of the first GANSynth implementation in [Pytorch](https://pytorch.org/). GANSynth is trained on
[NSynth](https://magenta.tensorflow.org/datasets/nsynth) dataset. GANSynth is one of the biggest model in the project, because of 
computational limits we couldn't benchmark it.

## Future works

In this section we would like to write some things about our opinions what could be done with this repo and how to work with it. It could be easly given to 6 people team or several smaller ones. 

1. Adding newer models. For now we add some rather old ones that are rather for showing purpose. Currently in era of [VALL-E](https://www.microsoft.com/en-us/research/project/vall-e-x/) or [AudioBox](https://audiobox.metademolab.com/) concentraining on one SOTA model (without open implementation) is also time consuming option.
2. Refactor and standarization. Currently many things needs some touches. Adding deepseed to all models, standarizing checkpoitning, decuplication... those are things that could be done. I would also combine this one with serving repo on [docker hub](https://hub.docker.com/) and on [HuggingFace](https://huggingface.co/spaces/HumanAIGC/OutfitAnyone/discussions).
3. Add more automated data processing for each model. In future data should be automatically downloaded and preprocessed, if directory pointed by hparams is empty. 