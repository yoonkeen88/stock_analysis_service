"""
Model loader for loading pre-trained ML models
"""
import os
import pickle
from typing import Optional, Any
from pathlib import Path
from app.core.config import settings


class ModelLoader:
    """Loader for ML models"""
    
    def __init__(self, model_dir: Optional[str] = None):
        self.model_dir = Path(model_dir or settings.ML_MODEL_PATH)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self._models: dict[str, Any] = {}
    
    def load_model(self, model_name: str) -> Optional[Any]:
        """
        Load a pre-trained model from disk
        
        Args:
            model_name: Name of the model to load
        
        Returns:
            Loaded model object or None if not found
        """
        if model_name in self._models:
            return self._models[model_name]
        
        model_path = self.model_dir / f"{model_name}.pkl"
        
        if not model_path.exists():
            return None
        
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            self._models[model_name] = model
            return model
        except Exception as e:
            print(f"Error loading model {model_name}: {e}")
            return None
    
    def save_model(self, model: Any, model_name: str) -> bool:
        """
        Save a model to disk
        
        Args:
            model: Model object to save
            model_name: Name to save the model as
        
        Returns:
            True if successful, False otherwise
        """
        try:
            model_path = self.model_dir / f"{model_name}.pkl"
            with open(model_path, 'wb') as f:
                pickle.dump(model, f)
            self._models[model_name] = model
            return True
        except Exception as e:
            print(f"Error saving model {model_name}: {e}")
            return False
    
    def list_available_models(self) -> list[str]:
        """List all available model files"""
        models = []
        for file in self.model_dir.glob("*.pkl"):
            models.append(file.stem)
        return models

