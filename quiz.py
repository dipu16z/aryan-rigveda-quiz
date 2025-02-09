import streamlit as st
import json

def load_leaderboard():
    """Loads the leaderboard from a JSON file."""
    try:
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_leaderboard(leaderboard):
    """Saves the leaderboard to a JSON file."""
    with open("leaderboard.json", "w") as file:
        json.dump(leaderboard, file, indent=4)

def conduct_quiz():
    """Runs the interactive quiz using Streamlit."""
    st.title("Aryan & Rig Veda Quiz")
    player_name = st.text_input("Enter your name:")
    
    if player_name:
        questions = [
            {"question": "What language family did the Aryans originally speak?", "options": ["Dravidian", "Indo-European", "Sino-Tibetan", "Austroasiatic"], "answer": "B"},
            {"question": "Where did the Aryans originally live according to historical texts?", "options": ["West of the Alps", "North of the Himalayas", "East of the Alps", "South of the Sahara"], "answer": "C"},
            {"question": "Which animal played the most significant role in Aryan life?", "options": ["Cow", "Horse", "Dog", "Elephant"], "answer": "B"},
            {"question": "Which ancient text contains hymns and prayers of the Aryans?", "options": ["Torah", "Rig Veda", "Quran", "Avesta"], "answer": "B"},
            {"question": "How many mandalas (books) does the Rig Veda consist of?", "options": ["5", "10", "7", "12"], "answer": "B"}
        ]
        
        score = 0
        total_questions = len(questions)
        
        for index, q in enumerate(questions, start=1):
            st.write(f"**Question {index}:** {q['question']}")
            answer = st.radio("Select an answer:", [f"{chr(65 + i)}. {option}" for i, option in enumerate(q['options'])], index=None, key=f"q{index}")
            
            if answer:
                selected_option = answer[0]
                if selected_option == q['answer']:
                    score += 2
                else:
                    score -= 0.66
        
        st.write(f"### {player_name}, your final score is: {score}/{total_questions * 2}")
        
        leaderboard = load_leaderboard()
        leaderboard[player_name] = score
        save_leaderboard(leaderboard)
        
        st.write("## Leaderboard:")
        sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        for rank, (name, scr) in enumerate(sorted_leaderboard, start=1):
            st.write(f"{rank}. {name} - {scr} points")

if __name__ == "__main__":
    conduct_quiz()
