from flask import Flask, render_template_string, request

app = Flask(__name__)


def get_color_name(hex_color):
    color_names = {
        '#ff0000': 'أحمر قانٍ',
        '#00ff00': 'أخضر زمردي',
        '#0000ff': 'أزرق بحري',
        '#ffff00': 'أصفر كناري',
        '#ffffff': 'أبيض ناصع',
        '#000000': 'أسود فاحم',
        '#ff00ff': 'أرجواني ملكي',
        '#00ffff': 'تركواز فاتح',
        '#ffa500': 'برتقالي مشمشي',
        '#808080': 'رمادي داكن',
        '#800080': 'بنفسجي غامق',
        '#8b0000': 'أحمر عنابي',
        '#ffd700': 'ذهبي لامع',
        '#adff2f': 'ليموني زاهي',
        '#dc143c': 'قرمزي داكن'
    }
    return color_names.get(hex_color.lower(), 'لون غير معروف')


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    # الاحتفاظ بالقيم المدخلة لعرضها مرة أخرى
    red_input = request.form.get("red", "0")
    green_input = request.form.get("green", "0")
    blue_input = request.form.get("blue", "0")
    white_input = request.form.get("white", "0")
    manual_color_input = request.form.get("manual_color", "#ffffff")

    if request.method == "POST":
        try:
            # استخدام اللون اليدوي فقط إذا تم تغييره عن القيمة الافتراضية
            if manual_color_input.strip() != "#ffffff":
                manual_color = manual_color_input.strip()
                if not manual_color.startswith("#"):
                    manual_color = f"#{manual_color}"
                color_name = get_color_name(manual_color)
                result = {
                    "color": manual_color,
                    "color_name": color_name,
                    "ratio": "تم اختيار اللون يدويًا"
                }
            else:
                # تحويل الإدخالات إلى أرقام من 0 إلى 5
                red_value = int(red_input) if red_input.isdigit() else 0
                green_value = int(green_input) if green_input.isdigit() else 0
                blue_value = int(blue_input) if blue_input.isdigit() else 0
                white_value = int(white_input) if white_input.isdigit() else 0

                total = red_value + green_value + blue_value + white_value
                if total == 0:
                    error = "يرجى إدخال نسب صحيحة!"
                else:
                    # بما أن القيم تتراوح من 0 إلى 5، فإن أقصى مجموع ممكن هو 20.
                    # يتم حساب النسبة التناسبية ثم ضربها في 255 للحصول على قيمة اللون.
                    red_ratio = int((red_value / total) * 255)
                    green_ratio = int((green_value / total) * 255)
                    blue_ratio = int((blue_value / total) * 255)
                    new_color = f'#{red_ratio:02x}{green_ratio:02x}{blue_ratio:02x}'
                    color_name = get_color_name(new_color)
                    ratio_text = (f"أحمر: {red_value}/5 | "
                                  f"أخضر: {green_value}/5 | "
                                  f"أزرق: {blue_value}/5 | "
                                  f"أبيض: {white_value}/5")
                    result = {
                        "color": new_color,
                        "color_name": color_name,
                        "ratio": ratio_text
                    }
        except Exception as e:
            error = str(e)

    html = """
    <!doctype html>
    <html lang="ar">
    <head>
      <meta charset="utf-8">
      <title>دمج الألوان</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&display=swap');
        body { 
            font-family: 'Tajawal', sans-serif; 
            direction: rtl; 
            text-align: center; 
            margin: 20px;
            background-color: #f0f0f0;
            color: #333;
        }
        .container {
            max-width: 500px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .color-box-container {
            max-width: 500px;
            margin: 20px auto;
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }
        .color-box { 
            width: 250px; 
            height: 120px; 
            margin: 20px auto; 
            border-radius: 8px;
            border: 2px solid #ccc;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.2);
        }
        form { 
            margin-top: 20px; 
            display: flex;
            flex-direction: column;
            gap: 10px;
        }
        input, button { 
            padding: 10px; 
            font-size: 16px;
            border-radius: 5px;
            border: 1px solid #ccc;
            text-align: center;
        }
        button {
            background-color: #007bff;
            color: white;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        button:hover {
            background-color: #0056b3;
        }
        .teacher {
            margin-top: 15px; 
            font-size: 26px; 
            font-weight: bold; 
            color: #007bff;
        }
        .result-text {
            font-size: 18px;
            font-weight: bold;
            margin-top: 10px;
        }
        .error {
            color: red;
            font-weight: bold;
        }
        label { display: block; }
      </style>
    </head>
    <body>
      <div class="container">
        <h1>دمج الألوان باستخدام النسبة والتناسب</h1>
        <div class="teacher">إعداد المعلمة: رنا العامرية</div>
        <form method="POST">
          <label>أحمر (0-5): <input type="text" name="red" placeholder="0" value="{{ red_input }}"></label>
          <label>أخضر (0-5): <input type="text" name="green" placeholder="0" value="{{ green_input }}"></label>
          <label>أزرق (0-5): <input type="text" name="blue" placeholder="0" value="{{ blue_input }}"></label>
          <label>أبيض (0-5): <input type="text" name="white" placeholder="0" value="{{ white_input }}"></label>
          <hr>
          <label>أو اختر لوناً يدويًا: <input type="color" name="manual_color" value="{{ manual_color_input }}"></label>
          <button type="submit">دمج الألوان</button>
        </form>
      </div>

      {% if error %}
      <p class="error">{{ error }}</p>
      {% endif %}

      {% if result %}
      <div class="color-box-container">
        <h2>اللون الناتج:</h2>
        <div class="color-box" style="background-color: {{ result.color }};"></div>
        <p class="result-text">{{ result.color_name }}</p>
        <p>{{ result.ratio }}</p>
      </div>
      {% endif %}

    </body>
    </html>
    """
    return render_template_string(html, result=result, error=error,
                                  red_input=red_input,
                                  green_input=green_input,
                                  blue_input=blue_input,
                                  white_input=white_input,
                                  manual_color_input=manual_color_input)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
