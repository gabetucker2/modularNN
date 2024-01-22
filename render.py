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
        <title>Dynamic Circles and Lines</title>
        <style>
            .circle {{
                width: 100px;
                height: 100px;
                line-height: 100px;
                border-radius: 50%;
                display: inline-block;
                margin: 10px;
                color: white;
                text-align: center;
                font-size: 16px;
                font-weight: bold;
                background-color: {color};
            }}
            .row {{
                text-align: center;
            }}
            /* Additional styles for lines here */
        </style>
    </head>
    <body>
        <div id="circles-container">{content}</div>
        <script>
            setInterval(function() {{
                fetch('/check-update')
                    .then(response => response.json())
                    .then(data => {{
                        var container = document.getElementById('circles-container');
                        if (data.triggered) {{
                            container.innerHTML = data.html;
                        }}
                        var circles = container.getElementsByClassName('circle');
                        for (var i = 0; i < circles.length; i++) {{
                            circles[i].style.backgroundColor = data.color;
                        }}
                    }})
                    .catch(error => console.error('Error:', error));
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
