from flask import Flask, render_template, request, jsonify
from main import LetterBoxedSolver

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    # Get letter groups from the user input
    letter_groups = request.form.get('letter_groups')
    if not letter_groups:
        return jsonify({"error": "Letter groups are required"}), 400

    try:
        # Initialize the solver and find solutions
        solver = LetterBoxedSolver(letter_groups)
        solutions = solver.solve_multiple(100)
        return jsonify({"solutions": solutions[:10]})  # Return the top 10 solutions
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)