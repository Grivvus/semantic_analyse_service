import torch
import transformers
from transformers import BertModel, BertTokenizer


def vectorize(text: list[str]) -> list[list[float]]:
    ...


def vectorize_one(text: str) -> list[float]:
    tokenizer, model = prepare_model()
    inputs = tokenizer(
        text, return_tensors="pt",
        padding=True, truncation=True,
    )
    with torch.no_grad():
        outputs = model(**inputs)
    text_embedding = outputs.last_hidden_state[:, 0, :].numpy().flatten()
    text_embedding = text_embedding.tolist()
    return text_embedding


def prepare_model() -> tuple[BertTokenizer, BertModel]:
    model_name = "bert-base-uncased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)
    return tokenizer, model
