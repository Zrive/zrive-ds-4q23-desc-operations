from transformers import pipeline
import pandas as pd

MODEL = "Azma-AI/bart-large-text-summarizer"


def generate_summary(description: str) -> str:
    """
    This function uses the "Azma-AI/bart-large-text-summarizer" model
    to perform summarization. If the input text is larger than the
    supported number of tokens, the original text will be split into
    fragments, and summarization will be applied to each fragment.

    description: the text to summarize
    """
    summarizer = pipeline("summarization", MODEL)

    if pd.notna(description) and len(description) > 3:
        max_length = 1024

        fragments = [
            description[i : i + max_length]
            for i in range(0, len(description), max_length)
        ]

        final_summary = ""

        for fragment in fragments:
            fragment_summary = summarizer(
                fragment, max_length=50, min_length=30, length_penalty=2.0, num_beams=4
            )
            final_summary += fragment_summary[0].get(
                "summary_text", fragment_summary[0].get("text", "")
            )

        final_summary = summarizer(
            final_summary,
            max_length=150,
            min_length=50,
            length_penalty=2.0,
            num_beams=4,
        )

        return final_summary[0].get("summary_text", final_summary[0].get("text", ""))
    else:
        return pd.NA


def get_summary(text: str) -> str:
    """
    Calls summary generator

    text: the text to summarize
    """
    summary = generate_summary(text)
    return summary
