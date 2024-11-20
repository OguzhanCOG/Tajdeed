from transformers import pipeline
import re
import sys
import os

class ConsoleOutputManagerPolyInfoEvolution:
  def __init__(self):
    self.stdout = sys.stdout
    self.stderr = sys.stderr
    self.devnull = open(os.devnull, 'w')
  def disable(self):
    sys.stdout = self.devnull
    sys.stderr = self.devnull
  def enable(self):
    sys.stdout = self.stdout
    sys.stderr = self.stderr
    self.devnull.close()

def process(rough_text):
    output_manager = ConsoleOutputManagerPolyInfoEvolution()
    output_manager.disable()

    prompt = f"Give me a short answer; a single answer. Do not hallucinate random questions after you have answered this question. Question: Turn this into some bullet points for a summary: '{rough_text}'. Answer:"
    # Define input prompt with clear instructions

    # Use the pipeline with adjusted parameters
    pipe = pipeline("text-generation", model="meta-llama/Llama-3.2-1B", device=0)

    # Generate a response
    response = pipe(
        prompt,
        max_length=1500,
        do_sample=False,  # Disable sampling for deterministic output
        repetition_penalty=1.0,  # Lower repetition penalty for more natural output
        eos_token_id=128001,  # Ensure generation stops at the eos_token
        pad_token_id=128001,  # Set pad_token_id to eos_token_id for stopping
        truncation=True,  # Explicitly truncate long inputs
    )

    def clean_output(response_text):
        # Find the first "Answer:" and keep everything before it (including the first "Answer:")
        match = re.search(r'Answer:.*?(\n|$)', response_text)
        
        if match:
            # Return only the portion before the first "Answer:" occurs
            return match.group(0).strip()
        else:
            # In case there's no "Answer:" in the text, return the input as it is
            return response_text.strip()

    response_text = (response[0]["generated_text"])[8:]

    output_manager.enable()

    print(clean_output(response_text))

process("n-person workshops: a series of 3 main workshops, each comprising of different aims. Workshop 1: the history of calligraphy in the Arab and Islamic world. Workshop 2: Teaching traditional arabic writing through collaborations with a cultural institution (ex: British Arab Center)  educating people about the Arabic alphabet, Workshop 3: Calligraphy+Graffiti, introducing calligraphy with a contemporary twist, by introducing the art form of “Calligraphiti” workshops by renowned artists. Inspired by artist El Seed.")