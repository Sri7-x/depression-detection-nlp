from transformers import pipeline

# Global variable for the model
emotion_classifier = None

def get_model():
    global emotion_classifier
    if emotion_classifier is None:
        print("Loading model... (This might take a moment on first run)")
        emotion_classifier = pipeline(
            "text-classification", 
            model="j-hartmann/emotion-english-distilroberta-base", 
            return_all_scores=True,
            framework="pt"
        )
    return emotion_classifier

def analyze_text(text: str):
    """
    Analyzes the text for "sadness" and other emotions to infer a depression level.
    Returns: {
        "depression_level": "Low" | "Moderate" | "High",
        "confidence": float,
        "recommendations": List[str]
    }
    """
    classifier = get_model()
    results = classifier(text)
    # results is a list of lists: [[{'label': 'anger', 'score': ...}, ...]]
    scores = {item['label']: item['score'] for item in results[0]}
    
    sadness_score = scores.get('sadness', 0)
    joy_score = scores.get('joy', 0)
    
    # Simple logic to determine "Depression Level" based on Sadness vs Joy
    # This is a HEURISTIC for demonstration purposes.
    
    level = "Low"
    recommendations = []
    
    if sadness_score > 0.7:
        level = "High"
        recommendations = [
            "Please reach out to a professional mental health counselor.",
            "Contact a trusted friend or family member immediately.",
            "Try to practice deep breathing exercises.",
            "Remember that you are not alone."
        ]
    elif sadness_score > 0.4:
        level = "Moderate"
        recommendations = [
            "Consider talking to a therapist.",
            "Engage in a gentle physical activity like walking.",
            "Try to maintain a regular sleep schedule.",
            "Practice mindfulness or meditation."
        ]
    else:
        # If joy is high, or sadness is low
        level = "Low"
        recommendations = [
            "Keep maintaining your healthy habits!",
            "Stay connected with your friends.",
            "Continue engaging in activities you enjoy.",
            "Drink plenty of water and stay active."
        ]
        
    return {
        "depression_level": level,
        "sadness_score": f"{sadness_score:.2f}",
        "recommendations": recommendations
    }

if __name__ == "__main__":
    # fast test
    print(analyze_text("I feel absolutely hopeless and life has no meaning."))
    print(analyze_text("I am so happy today!"))
