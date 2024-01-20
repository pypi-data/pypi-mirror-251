from setuptools import setup, find_packages

VERSION = '0.1.0' 
DESCRIPTION = 'Generative Artificial Intelligence'
LONG_DESCRIPTION = 'Utilizing Generative Artificial Intelligence models like "GPT-4" and "Gemini Pro" as coding and writing assistants for "Python" users. Through these models, "GenAIPy" offers a variety of functions, encompassing text generation, code optimization, natural language processing, chat, and image interpretation. The goal is to aid "Python" users in streamlining laborious coding and language processing tasks.'

setup(
        name="GeAI", 
        version=VERSION,
        author="Li Yuan",
        author_email="<lyuan@gd.edu.kg>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[],
        keywords=['Generative AI', 'LLM', 'API'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)