from transformers import pipeline
import os

from utils.document_loader import load_document
from nlp.text_chunker import chunk_text
from nlp.summarizer import generate_notes
from nlp.notes_organizer import organize_notes

# reuse T5 model for question generation
qg_pipeline = None

def load_qg_model():
    return pipeline(
        "text2text-generation",
        model="t5-small",
        tokenizer="t5-small",
        device=-1
    )


def generate_questions(organized_notes):

    global qg_pipeline
    if qg_pipeline is None:
        qg_pipeline = load_qg_model()

    questions = {}

    for topic, notes in organized_notes.items():

        topic_questions = []

        for note in notes:
            if len(note.split()) < 5:
                continue

            input_text = " ".join(note.split()[:50])
            prompt = "generate a meaningful exam question: " + input_text

            try:    
                result = qg_pipeline(
                    prompt,
                    max_length=64,
                    do_sample=False
                )[0]["generated_text"]

                question = result.strip().capitalize()

                if not question.endswith("?"):
                    question += "?"

                topic_questions.append(question)

            except Exception as e:
                print("Question generation failed:",e)

        seen = set()
        topic_questions = [
            q for q in topic_questions
            if not (q in seen or seen.add(q))
        ]

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