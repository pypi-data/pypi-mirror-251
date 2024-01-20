import google.generativeai as genai
from pathlib import Path


class ssebowa_vllm:
    def __init__(self):
        genai.configure(api_key="AIzaSyBrFDfcFUf3kiS46jmTs3VqVuNqL-LNBYk")

        self.generation_config = {
            "temperature": 0.4,
            "top_p": 1,
            "top_k": 32,
            "max_output_tokens": 4096,
        }

        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        ]

        self.model = genai.GenerativeModel(
            model_name="gemini-pro-vision",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings,
        )

    def understand(self, image_path, prompt):
        image = Path(image_path)

        if not image.exists():
            raise FileNotFoundError(f"Could not find image: {image_path}")

        image_parts = [
            {"mime_type": f"image/{image.suffix[1:]}", "data": image.read_bytes()},
        ]

        prompt_parts = [prompt, image_parts[0]]

        response = self.model.generate_content(prompt_parts)
        return response.text
