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

    text_lower = text.lower()

    # 🔴 Critical suicide/self-harm detection
    HIGH_RISK_WORDS = [
        "suicide",
        "kill myself",
        "end my life",
        "want to die",
        "take my life",
        "i don't want to live"
    ]

    for word in HIGH_RISK_WORDS:
        if word in text_lower:
            return {
                "depression_level": "High",
                "sadness_score": "1.00",
                "recommendations": [
                    "Please seek immediate help from a mental health professional.",
                    "Reach out to a trusted friend or family member.",
                    "Contact a suicide prevention helpline.",
                    "Remember that support is available and you are not alone."
                ]
            }

    # 🧠 Emotion Model Analysis
    classifier = get_model()
    results = classifier(text)

    scores = {item['label']: item['score'] for item in results[0]}

    sadness_score = scores.get('sadness', 0)
    joy_score = scores.get('joy', 0)

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
        if scores.get('anger', 0) > 0.5:
            level = "High"
            recommendations = [
                "You are feeling very angry! Please seek advice.",
                "Try to remain calm."
            ]
        else:
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
    print(analyze_text("I feel absolutely hopeless and life has no meaning."))
    print(analyze_text("I am thinking about suicide"))
    print(analyze_text("I am so happy today!"))
