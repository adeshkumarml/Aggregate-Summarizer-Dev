from app.config.config import MODEL_COSTS

def estimate_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    model_cost = MODEL_COSTS.get(model_name)

    try:
        input_cost = (input_tokens * model_cost["input"]) / 1000000
        output_cost = (output_tokens * model_cost["output"]) / 1000000
        
        return round(input_cost + output_cost, 6)
    
    except Exception:
        return 0.0