from transformers import pipeline
import os
import re
import streamlit as st
import traceback

from utils.document_loader import load_document
from nlp.text_chunker import chunk_text
from nlp.summarizer import generate_notes
from nlp.notes_organizer import organize_notes

@st.cache_resource
def load_qg_model():
    # use a proper QG fine-tuned model
    return pipeline(
        "text2text-generation",
        model="mrm8488/t5-base-finetuned-question-generation-ap",
        tokenizer="mrm8488/t5-base-finetuned-question-generation-ap",
        device=-1
    )

# safe getter with error handling

def get_qg_model():
    try:
        return load_qg_model()
    except Exception:
        print("QG model failed to load:")
        traceback.print_exc()
        return None

# truncate at sentence boundary
def truncate_to_sentences(text, max_words=50):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    result = []
    count = 0
    for sent in sentences:
        words = len(sent.split())
        if count + words > max_words:
            break
        result.append(sent)
        count += words
    return " ".join(result) if result else " ".join(text.split()[:max_words])


def generate_questions(organized_notes):

    # graceful fallback if model unavailable
    model = get_qg_model()
    if model is None:
        return {
            topic: ["Question generation unavailable."]
            for topic in organized_notes
        }

    questions = {}

    for topic, notes in organized_notes.items():

        topic_questions = []

        for note in notes:
            if len(note.split()) < 5:
                continue

            # sentence-aware truncation
            input_text = truncate_to_sentences(note, max_words=50)

            # updated prompt for fine-tuned model
            prompt = "generate question: " + input_text

            try:
                result = model(
                    prompt,
                    max_length=64,
                    do_sample=False
                )[0]["generated_text"]

            # Strip "question: " prefix the model adds
                question = result.strip()
                question = " ".join(question.split())
                if question.lower().startswith("question:"):
                    question = question[len("question:"):].strip()

                if question:
                    question = question[0].upper() + question[1:]

                if not question.endswith("?"):
                    question += "?"

            # Filter low quality questions
                if len(question.split()) > 25:
                    continue
                if question.lower().startswith(("generate", "answer")):
                    continue

                # Filter hallucinated questions containing words not in source notes
                source_words = set(" ".join(notes).lower().split())
                question_words = set(re.findall(r"\b[\w\-]+\b", question.lower()))

                # Remove common stop words from check
                stop_words = {"what","is","are","the","a","an","do","does","how","why",
                            "when","where","who","which","in","of","to","and","or","for","can","could","would","should",
                            "be","been","being","this","that","these","those"}
                question_words -= stop_words

                foreign_words = question_words - source_words

                if len(question_words) > 0:
                    ratio = len(foreign_words) / len(question_words)
                    if ratio > 0.5:
                        continue

                # Filter garbled/spaced-out character questions
                if any(len(w) == 1 for w in question.split()[3:]):
                    continue

                topic_questions.append(question)

            except Exception as e:
                print("Question generation failed:", e)

        # Deduplicate
        seen = set()
        unique_questions = []

        for q in topic_questions:
            key = " ".join(q.lower().split())

            if key not in seen:
                seen.add(key)
                unique_questions.append(q)

        topic_questions = unique_questions
        if not topic_questions:
            topic_questions = ["No questions generated for this topic."]

        questions[topic] = topic_questions

    return questions


if __name__ == "__main__":

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sample_file = os.path.join(base_dir, "data", "uploads", "sample.pdf")

    documents = load_document(sample_file)
    chunks = chunk_text(documents)
    notes = generate_notes(chunks)
    organized_notes = organize_notes(notes)
    questions = generate_questions(organized_notes)

    for topic, qs in questions.items():
        print("\n", topic)
        for q in qs:
            print(q)