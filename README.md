# Automated Content Generator - StudySmart

This is a basic prototype of an automated content generation system using Python and GPT-based models. 

## Project structure

Our repository is organized as follows:

```
.
├── doc
│   ├── image_captioning.ipynb
│   └── poc.ipynb
├── LICENSE
├── poetry.lock
├── pyproject.toml
├── README.md
├── script.py
└── src
    ├── core
    │   ├── prompts.py
    │   └── __pycache__
    │       └── prompts.cpython-311.pyc
    └── dataset
        ├── test_keywords.csv
        ├── arduino-uno.jpg
        └── volcano-erupting.jpg
```

### Documentation

All the Jupyther notebooks (`*.ipynb`) under the `/doc` directory contains the documentation, experiments and explanations of every decision for the final script. Please consider reading and executing them.

### Source directory

Directory that contains the dataset and file elements used in the testing notebooks and final script. 

It also contains the core directory, which holds the prompts used in the final script and the chat_completions functions. The `/core` code is meant for organizational reasons, i.e. keep the final `script.py` clean and organized.

## Installing the dependencies

In this project, it's used Poetry as the dependency manager. Reference documentation: [https://python-poetry.org](https://python-poetry.org). To install the required dependencies run the command below:

```
poetry install --no-root
```

## Run the script

To understand how to run the script, run `poetry run python script.py --help`

```
usage: script.py [-h] -m {article_gen,image_caption} [-k KEYWORDS_FILE] [-i IMAGE] -o OUTPUT

Automated Content Generation Tool

options:
  -h, --help            show this help message and exit
  -m {article_gen,image_caption}, --mode {article_gen,image_caption}
                        Mode of operation: 'article_gen' to generate articles, 'image_caption' to generate captions for images.
  -k KEYWORDS_FILE, --keywords-file KEYWORDS_FILE
                        Path to the keywords CSV file (required for article generation mode).
  -i IMAGE, --image IMAGE
                        Path to the image file (required for image captioning mode).
  -o OUTPUT, --output OUTPUT
                        Path to the output JSON file.
```

If you want to generate an SEO-friendly article, you can do as follow:

```
poetry run python script.py -m article_gen -k src/dataset/test_keywords.csv -o output.json
```

If you want to generate an image caption, you can do as follow:

```
poetry run python script.py -m image_caption -i src/dataset/volcano-erupting.jpg -o output.json
```