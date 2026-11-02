import ollama

class PragatiCampaignEngine:
    def __init__(self, api_key=None):
        self.model_name = "llama3.2"

    def generate_paytm_qr_offer(self, product_name, discount_pct):
        prompt = f"""
        Create a promotional Paytm Cashback Campaign for a retail product.
        Product: {product_name}
        Discount: {discount_pct}% Cashback via Paytm QR!

        Generate output with these exact 3 sections:
        1. Catchy Soundbox Audio Announcement Text (Hinglish, 1 short sentence)
        2. QR Banner Headline for Paytm Merchant App
        3. WhatsApp Customer Broadcast Message with Emojis
        """

        try:
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
        except Exception as e:
            return f"⚠️ Ollama Error: Ensure Ollama server is running. Details: {str(e)}"