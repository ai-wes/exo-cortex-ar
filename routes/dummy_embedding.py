from fastapi import Body, HTTPException
import random

def dummy_embedding(text: str, length=8):
    return [random.random() for _ in range(length)]
