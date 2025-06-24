import openai
import re
import tkinter as tk
from tkinter import ttk

# ✅ OpenRouter credentials
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

def generate_next_sentence(input_sentence):
    prompt = f"""You are a writing assistant.
Given the sentence: "{input_sentence}"
Write the next sentence that follows naturally and keeps the same context."""

    try:
        response = openai.ChatCompletion.create(
            model="mistralai/devstral-small:free",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.8
        )

        full_text = response.choices[0].message.content.strip()

        # Try to extract a clean sentence
        match = re.search(r"([^.?!\n]+[.?!])", full_text)
        if match:
            return match.group(1).strip()

        for line in full_text.splitlines():
            line = line.strip()
            if line and not line.startswith("◁"):
                return line

        return full_text if full_text else "❌ No output from AI."

    except Exception as e:
        return f"❌ Error: {e}"

# GUI function
def on_generate():
    sentence = entry.get().strip()
    if not sentence:
        result_label.config(text="⚠️ Please enter a sentence.", foreground="red")
        return

    result_label.config(text="⏳ Generating next sentence...", foreground="gray")
    window.update_idletasks()
    output = generate_next_sentence(sentence)
    result_label.config(text=f"📝 {sentence}\n\n➡️ {output}", foreground="#222222")

# GUI window setup
window = tk.Tk()
window.title("Next Sentence Generator - Izhaar Kazmi")
window.geometry("700x400")
window.configure(bg="#f2f2f2")
window.resizable(False, False)

style = ttk.Style()
style.configure("TButton", font=("Segoe UI", 11), padding=6)
style.configure("TLabel", font=("Segoe UI", 12), background="#f2f2f2")

# Widgets
heading = tk.Label(window, text="✨ AI Next Sentence Generator ✨", font=("Segoe UI", 16, "bold"), bg="#f2f2f2", fg="#333")
heading.pack(pady=20)

entry = tk.Entry(window, font=("Segoe UI", 12), width=60, borderwidth=2, relief="groove")
entry.pack(pady=10)

generate_btn = ttk.Button(window, text="Generate", command=on_generate)
generate_btn.pack(pady=10)

result_label = tk.Label(window, text="", wraplength=650, justify="left", font=("Segoe UI", 12), bg="#f2f2f2", fg="#333")
result_label.pack(pady=20)

# Start GUI loop
window.mainloop()
