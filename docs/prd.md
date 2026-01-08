PRD: "Elder-Friendly Pharma Assistant"

1. Purpose & Goals
The Problem: Older people often struggle with small text on medicine bottles and complex medical jargon in leaflets.

The Solution: A simple, high-contrast web app where a user types a medicine name and receives a "Plain English" summary of what it is, how to take it, and major warnings.

Primary Goal: Reduce medication errors by providing clear, large-print information.

2. Target Audience (User Personas)
Primary User: "Senior Sam" (75 years old). He has slight tremors, uses reading glasses, and easily feels overwhelmed by complex technology.

Needs: Large buttons, high contrast, zero technical jargon, and "voice-friendly" text.

3. Functional Requirements
Search Feature: A single, large search bar to enter a medicine name (e.g., "Lisinopril").

Data Fetching: The app must connect to a medical database (like openFDA) to get real-time data.

AI Summarizer: The app must use an AI model (like Gemini or Claude) to rewrite the technical "Product Label" into a "3rd-grade reading level" summary.

Categorized Info: Results must be split into:

What is this for? (Purpose)

How do I take it? (Instructions)

Warning! (Dangerous side effects or interactions)

4. User Interface (Elder-Friendly Design)
Text Size: Minimum 18px for body text; 24px for headings.

Contrast: Pure black text on a soft white or light yellow background.

Input: Allow for common spelling errors (AI should guess "Tylenol" if they type "Tilenol").

Buttons: Extra-large "Search" and "Clear" buttons to accommodate motor difficulties.

5. Technical Stack
Frontend: Python with Streamlit (perfect for quick, simple AI tools).

Backend Logic: Python's requests library to fetch from the openFDA API.

AI Logic: LangChain or a direct API call to a model to perform the "Summarization" task.