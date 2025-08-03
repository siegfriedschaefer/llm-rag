Of course, here is a more formally structured version of your `README.md` file.

***

# Semantic File Comparison using LLMs

## Motivation

The idea for this project was born from a practical need. My son was faced with the task of understanding the changes in a new version of the German industry standard DIN 4108-2, titled "Thermal protection and energy economy in buildings – Part 2: Minimum requirements to thermal insulation."

Theoretically, leveraging Large Language Models (LLMs) to semantically compare two document versions should be a straightforward task. This project was started to put that theory into practice.

## The Challenge

It quickly became apparent that the initial assumption was wrong. The primary challenge was not the semantic comparison itself, but the preliminary step of reliably extracting clean text from PDF documents using local Python libraries.

## Findings

Several libraries were evaluated for document parsing, with the following observations:

* **Finding a suitable local Python module for reading complex documents is non-trivial.**
* **`pypdf`**: While functional, this library proved to be the weakest in interpreting the specific documents used. It introduced several rendering artifacts and unusual character encodings.
* **`fitz` (PyMuPDF)**: This library provided the best results out of the box, handling the documents with greater accuracy.
* **`LlamaIndex`**: This library was considered, but its dependency on `nltk` (and its subsequent dependencies) presented a setup overhead that was too time-consuming for the initial phase of this project.

## Decision

Given the findings, the project will proceed using the **`fitz`** library for all document parsing and text extraction tasks.

