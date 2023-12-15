from transformers import pipeline
import pandas as pd


def generate_summary(description):
    # Load the summarization pipeline
    summarizer = pipeline("summarization", model="Azma-AI/bart-large-text-summarizer")

    # Check if the description is not null(has more than 3 characters)
    if pd.notna(description) and len(description) > 3:
        """
        The model has a limit of 1024 characters of input so we have divided the inputs in different fragments to be able to use it.
        Once divided we have made a summary of each part and we have joined them together.
        Finally we have made a summary of the previous concatenation.

        """

        # Define maximum length allowed by the model (1024 tokens)
        max_length = 1024

        # Divide the description into fragments of maximum length
        fragments = [
            description[i : i + max_length]
            for i in range(0, len(description), max_length)
        ]

        # Initialize the final summary
        final_summary = ""

        # Iterate on each fragment and generate summary
        for fragment in fragments:
            fragment_summary = summarizer(
                fragment, max_length=50, min_length=30, length_penalty=2.0, num_beams=4
            )
            final_summary += fragment_summary[0].get(
                "summary_text", fragment_summary[0].get("text", "")
            )

        # Apply summary to combined text
        final_summary = summarizer(
            final_summary,
            max_length=150,
            min_length=50,
            length_penalty=2.0,
            num_beams=4,
        )

        return final_summary[0].get("summary_text", final_summary[0].get("text", ""))
    else:
        # If the description is null return NA
        return pd.NA


def get_summary(df):
    # Load the summarization pipeline
    summarizer = pipeline("summarization", model="Azma-AI/bart-large-text-summarizer")

    # Add a new column for the final summary
    df["summary_azma_ai_model"] = None

    for index, row in df.iterrows():
        description = str(row["WEB"])

        if pd.notna(description) and len(description) > 3:
            # Generate summary
            summary = generate_summary(description)

            # Assign the final summary to the DataFrame
            df.at[index, "summary_azma_ai_model"] = summary
        else:
            # If the description is NaN return NA
            df.at[index, "summary_azma_ai_model"] = pd.NA

    return df
