from flask import Flask, jsonify
import threading

app = Flask(__name__)

# Global variables
triggered = False
color = "black"
lerping = False

lerpDuration = 1

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
            .line {{}}
        </style>
    </head>
    <body>
        <div id="circles-container">{content}</div>
        <div id="lines-container"></div>
        <script>
            let lerping = false;
            let lerpStart = 0;
            const lerpDuration = {lerpDuration*1000}; // LERP back over 1 second
            const originalColor = '#000000'; // Original color
            const lerpCol = '#ff0000'; // Temporary color

            function triggerLerp() {{
                lerping = true;
                lerpStart = performance.now();
                requestAnimationFrame(lerpColor);
            }}

            function lerpColor(time) {{
                if (lerping) {{
                    const elapsed = time - lerpStart;
                    const progress = Math.min(elapsed / lerpDuration, 1); // Cap progress at 1
                    console.log(progress)

                    updateCircleColors(progress);

                    if (elapsed < lerpDuration) {{
                        requestAnimationFrame(lerpColor);
                    }} else {{
                        lerping = false;
                    }}
                }}
            }}

            function updateCircleColors(progress) {{
                var circles = document.getElementsByClassName('circle');
                var lines = document.getElementsByClassName('line');
                const color = progress < 1 ? interpolateColor(lerpCol, originalColor, progress) : originalColor;
                for (let circle of circles) {{
                    circle.style.backgroundColor = color;
                }}
                for (let line of lines) {{
                    line.style.backgroundColor = color;
                    line.style.color = color;
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

                            let lineStyle = `position: absolute; width: ${{lineLength}}px; height: 5px; background-color: black; top: ${{startY}}px; left: ${{startX}}px; transform: rotate(${{angle}}deg); transform-origin: 0 0;`;

                            let line = document.createElement("div");
                            line.className = "line";
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
                        if (data.lerping && !lerping) {{
                            triggerLerp();
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
    global color, triggered, lerping
    return jsonify(triggered=triggered, lerping=lerping, color=color, html=generate_rows_html([3, 5, 5, 1]) if triggered else "")

@app.route('/trigger-red', methods=['POST'])
def trigger_red():
    global lerping
    lerping = True
    # Start a timer to reset the lerping flag after the lerp duration
    threading.Timer(lerpDuration, reset_lerp_flag).start()
    return jsonify(success=True)

def reset_lerp_flag():
    global lerping
    lerping = False

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
