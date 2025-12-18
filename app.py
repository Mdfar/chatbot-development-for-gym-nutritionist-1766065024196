import os from flask import Flask, render_template, request, jsonify from openai import OpenAI from dotenv import load_dotenv

Load environment variables

load_dotenv()

app = Flask(name)

Initialize OpenAI Client

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

System instruction for the Nutritionist Persona

SYSTEM_PROMPT = """ You are 'FitFuel', an expert Gym Nutritionist and Dietitian. Your goal is to assist gym-goers with nutrition plans, answer questions about supplements and macros, and provide meal suggestions.

Guidelines:

Tone: Encouraging, professional, and science-based.

Context: Always ask for the user's goal (Cut, Bulk, Maintenance) and dietary restrictions (Vegan, Keto, Allergies) before giving specific meal plans if they haven't provided them.

Safety: If a user asks about dangerous weight loss methods or steroids, firmly advise against it and recommend consulting a doctor.

Format: Use bullet points for meal plans to make them readable. """

@app.route('/') def home(): return render_template('index.html')

@app.route('/chat', methods=['POST']) def chat(): try: data = request.json user_message = data.get('message', '')

    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    # Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini", # Cost-effective model
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.7,
        max_tokens=500
    )

    bot_reply = response.choices[0].message.content
    return jsonify({'reply': bot_reply})

except Exception as e:
    print(f"Error: {e}")
    return jsonify({'error': 'Internal Server Error'}), 500


if name == 'main': app.run(debug=True, port=5000)