import streamlit as st
import json

def load_questions():
    """Loads the questions from a JSON file."""
    try:
        with open("questions.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

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
        questions = load_questions()
        responses = {}
        
        for index, q in enumerate(questions, start=1):
            st.write(f"**Question {index}:** {q['question']}")
            responses[f"q{index}"] = st.radio("Select an answer:", [f"{chr(65 + i)}. {option}" for i, option in enumerate(q['options'])], index=None, key=f"q{index}")
        
        if st.button("Submit Quiz"):
            score = 0
            total_questions = len(questions)
            
            for index, q in enumerate(questions, start=1):
                answer = responses[f"q{index}"]
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
