import streamlit as st
import streamlit.components.v1 as components
import math
import matplotlib.pyplot as plt
import numpy as np

# ==================== БЛОК ДЛЯ ЗАПУСКА КАК ПРИЛОЖЕНИЕ (PWA) ====================
pwa_html = """
<script>
const manifest = {
  "short_name": "MatchCentr",
  "name": "Математический Супер-Центр",
  "icons": [
    {
      "src": "https://flaticon.com",
      "sizes": "512x512",
      "type": "image/png"
    }
  ],
  "start_url": "/",
  "background_color": "#0e1117",
  "theme_color": "#ff4b4b",
  "display": "standalone",
  "orientation": "portrait"
};

const stringManifest = JSON.stringify(manifest);
const blob = new Blob([stringManifest], {type: 'application/json'});
const manifestURL = URL.createObjectURL(blob);
const link = document.createElement('link');
link.rel = 'manifest';
link.href = manifestURL;
document.head.appendChild(link);

const swCode = "self.addEventListener('fetch', function(event) {});";
const swBlob = new Blob([swCode], {type: 'application/javascript'});
const swURL = URL.createObjectURL(swBlob);

if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register(swURL)
    .then(() => console.log('PWA готов!'))
    .catch(err => console.log('Ошибка PWA:', err));
}
</script>
"""
components.html(pwa_html, height=0, width=0)
# ===============================================================================

# НАСТРОЙКА СТРАНИЦЫ И ИНТЕРФЕЙСА
st.set_page_config(page_title="Математический Супер-Центр", page_icon="🧮", layout="centered")
st.title("🧮 МАТЕМАТИЧЕСКИЙ СУПЕР-ЦЕНТР")

# Выбор операции
operation = st.selectbox(
    "Выберите математическую операцию:",
    ["Сложение", "Вычитание", "Умножение", "Деление", "Степень", "Квадратный корень", "Синус", "Косинус"]
)

# Переменные по умолчанию для функции вычислений
num1, num2, deg, quad_a, quad_b, quad_c = 0.0, 0.0, 0.0, 1.0, 0.0, 0.0

# Отображаем нужные поля ввода в зависимости от операции
if operation in ["Сложение", "Вычитание", "Умножение", "Деление", "Степень"]:
    num1 = st.number_input("Введите первое число:", value=0.0)
    num2 = st.number_input("Введите второе число:", value=0.0)
elif operation == "Квадратный корень":
    num1 = st.number_input("Введите число для извлечения корня:", value=0.0)
elif operation in ["Синус", "Косинус"]:
    deg = st.number_input("Введите угол в градусах:", value=0.0)

# --- Логика вычислений ---
def calculate_math(op, num1, num2, deg, quad_a, quad_b, quad_c):
    try:
        if op == "Сложение": return f"Результат: {num1 + num2}"
        elif op == "Вычитание": return f"Результат: {num1 - num2}"
        elif op == "Умножение": return f"Результат: {num1 * num2}"
        elif op == "Деление": return f"Результат: {num1 / num2}" if num2 != 0 else "Ошибка: Деление на ноль"
        elif op == "Степень": return f"Результат: {num1 ** num2}"
        elif op == "Квадратный корень": return f"Результат: {math.sqrt(num1)}" if num1 >= 0 else "Ошибка: Корень из отрицательного числа"
        elif op == "Синус": return f"Результат: {math.sin(math.radians(deg))}"
        elif op == "Косинус": return f"Результат: {math.cos(math.radians(deg))}"
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Кнопка для запуска вычислений и вывод результата
if st.button("Вычислить"):
    result = calculate_math(operation, num1, num2, deg, quad_a, quad_b, quad_c)
    st.success(result)
