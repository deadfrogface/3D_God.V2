from ai_backend.froggy.froggy_brain import predict, train_on_example

def ask_froggy_anything(log_text="") -> dict:
    features = extract_log_features(log_text)
    prediction = predict(features)
    diagnosis = get_error_description(prediction)

    if diagnosis.get("learn_on_use"):
        train_on_example(features, prediction)

    fix_fn = FIX_FUNCTIONS.get(prediction, lambda: "Kein Fix verfügbar")

    return {
        "problem": diagnosis.get("problem"),
        "cause": diagnosis.get("cause"),
        "suggestion": diagnosis.get("suggestion"),
        "can_fix": diagnosis.get("can_fix", False),
        "fix_fn": fix_fn
    }
