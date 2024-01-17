from typing import Any, List, Optional

import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from inter_jamisson.interface_adapters.model.knn_model import KNNModel

app = FastAPI()
knn_model = KNNModel("data/ola.pkl")


class ModelInput(BaseModel):
    SepalLengthCm: float
    SepalWidthCm: float
    PetalLengthCm: float
    PetalWidthCm: float


class ApiInput(BaseModel):
    instances: List[ModelInput]
    parameters: Optional[Any] = None


class ModelOutput(BaseModel):
    Species: str


class ApiOutput(BaseModel):
    predictions: List[ModelOutput]


@app.post("/predict")
def predict(input_data: ApiInput):
    try:
        instances = input_data.instances
        input_df = pd.DataFrame([dict(i) for i in instances])

        results = knn_model.model.predict(input_df)
        output = [ModelOutput(Species=str(r)) for r in results]

        return ApiOutput(predictions=output)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
