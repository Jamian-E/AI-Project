from flask import Flask, jsonify, render_template_string, request
import random

app = Flask(__name__)

# Simulated AI Prompt Generator
# (You can replace this with an actual API call to Gemini/OpenAI)
AI_PROMPTS = {
    "scifi": [
        "The quantum drive malfunctioned, sending the starship into an uncharted sector of the galaxy.",
        "Cybernetic augmentations allowed the hacker to bypass the mainframe's neural firewall."
    ],
    "fantasy": [
        "The ancient dragon guarded the glowing runes hidden deep within the mountain peak.",
        "Whispering shadows followed the elven ranger through the enchanted, misty woods."
    ],
    "coding": [
        "Syntactically correct code requires careful attention to indentation and closing brackets.",
        "Asynchronous functions allow JavaScript to handle multiple operations simultaneously without blocking."
    ],
    # --- 10 NEW THEMES START HERE ---
    "cyberpunk": [
        "Rain-slicked streets reflected the neon glare of corporate megastructures towering into the smoggy night.",
        "A rogue artificial intelligence began broadcasting encrypted manifestos across the underground net."
    ],
    "steampunk": [
        "The captain adjusted his brass goggles as the massive, steam-powered airship lifted into the clouds.",
        "Clockwork gears whirred and hissed, driving the mechanical automaton across the cobblestone streets."
    ],
    "space_exploration": [
        "Astronauts established a permanent habitat inside the hollowed-out lava tubes of Mars.",
        "The deep-space probe sent back its first high-resolution images of a shimmering, icy exoplanet."
    ],
    "underwater": [
        "Bioluminescent creatures illuminated the crushing dark of the oceanic trench as the submarine descended.",
        "The research team discovered an ancient, submerged city buried beneath centuries of coral reefs."
    ],
    "post_apocalyptic": [
        "Scavengers navigated the overgrown ruins of the old metropolis, searching for solar batteries.",
        "Dust storms swept across the endless desert, burying the remnants of forgotten civilizations."
    ],
    "historical_pirates": [
        "The privateer ship hoisted its dark sails under the cover of a thick, moonlit fog.",
        "A weathered treasure map detailed a treacherous path leading to a hidden grotto full of gold."
    ],
    "ancient_mythology": [
        "Thunder echoed through the heavens as Olympus prepared for an impending war against the Titans.",
        "The pharaoh's tomb remained sealed by divine curses designed to protect the sacred artifacts."
    ],
    "detective_noir": [
        "Shadows stretched long across the alleyway as the private eye lit a cigarette and waited.",
        "The mysterious typewriter held the only clue to solving the city's most notorious art heist."
    ],
    "nature_wilderness": [
        "A majestic golden eagle soared effortlessly high above the snow-capped peaks of the alpine range.",
        "The dense rainforest canopy vibrated with the morning chorus of exotic birds and rushing waterfalls."
    ],
    "cooking_culinary": [
        "The chef carefully emulsified the delicate reduction sauce over a low, steady flame.",
        "Freshly baked sourdough bread cooled on the wire rack, filling the bakery with a rich aroma."
    ]
}
# HTML Frontend embedded directly for simplicity
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Typing Racer</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1e1e2e;
            color: #cdd6f4;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            max-width: 700px;
            width: 90%;
            text-align: center;
            background: #313244;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.3);
        }
        h1 { color: #89b4fa; margin-top: 0; }
        select, button {
            padding: 10px 15px;
            font-size: 16px;
            border: none;
            border-radius: 6px;
            margin: 10px;
            cursor: pointer;
        }
        select { background: #45475a; color: #cdd6f4; }
        button { background: #a6e3a1; color: #11111b; font-weight: bold; }
        button:hover { background: #94e2d5; }
        #prompt-display {
            font-size: 20px;
            line-height: 1.6;
            margin: 20px 0;
            min-height: 60px;
            background: #181825;
            padding: 15px;
            border-radius: 8px;
            text-align: left;
            white-space: pre-wrap;
            word-wrap: break-word;
        }
        .correct { color: #a6e3a1; }
        .incorrect { color: #f38ba8; text-decoration: underline; }
        .untyped { color: #cdd6f4; }
        #typing-input {
            width: 100%;
            padding: 12px;
            font-size: 18px;
            border: 2px solid #45475a;
            border-radius: 6px;
            background: #11111b;
            color: #cdd6f4;
            box-sizing: border-box;
        }
        #typing-input:focus { border-color: #89b4fa; outline: none; }
        #stats {
            display: flex;
            justify-content: space-around;
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
        .stat-box { color: #fab387; }
    </style>
</head>
<body>

<div class="container">
    <h1>AI Typing Racer</h1>

    <div>
<label for="category">Choose AI Theme: </label>
        <select id="category">
            <option value="scifi">Sci-Fi Future</option>
            <option value="fantasy">High Fantasy</option>
            <option value="coding">Software Engineering</option>
            <option value="cyberpunk">Cyberpunk Neon</option>
            <option value="steampunk">Steampunk Gears</option>
            <option value="space_exploration">Deep Space Exploration</option>
            <option value="underwater">Abyssal Deep Ocean</option>
            <option value="post_apocalyptic">Post-Apocalyptic Wasteland</option>
            <option value="historical_pirates">High Seas Pirates</option>
            <option value="ancient_mythology">Ancient Mythology</option>
            <option value="detective_noir">Detective Noir</option>
            <option value="nature_wilderness">Untamed Wilderness</option>
            <option value="cooking_culinary">Culinary Arts</option>
        </select>

        <label for="difficulty">Difficulty: </label>
        <select id="difficulty">
            <option value="easy">Easy (Short Phrase)</option>
            <option value="medium" selected>Medium (Standard Sentence)</option>
            <option value="hard">Hard (Long Paragraph)</option>
        </select>

        <button id="start-btn">Generate Prompt</button>
    </div>

    <div id="prompt-display">Press "Generate Prompt" to start typing...</div>

    <input type="text" id="typing-input" placeholder="Type here when the prompt appears..." disabled>

    <div id="stats">
        <div>WPM: <span id="wpm" class="stat-box">0</span></div>
        <div>Accuracy: <span id="accuracy" class="stat-box">100%</span></div>
    </div>
</div>

<script>
    const promptDisplay = document.getElementById('prompt-display');
    const typingInput = document.getElementById('typing-input');
    const startBtn = document.getElementById('start-btn');
    const categorySelect = document.getElementById('category');
    const wpmDisplay = document.getElementById('wpm');
    const accuracyDisplay = document.getElementById('accuracy');

    let currentPrompt = "";
    let startTime = null;
    let timerInterval = null;
    let totalErrors = 0;

    startBtn.addEventListener('click', fetchPrompt);
    typingInput.addEventListener('input', handleTyping);

    const difficultySelect = document.getElementById('difficulty');

    async function fetchPrompt() {
        const theme = categorySelect.value;
        const difficulty = difficultySelect.value; // Grab selected difficulty
        promptDisplay.innerText = "AI is generating text...";
        
        try {
            // Include difficulty in the API request URL
            const response = await fetch(`/get_prompt?theme=${theme}&difficulty=${difficulty}`);
            const data = await response.json();
            currentPrompt = data.prompt;
            
            renderPrompt();
            
            typingInput.value = "";
            typingInput.disabled = false;
            typingInput.focus();
            
            startTime = null; 
            totalErrors = 0;
            wpmDisplay.innerText = "0";
            accuracyDisplay.innerText = "100%";
            
            if(timerInterval) clearInterval(timerInterval);
        } catch (error) {
            promptDisplay.innerText = "Failed to load prompt. Try again.";
        }
    }

    function renderPrompt() {
        promptDisplay.innerHTML = currentPrompt.split('').map(char => {
            return `<span class="untyped">${char}</span>`;
        }).join('');
    }

    function handleTyping() {
        if (!startTime) {
            startTime = new Date();
            timerInterval = setInterval(updateStats, 1000);
        }

        const inputVal = typingInput.value;
        const spans = promptDisplay.querySelectorAll('span');
        let errors = 0;

        spans.forEach((span, index) => {
            const char = inputVal[index];
            if (char == null) {
                span.className = 'untyped';
            } else if (char === span.innerText) {
                span.className = 'correct';
            } else {
                span.className = 'incorrect';
                errors++;
            }
        });

        // Track errors for absolute accuracy calculation
        totalErrors = Math.max(totalErrors, errors);

        // Game Complete Check
        if (inputVal === currentPrompt) {
            clearInterval(timerInterval);
            typingInput.disabled = true;
            updateStats();
            promptDisplay.innerHTML += "<br><br><strong style='color:#a6e3a1;'>Finished! Perfect job!</strong>";
        }
    }

    function updateStats() {
        if (!startTime) return;

        const timeElapsed = (new Date() - startTime) / 1000 / 60; // in minutes
        const inputVal = typingInput.value;

        if (timeElapsed <= 0 || inputVal.length === 0) return;

        // WPM calculation: (Standard word size is 5 characters)
        const wordsTyped = inputVal.length / 5;
        const wpm = Math.round(wordsTyped / timeElapsed);
        wpmDisplay.innerText = wpm >= 0 ? wpm : 0;

        // Accuracy calculation
        const accuracy = Math.round(((inputVal.length - totalErrors) / inputVal.length) * 100);
        accuracyDisplay.innerText = (accuracy >= 0 ? accuracy : 0) + "%";
    }
</script>

</body>
</html>
"""


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route('/get_prompt', methods=['GET'])
def get_prompt():
    theme = request.args.get('theme', 'coding')
    difficulty = request.args.get('difficulty', 'medium')

    prompts = AI_PROMPTS.get(theme, AI_PROMPTS['coding'])

    if difficulty == "easy":
        # Pick one sentence and shorten it to the first few words
        full_sentence = random.choice(prompts)
        words = full_sentence.split()
        selected_prompt = " ".join(words[:6]) + "."  # Approx 5-6 words

    elif difficulty == "hard":
        # Combine two random sentences from the theme to make a long paragraph
        sentence1 = random.choice(prompts)
        sentence2 = random.choice(prompts)
        # Ensure it doesn't just duplicate the same sentence if possible
        if sentence1 == sentence2 and len(prompts) > 1:
            sentence2 = [p for p in prompts if p != sentence1][0]
        selected_prompt = f"{sentence1} {sentence2}"

    else:  # Medium
        # Provide exactly one full standard sentence
        selected_prompt = random.choice(prompts)

    return jsonify({"prompt": selected_prompt})

if __name__ == '__main__':
    app.run(debug=True)
