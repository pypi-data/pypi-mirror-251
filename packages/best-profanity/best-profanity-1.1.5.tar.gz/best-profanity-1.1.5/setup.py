from pathlib import Path
import setuptools

long_description = Path("README.md").read_text(encoding="utf8")

setuptools.setup(
    name="best-profanity",
    version="1.1.5",
    author="Victor Zhou, 2021 Menelaos Kotoglou, Dimitrios Mistriotis, and Joey Nicole Mindo",
    author_email="joeynicole99@gmail.com",
    description=(
        "An efficient, and accurate machine learning model for detecting profane or vulgar terminology in both English and Filipino languages, including current Gen Z slang and expressions."
    ),
    packages=setuptools.find_packages(),
    install_requires=["scikit-learn==1.3.2", "joblib>=1.3.2"],
    python_requires=">=3.8",
    package_data={
        "best_profanity": [
            "data/tagalog-model.joblib",
            "data/tagalog-vectorizer.joblib",
            "data/english-vectorizer.joblib",
            "data/english-model.joblib",
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
