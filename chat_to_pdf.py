from fpdf import FPDF
import json
import sys
import os

# -------------------------
# PDF Builder
# -------------------------
class ChatPDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, "Chat Export", ln=True, align="C")
        self.ln(5)

    def add_message(self, role, content):
        self.set_font("Arial", "B", 11)
        self.cell(0, 8, role.upper(), ln=True)

        self.set_font("Arial", "", 10)
        self.multi_cell(0, 6, content)
        self.ln(3)


# -------------------------
# Load Chat Data
# -------------------------
def load_chat(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()

    # Try JSON first (ChatGPT export style)
    try:
        parsed = json.loads(data)

        # expected: list of messages OR nested structure
        if isinstance(parsed, list):
            return parsed

        if "messages" in parsed:
            return parsed["messages"]

    except:
        pass

    # fallback: treat as plain text
    return [{"role": "chat", "content": data}]


# -------------------------
# Convert to PDF
# -------------------------
def convert_to_pdf(messages, output_file="output.pdf"):
    pdf = ChatPDF()
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.add_page()

    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")

        pdf.add_message(role, content)

    pdf.output(output_file)
    print(f"Saved: {output_file}")


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python chat_to_pdf.py input.json")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.exists(input_file):
        print("File not found")
        sys.exit(1)

    messages = load_chat(input_file)
    convert_to_pdf(messages)
