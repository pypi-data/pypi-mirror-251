class TextCompletion:
    def __init__(self, http_client, prompt, **kwargs):
        self.http_client = http_client
        self.prompt = prompt
        self.params = kwargs

    def get_response(self):
        # Logic to communicate with the model API
        response = self.http_client.post("/text-completion", data=self._build_payload())
        return response

    def _build_payload(self):
        return {
            "prompt": self.prompt,
            **self.params
        }
