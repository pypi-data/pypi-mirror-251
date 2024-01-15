from llm_guard.transformers_helpers import pipeline
from llm_guard.util import calculate_risk_score, extract_urls, logger

from .base import Scanner

_model_path = (
    "DunnBC22/codebert-base-Malicious_URLs",
    "laiyer/codebert-base-Malicious_URLs-onnx",  # ONNX version
)

_malicious_labels = [
    "defacement",
    "phishing",
    "malware",
]


class MaliciousURLs(Scanner):
    """
    This scanner is used to scan and detect malicious URLs in the text.

    Large Language Models can occasionally produce malicious URLs in their outputs.
    Using the "DunnBC22/codebert-base-Malicious_URLs" model from HuggingFace, this class classifies
    URLs as either malicious or benign to safeguard users from potential threats.
    """

    def __init__(self, *, threshold=0.5, use_onnx: bool = False):
        """
        Initializes an instance of the MaliciousURLs class.

        Parameters:
            threshold (float): The threshold used to determine if the website is malicious. Defaults to 0.5.
            use_onnx (bool): Whether to use the ONNX version of the model. Defaults to False.
        """

        self._threshold = threshold
        self._classifier = pipeline(
            task="text-classification",
            model=_model_path[0],
            onnx_model=_model_path[1],
            truncation=True,
            use_onnx=use_onnx,
            top_k=None,
            max_length=512,
        )

    def scan(self, prompt: str, output: str) -> (str, bool, float):
        if output.strip() == "":
            return output, True, 0.0

        urls = extract_urls(output)
        if len(urls) == 0:
            return output, True, 0.0

        logger.debug(f"Found {len(urls)} URLs in the output")

        results = self._classifier(urls)
        for url, result in zip(urls, results):
            malicious_scores = [
                item["score"] for item in result if item["label"] in _malicious_labels
            ]
            highest_malicious_score = max(malicious_scores)
            if highest_malicious_score > self._threshold:
                logger.warning(
                    f"Detected malware URL '{url}' with score: {highest_malicious_score}"
                )

                return output, False, calculate_risk_score(highest_malicious_score, self._threshold)

        logger.debug(f"Not malware URLs in the output: {results}")

        return output, True, 0.0
