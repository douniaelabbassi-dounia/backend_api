import os, joblib
from typing import Protocol, runtime_checkable
import pandas as pd
from ..config import Config

@runtime_checkable
class SklearnLike(Protocol):
    def predict(self, X: pd.DataFrame): ...

def load_model(filename: str) -> SklearnLike:
    path = os.path.join(Config.MODELS_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Model not found: {path}")
    return joblib.load(path)
