import io
import re
import pandas as pd
import numpy as np
from PIL import Image
import easyocr

class PragatiAICopilot:
    def __init__(self, api_key=None):
        # Initialize EasyOCR directly
        self.reader = easyocr.Reader(['en'], gpu=False)

    def analyze_bill_or_inventory_image(self, image_bytes, image_mime="image/jpeg"):
        """Fast, direct local OCR without thread locking."""
        try:
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            img_np = np.array(image)

            # Detect text boxes directly
            results = self.reader.readtext(img_np, detail=1)

            if not results:
                return "⚠️ Could not read text from this image. Please ensure the receipt is clear."

            # Group detected bounding boxes line-by-line using vertical Y-coordinates
            lines = []
            # Sort detected items vertically by Y-coordinate
            sorted_results = sorted(results, key=lambda x: x[0][0][1])

            current_line = []
            last_y = None

            for box, text, prob in sorted_results:
                y_center = (box[0][1] + box[2][1]) / 2
                if last_y is None or abs(y_center - last_y) < 15:
                    current_line.append((box[0][0], text))
                else:
                    # Sort horizontal elements in the line (X-coordinate)
                    current_line.sort(key=lambda x: x[0])
                    lines.append(" | ".join([item[1] for item in current_line]))
                    current_line = [(box[0][0], text)]
                last_y = y_center

            if current_line:
                current_line.sort(key=lambda x: x[0])
                lines.append(" | ".join([item[1] for item in current_line]))

            # Format extracted lines straight into clean Markdown Table rows
            table_rows = ["| Extracted Item / Detail | Value / Amount |", "| :--- | :--- |"]
            for l in lines:
                parts = l.split(" | ")
                if len(parts) >= 2:
                    item_name = " ".join(parts[:-1])
                    price = parts[-1]
                    table_rows.append(f"| {item_name} | {price} |")
                else:
                    table_rows.append(f"| {parts[0]} | - |")

            return "\n".join(table_rows)

        except Exception as e:
            return f"⚠️ Error processing image: {str(e)}"

    def voice_soundbox_assistant(self, user_speech_text, conversation_history, kpis):
        """Conversational Chatbot with strict Hinglish grounding."""
        import ollama
        system_prompt = f"""
        You are Paytm Soundbox Pragati Voice Assistant speaking directly to an Indian Kirana shop owner.
        Store KPIs:
        - 7-Day Revenue: ₹{kpis.get('recent_7_days_revenue', 0):,.2f}
        - Daily Sales Average: ₹{kpis.get('avg_daily_sales', 0):,.2f}

        STRICT RULES:
        1. Speak in warm, natural Hinglish (Hindi written in English script).
        2. Keep replies short (maximum 2-3 sentences).
        """

        messages = [{'role': 'system', 'content': system_prompt}]
        for msg in conversation_history:
            messages.append({'role': msg['role'], 'content': msg['content']})
        messages.append({'role': 'user', 'content': user_speech_text})

        try:
            response = ollama.chat(
                model="llama3.2",
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            return f"Namaste! Thoda aaram kar lijiye. Aaj aapka dhandha badiya raha hai!"

    def generate_excel_bytes(self, markdown_table_str):
        """Dynamically parses markdown table into Excel binary."""
        rows = []
        for line in markdown_table_str.split("\n"):
            if "|" in line and ":---" not in line and "---" not in line:
                columns = [col.strip() for col in line.split("|")[1:-1]]
                if columns:
                    rows.append(columns)
        
        if len(rows) > 1:
            df = pd.DataFrame(rows[1:], columns=rows[0])
        else:
            df = pd.DataFrame({"Extracted Text": [markdown_table_str]})

        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='ReceiptDetails', index=False)
        return output.getvalue()