import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Математический Супер-Центр", page_icon="🌌", layout="centered")
st.title("🌌 МАТЕМАТИЧЕСКИЙ СУПЕР-ЦЕНТР")

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
        elif op == "Тангенс": return f"Результат: {math.tan(math.radians(deg))}" if deg % 180 != 90 else "Ошибка: Тангенс не существует"
        elif op == "Квадратное уравнение":
            if quad_a == 0: return "Ошибка: a = 0"
            D = quad_b**2 - 4*quad_a*quad_c
            if D > 0:
                x1 = (-quad_b + math.sqrt(D)) / (2*quad_a)
                x2 = (-quad_b - math.sqrt(D)) / (2*quad_a)
                return f"D = {D}; x1 = {x1:.4f}; x2 = {x2:.4f}"
            elif D == 0:
                x = -quad_b / (2*quad_a)
                return f"D = 0; x = {x:.4f}"
            else:
                return f"D = {D}; Действительных корней нет"
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Создание вкладок
tab1, tab2, tab3 = st.tabs(["🧮 Калькулятор и Уравнения", "📈 Графики 2D", "🛸 Графики 3D"])

# --- ВКЛАДКА 1 ---
with tab1:
    operation = st.selectbox("Выберите операцию", ["Сложение", "Вычитание", "Умножение", "Деление", "Степень", "Квадратный корень", "Синус", "Косинус", "Тангенс", "Квадратное уравнение"])
    
    num1, num2 = 0.0, 0.0
    deg = 0.0
    quad_a, quad_b, quad_c = 1.0, 0.0, 0.0
    
    if operation in ["Сложение", "Вычитание", "Умножение", "Деление", "Степень", "Квадратный корень"]:
        num1 = st.number_input("Число 1 / Основное число", value=0.0)
        if operation != "Квадратный корень":
            num2 = st.number_input("Число 2 / Степень", value=0.0)
    elif operation in ["Синус", "Косинус", "Тангенс"]:
        deg = st.number_input("Угол в градусах", value=0.0)
    elif operation == "Квадратное уравнение":
        quad_a = st.number_input("Коэффициент a", value=1.0)
        quad_b = st.number_input("Коэффициент b", value=0.0)
        quad_c = st.number_input("Коэффициент c", value=0.0)
        
    if st.button("Рассчитать", type="primary"):
        res = calculate_math(operation, num1, num2, deg, quad_a, quad_b, quad_c)
        st.success(res)

# --- ВКЛАДКА 2 ---
with tab2:
    st.markdown("### Построение математических функций на плоскости")
    func_2d_type = st.radio("Выберите график", ["Синусоида (sin x)", "Парабола (x²)", "Кубическая парабола (x³)", "Своя функция (введите формулу)"])
    
    custom_expr = ""
    if func_2d_type == "Своя функция (введите формулу)":
        custom_expr = st.text_input("Формула (например: np.sin(x) * x)", value="np.sin(x) * x")
        
    if st.button("Построить 2D График"):
        fig, ax = plt.subplots(figsize=(6, 4))
        x = np.linspace(-10, 10, 400)
        try:
            if func_2d_type == "Синусоида (sin x)":
                y, title = np.sin(x), "y = sin(x)"
            elif func_2d_type == "Парабола (x²)":
                y, title = x**2, "y = x²"
            elif func_2d_type == "Кубическая парабола (x³)":
                y, title = x**3, "y = x³"
            else:
                allowed = {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan}
                y = eval(custom_expr, {"__builtins__": {}}, allowed)
                title = f"y = {custom_expr}"
            ax.plot(x, y, color="#FF6B6B", linewidth=2.5)
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.set_title(title, fontweight="bold")
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Ошибка в формуле: {e}")

# --- ВКЛАДКА 3 ---
with tab3:
    st.markdown("### Трехмерные математические поверхности")
    func_3d_type = st.radio("Выберите 3D поверхность", ["3D Волна (Синус от расстояния)", "3D Сёдла / Гиперболический параболоид", "3D Горка / Гауссиан"])
    
    if st.button("Сгенерировать 3D Модель"):
        fig = plt.figure(figsize=(7, 5))
        ax = fig.add_subplot(111, projection='3d')
        x = y = np.linspace(-5, 5, 100)
        X, Y = np.meshgrid(x, y)
        
        if func_3d_type == "3D Волна (Синус от расстояния)":
            Z, cmap = np.sin(np.sqrt(X**2 + Y**2)), "coolwarm"
        elif func_3d_type == "3D Сёдла / Гиперболический параболоид":
            Z, cmap = X**2 - Y**2, "twilight"
        else:
            Z, cmap = np.exp(-(X**2 + Y**2)/4), "viridis"
            
        surf = ax.plot_surface(X, Y, Z, cmap=cmap, edgecolor='none', alpha=0.8)
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
        st.pyplot(fig)
