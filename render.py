from flask import Flask, jsonify
import threading

# This code is an abominable minimal viable product and will be improved in the future.

app = Flask(__name__)

# Global variables
triggered = False
color = "black"
lerping = False
lerpDuration = 0.2
msPerIteration = 10

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
            .line {{
                position: absolute;
                height: 5px;
                background-color: black;
                transform-origin: 0 0;
                z-index: 1;
            }}
        </style>
    </head>
    <body>
        <div id="circles-container">{content}</div>
        <div id="lines-container"></div>
        <script>
            function drawLines() {{
                var linesContainer = document.getElementById("lines-container");
                linesContainer.innerHTML = "";

                var rows = document.getElementsByClassName("row");
                if (rows.length < 2) return;

                for (let i = 0; i < rows.length - 1; i++) {{
                    let startCircles = rows[i].getElementsByClassName("circle");
                    let endCircles = rows[i + 1].getElementsByClassName("circle");

                    for (let si = 0; si < startCircles.length; si++) {{
                        for (let ei = 0; ei < endCircles.length; ei++) {{
                            let startCircle = startCircles[si];
                            let endCircle = endCircles[ei];

                            // Extract the numeric part from the circle IDs
                            let startCircleIdPart = startCircle.id.replace("circle_", "");
                            let endCircleIdPart = endCircle.id.replace("circle_", "");

                            // Construct line ID based on the numeric parts of the circle IDs
                            let lineId = `line_${{startCircleIdPart}}_${{endCircleIdPart}}`;
                            let line = document.createElement("div");
                            line.className = "line";
                            line.id = lineId;
                            linesContainer.appendChild(line);
                            positionLine(startCircle, endCircle, line);
                        }}
                    }}
                }}
            }}

            function positionLine(startCircle, endCircle, line) {{
                let startRect = startCircle.getBoundingClientRect();
                let endRect = endCircle.getBoundingClientRect();

                let startX = startRect.left + startRect.width / 2;
                let startY = startRect.top + startRect.height / 2;
                let endX = endRect.left + endRect.width / 2;
                let endY = endRect.top + endRect.height / 2;

                let lineLength = Math.sqrt(Math.pow(endX - startX, 2) + Math.pow(endY - startY, 2));
                let angle = Math.atan2(endY - startY, endX - startX) * 180 / Math.PI;

                line.style.width = `${{lineLength}}px`;
                line.style.top = `${{startY}}px`;
                line.style.left = `${{startX}}px`;
                line.style.transform = `rotate(${{angle}}deg)`;
            }}

            let lerpingElements = {{}};
            let resettingElements = {{}};
            const lerpDuration = {lerpDuration * 1000};
            const originalColor = '#000000'; // Define originalColor globally

            function triggerLerp(elementId) {{
                const now = performance.now();

                lerpingElements[elementId] = lerpingElements[elementId] || {{}};
                lerpingElements[elementId].latestTriggerTime = now;
                lerpingElements[elementId].lerping = true;
                lerpingElements[elementId].lerpStart = now; // Always reset lerpStart on new trigger
                lerpingElements[elementId].color = '#ff0000';

                requestAnimationFrame(function(timestamp) {{
                    lerpColor(timestamp, elementId);
                }});
            }}

            function lerpColor(time, elementId, restart) {{
                const state = lerpingElements[elementId];
                if (state && state.lerping) {{
                    if (state.latestTriggerTime > state.lerpStart) {{
                        state.lerpStart = state.latestTriggerTime;
                    }}
                    const elapsed = time - state.lerpStart;
                    const progress = Math.min(elapsed / lerpDuration, 1);
                    updateElementColor(elementId, state.color, progress);

                    if (elapsed < lerpDuration) {{
                        requestAnimationFrame(function(timestamp) {{
                            lerpColor(timestamp, elementId);
                        }});
                    }} else {{
                        state.lerping = false;
                        updateElementColor(elementId, originalColor, 1);
                        fetch(`/reset-lerp/${{elementId}}`, {{ method: 'POST' }});
                    }}
                }}
            }}

            function updateElementColor(elementId, targetColor, progress) {{
                const element = document.getElementById(elementId);
                if (element) {{
                    const interpolatedColor = interpolateColor(targetColor, originalColor, progress);
                    element.style.color = interpolatedColor;
                    element.style.backgroundColor = interpolatedColor;
                }}
            }}

            function interpolateColor(color1, color2, factor) {{
                var result = '#';
                for (let i = 1; i < 6; i += 2) {{
                    let val1 = parseInt(color1.substr(i, 2), 16);
                    let val2 = parseInt(color2.substr(i, 2), 16);
                    let val = Math.round(val1 + (val2 - val1) * factor).toString(16);
                    result += ('0' + val).substr(-2);
                }}
                return result;
            }}

            setInterval(function() {{
                fetch("/check-update")
                    .then(response => response.json())
                    .then(data => {{
                        var container = document.getElementById("circles-container");
                        if (data.triggered) {{
                            container.innerHTML = data.html;
                            drawLines();
                        }}
                        for (const elementId in data.lerpingElements) {{
                            if (data.resettingElements[elementId]) {{
                                triggerLerp(elementId);
                                fetch(`/reset-resetting/${{elementId}}`, {{ method: 'POST' }});
                            }}

                            resettingElements[elementId] = data.resettingElements[elementId];
                        }}
                    }})
                    .catch(error => console.error("Error:", error));
            }}, {msPerIteration});

        </script>

    </body>
    </html>
    '''

@app.route('/check-update')
def check_update():
    global color, triggered, lerpingElements, resettingElements
    response = {
        'triggered': triggered,
        'lerpingElements': lerpingElements,
        'resettingElements': resettingElements,
        'color': color,
        'html': generate_rows_html([3, 5, 5, 1]) if triggered else ""
    }
    return jsonify(response)

# Global variable for tracking lerping states
lerpingElements = {}
resettingElements = {}

@app.route('/trigger-red/<element_id>', methods=['POST'])
def trigger_specific_red(element_id):
    global lerpingElements, resettingElements
    resettingElements[element_id] = True  # If called while already lerping, reset lerp progress
    lerpingElements[element_id] = True  # Set the lerping state for the specific element
    return jsonify(success=True, message=f"Triggered red for {element_id}")

@app.route('/reset-resetting/<element_id>', methods=['POST'])
def reset_resetting(element_id):
    global resettingElements
    if element_id in resettingElements:
        resettingElements[element_id] = False
    return jsonify(success=True, message=f"Reset resetting state for {element_id}")

@app.route('/reset-lerp/<element_id>', methods=['POST'])
def reset_lerp(element_id):
    global lerpingElements
    # Remove the element from the lerping elements
    if element_id in lerpingElements:
        lerpingElements[element_id] = False
    return jsonify(success=True)

def reset_lerp_flag():
    global lerping
    lerping = False

@app.route('/trigger', methods=['POST'])
def trigger():
    global triggered
    triggered = True
    return jsonify(success=True)

def generate_rows_html(rows):
    html = ''
    for i, row_count in enumerate(rows):
        html += f'<div class="row">'
        for j in range(row_count):
            html += f'<div id="circle_{i}_{j}" class="circle"></div>'
        html += '</div>'
    return html

if __name__ == '__main__':
    app.run(debug=True)
