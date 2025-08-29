from flask import Flask, request, jsonify
import os, re

app = Flask(__name__)

def is_int_str(s): return re.fullmatch(r"-?\d+", s or "") is not None

@app.post("/bfhl")
def bfhl():
    try:
        data = (request.get_json() or {}).get("data", [])
        FULL_NAME = (os.getenv("FULL_NAME", "john_doe")).lower()
        DOB = os.getenv("DOB_DDMMYYYY", "17091999")
        EMAIL = os.getenv("EMAIL", "john@example.com")
        ROLL = os.getenv("ROLL_NUMBER", "123456")

        to_str = lambda x: x if isinstance(x, str) else (str(x) if isinstance(x, (int, float)) else "")
        numeric = [s for s in map(to_str, data) if is_int_str(s)]
        alphas  = [s for s in data if isinstance(s, str) and s.isalpha()]
        specials = [x if isinstance(x, str) else str(x) for x in data
                    if not (isinstance(x, str) and x.isalpha()) and not is_int_str(to_str(x))]

        even_numbers = [s for s in numeric if int(s) % 2 == 0]
        odd_numbers  = [s for s in numeric if abs(int(s)) % 2 == 1]
        alphabets    = [s.upper() for s in alphas]
        total_sum    = str(sum(int(s) for s in numeric))
        letters = list("".join(alphas))
        alternate_caps = "".join(ch.upper() if i % 2 == 0 else ch.lower() for i, ch in enumerate(reversed(letters)))

        return jsonify({
            "is_success": True,
            "user_id": f"{FULL_NAME}_{DOB}",
            "email": EMAIL,
            "roll_number": ROLL,
            "even_numbers": even_numbers,
            "odd_numbers": odd_numbers,
            "alphabets": alphabets,
            "special_characters": specials,
            "sum": total_sum,
            "alternate_caps": alternate_caps
        }), 200
    except:
        return jsonify({"is_success": False, "error": "Invalid input format"}), 400

if __name__ == "__main__":
    app.run(port=3000)
