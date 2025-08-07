from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

tokenizer = AutoTokenizer.from_pretrained("kredor/punctuate-all")
model = AutoModelForTokenClassification.from_pretrained("kredor/punctuate-all")
punctuator = pipeline("token-classification", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

def restore_punctuation(text):
    output = punctuator(text)
    punctuated = ""
    for word in output:
        punctuated += word['word'] + (" " if word['end'] < len(text) else "")
    return punctuated.replace(" ,", ",").replace(" .", ".").replace(" ?", "?")

# Example:
if __name__ == "__main__":
    raw_text = "salem bienvenue au meeting aujourd hui nous allons parler du projet"
    print("📄 With punctuation:\n", restore_punctuation(raw_text))
