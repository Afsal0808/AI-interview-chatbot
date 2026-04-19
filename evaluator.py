def evaluate_answer(answer):
    score = 0

    # Length check
    if len(answer.split()) > 5:
        score += 2

    # Keywords check
    keywords = ["team", "hardworking", "problem", "experience", "skills"]

    for word in keywords:
        if word in answer.lower():
            score += 1

    # Final feedback
    if score >= 4:
        return "✅ Excellent Answer"
    elif score >= 2:
        return "👍 Good Answer"
    else:
        return "⚠️ Needs Improvement"