from flask import Flask, render_template, jsonify, request
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()

        a = float(data.get('a', 1))
        b = float(data.get('b', 0))
        c = float(data.get('c', 0))

        xmin = float(data.get('xmin', -50))
        xmax = float(data.get('xmax', 50))

        # Բարձր որակ - "անվերջ" էֆեկտ
        # Ըստ միջակայքի երկարության որոշել կետերի քանակը
        range_length = xmax - xmin
        num_points = min(10000, int(range_length * 100))
        num_points = max(num_points, 100)  # առնվազն 100 կետ

        x = np.linspace(xmin, xmax, num_points)
        y = a * x**2 + b * x + c

        # գագաթ (պաշտպանել զրոյի բաժանումից)
        if a != 0:
            vertex_x = -b / (2 * a)
            vertex_y = a * vertex_x**2 + b * vertex_x + c
        else:
            vertex_x = 0
            vertex_y = c

        # ֆոկուս և ուղղաձիգ
        if a != 0:
            p = 1 / (4 * a)
            focus_x = vertex_x
            focus_y = vertex_y + p
            directrix_y = vertex_y - p
        else:
            p = 0
            focus_x = vertex_x
            focus_y = vertex_y
            directrix_y = vertex_y

        return jsonify({
            'success': True,
            'x': x.tolist(),
            'y': y.tolist(),
            'vertex': [vertex_x, vertex_y],
            'focus': [focus_x, focus_y],
            'directrix': directrix_y,
            'p': p,
            'num_points': num_points
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
