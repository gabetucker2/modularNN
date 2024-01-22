from flask import Flask, jsonify
import threading

app = Flask(__name__)

# Global variables
triggered = False
color = "black"

@app.route('/')
def index():
    global triggered
    content = generate_rows_html([3, 5, 5, 1]) if triggered else "Waiting for trigger..."
    return f'''
    <!doctype html>
    <html>
    <head>
        <title>Neural Network Visualization</title>
        <style>
            .circle {{
                width: 150px;
                height: 150px;
                border-radius: 50%;
                display: inline-block;
                margin: 10px;
                color: white;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                background-color: {color};
                position: relative;
                z-index: 2;
            }}
            .row {{
                text-align: center;
            }}
        </style>
    </head>
    <body>
        <div id="circles-container">{content}</div>
        <div id="lines-container"></div>
        <script>
            function drawLines() {{
                var linesContainer = document.getElementById("lines-container");
                linesContainer.innerHTML = ""; // Clear previous lines

                var rows = document.getElementsByClassName("row");
                if (rows.length < 2) return; // Ensure there are at least two rows

                for (let i = 0; i < rows.length - 1; i++) {{
                    let startCircles = rows[i].getElementsByClassName("circle");
                    let endCircles = rows[i + 1].getElementsByClassName("circle");

                    for (let startCircle of startCircles) {{
                        let startRect = startCircle.getBoundingClientRect();

                        for (let endCircle of endCircles) {{
                            let endRect = endCircle.getBoundingClientRect();

                            let startX = startRect.left + startRect.width / 2;
                            let startY = startRect.top + startRect.height / 2;
                            let endX = endRect.left + endRect.width / 2;
                            let endY = endRect.top + endRect.height / 2;

                            let lineLength = Math.sqrt(Math.pow(endX - startX, 2) + Math.pow(endY - startY, 2));
                            let angle = Math.atan2(endY - startY, endX - startX) * 180 / Math.PI;

                            let lineStyle = `position: absolute; width: ${{lineLength}}px; height: 2px; background-color: black; top: ${{startY}}px; left: ${{startX}}px; transform: rotate(${{angle}}deg); transform-origin: 0 0;`;

                            let line = document.createElement("div");
                            line.setAttribute("style", lineStyle);
                            linesContainer.appendChild(line);
                        }}
                    }}
                }}
            }}

            setInterval(function() {{
                fetch("/check-update")
                    .then(response => response.json())
                    .then(data => {{
                        var container = document.getElementById("circles-container");
                        if (data.triggered) {{
                            container.innerHTML = data.html;
                            drawLines(); // Call drawLines to add lines
                        }}
                        var circles = container.getElementsByClassName("circle");
                        for (var i = 0; i < circles.length; i++) {{
                            circles[i].style.backgroundColor = data.color;
                        }}
                    }})
                    .catch(error => console.error("Error:", error));
            }}, 50);
        </script>
    </body>
    </html>
    '''




@app.route('/check-update')
def check_update():
    global color, triggered
    # Return the current state and HTML content
    return jsonify(triggered=triggered, color=color, html=generate_rows_html([3, 5, 5, 1]) if triggered else "")

@app.route('/trigger-red', methods=['POST'])
def trigger_red():
    global color
    original_color = color
    color = "red"
    threading.Timer(0.1, revert_color, args=[original_color]).start()
    return jsonify(success=True)

@app.route('/trigger', methods=['POST'])
def trigger():
    global triggered
    triggered = True
    return jsonify(success=True)

def revert_color(original_color):
    global color
    color = original_color

def generate_rows_html(rows):
    html = ''
    for row_count in rows:
        html += '<div class="row">' + ''.join([f'<div class="circle"></div>' for _ in range(row_count)]) + '</div>'
    # Add logic to generate lines here, or handle it dynamically with JavaScript/SVG
    return html

if __name__ == '__main__':
    app.run(debug=True)
