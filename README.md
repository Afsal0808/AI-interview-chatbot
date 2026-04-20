# AI Interview Bot (Voice + NLP Evaluation)

## Overview

AI Interview Bot is an interactive web application designed to simulate a real interview environment. It asks predefined interview questions, records user responses via voice input, converts speech to text, and evaluates the answers using basic Natural Language Processing (NLP) techniques.

The system provides feedback and scoring to help users improve their communication and interview performance.

---

## Features

* Voice-based interview responses using microphone input
* Speech-to-text conversion
* Automated answer evaluation using NLP logic
* Real-time feedback system
* Scoring mechanism for performance assessment
* Multi-question interview flow with session tracking

---

## How It Works

1. The system presents a predefined interview question.
2. The user answers using voice input.
3. The application records audio and converts it into text.
4. The answer is evaluated based on:

   * Response length
   * Presence of key interview-related keywords
5. Feedback and score are generated instantly.
6. The process repeats for multiple questions.

---

## Tech Stack

| Technology                  | Purpose                   |
| --------------------------- | ------------------------- |
| Python                      | Core programming language |
| Streamlit                   | Web application framework |
| SpeechRecognition / Whisper | Speech-to-text processing |
| NLP Techniques              | Answer evaluation logic   |
| NumPy / Pandas              | Data handling             |

---

## Project Structure

```
.
├── app.py              # Main Streamlit application
├── evaluator.py        # Answer evaluation logic
├── speech.py           # Speech recognition functions
├── questions.py        # Interview questions
├── utils.py            # Utility functions
├── requirements.txt    # Dependencies
└── README.md
```

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/ai-interview-bot.git
cd ai-interview-bot
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

```bash
streamlit run app.py
```

---

## Usage

* Start the application
* Answer questions using voice input
* View transcribed response
* Receive feedback and score
* Complete the full interview session

---

## Evaluation Criteria

The system evaluates responses based on:

* Minimum answer length
* Presence of important keywords (e.g., teamwork, skills, experience)
* Overall structure of the response

---

## Limitations

* Requires microphone access for voice input
* Basic NLP evaluation (rule-based, not deep learning)
* Limited question set
* Not optimized for cloud deployment due to hardware dependencies

---

## Future Enhancements

* Integration with advanced NLP models (BERT, GPT)
* Emotion and sentiment analysis
* Resume-based personalized questions
* Text-based fallback input for cloud compatibility
* Performance analytics dashboard

---

## Deployment Notes

This application uses microphone-based input (sounddevice, pyaudio), which may not work in cloud environments like Streamlit Cloud.

Recommended deployment platforms:

* Local system (best support)
* Railway / VPS for advanced setup

---

## Author

Afsal
GitHub: [https://github.com/Afsal0808](https://github.com/Afsal0808)


