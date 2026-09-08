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

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Математический Супер-Центр", page_icon="🧮", layout="centered")
st.title("🧮 МАТЕМАТИЧЕСКИЙ СУПЕР-ЦЕНТР")

# СОЗДАЕМ ТАБЫ (ВКЛАДКИ)
tab1, tab2, tab3 = st.tabs(["🧮 2D & Калькулятор", "🧊 3D Режим", "🌌 Физический Симулятор"])

# ==================== ВКЛАДКА 1: 2D & КАЛЬКУЛЯТОР ====================
with tab1:
    st.subheader("Стандартные вычисления и 2D графики")
    operation = st.selectbox(
        "Выберите операцию:",
        ["Сложение", "Вычитание", "Умножение", "Деление", "Степень", "Квадратный корень", "Синус", "Косинус"],
        key="op2d"
    )

    num1, num2, deg, quad_a, quad_b, quad_c = 0.0, 0.0, 0.0, 1.0, 0.0, 0.0

    if operation in ["Сложение", "Вычитание", "Умножение", "Деление", "Степень"]:
        num1 = st.number_input("Введите первое число:", value=0.0, key="n1")
        num2 = st.number_input("Введите второе число:", value=0.0, key="n2")
    elif operation == "Квадратный корень":
        num1 = st.number_input("Введите число для корня:", value=0.0, key="n1_sqrt")
    elif operation in ["Синус", "Косинус"]:
        deg = st.number_input("Введите угол в градусах:", value=0.0, key="deg")

    def calculate_math(op, n1, n2, dg):
        try:
            if op == "Сложение": return f"Результат: {n1 + n2}"
            elif op == "Вычитание": return f"Результат: {n1 - n2}"
            elif op == "Умножение": return f"Результат: {n1 * n2}"
            elif op == "Деление": return f"Результат: {n1 / n2}" if n2 != 0 else "Ошибка: Деление на ноль"
            elif op == "Степень": return f"Результат: {n1 ** n2}"
            elif op == "Квадратный корень": return f"Результат: {math.sqrt(n1)}" if n1 >= 0 else "Ошибка: Корень из отрицательного числа"
            elif op == "Синус": return f"Результат: {math.sin(math.radians(dg))}"
            elif op == "Косинус": return f"Результат: {math.cos(math.radians(dg))}"
        except Exception as e:
            return f"Ошибка: {str(e)}"

    if st.button("Вычислить", key="btn_calc"):
        res = calculate_math(operation, num1, num2, deg)
        st.success(res)

    if operation in ["Синус", "Косинус"]:
        if st.button("Показать 2D График", key="btn_2d"):
            x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
            fig, ax = plt.subplots(figsize=(8, 3.5))
            if operation == "Синус":
                ax.plot(np.degrees(x), np.sin(x), label='y = sin(x)', color='blue')
                ax.scatter(deg, math.sin(math.radians(deg)), color='red', s=100)
            else:
                ax.plot(np.degrees(x), np.cos(x), label='y = cos(x)', color='green')
                ax.scatter(deg, math.cos(math.radians(deg)), color='red', s=100)
            ax.axhline(0, color='black', linewidth=0.5)
            ax.grid(True, linestyle='--', alpha=0.5)
            ax.set_title(f"График {operation}")
            st.pyplot(fig)

# ==================== ВКЛАДКА 2: 3D РЕЖИМ ====================
with tab2:
    st.subheader("Визуализация 3D Поверхностей")
    st.write("Построение трехмерного графика функции волны: $z = \\sin(\\sqrt{x^2 + y^2})$")
    
    grid_size = st.slider("Разрешение сетки (чем больше, тем точнее график):", 20, 100, 50)
    
    if st.button("Сгенерировать 3D График", key="btn_3d"):
        x = np.linspace(-5, 5, grid_size)
        y = np.linspace(-5, 5, grid_size)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        Z = np.sin(R)  # Функция красивой 3D волны

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        # Строим поверхность с цветовой картой 'viridis'
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)
        
        ax.set_xlabel('Ось X')
        ax.set_ylabel('Ось Y')
        ax.set_zlabel('Ось Z')
        ax.set_title("3D Математическая Поверхность")
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
        
        st.pyplot(fig)

# ==================== ВКЛАДКА 3: ФИЗИЧЕСКИЙ СИМУЛЯТОР ====================
with tab3:
    st.subheader("🌌 Модель искривления пространства (Гравитация Эйнштейна)")
    st.write("Согласно ОТО, массивные объекты прогибают пространство-время. Чем больше масса, тем сильнее искривление и гравитация.")
    
    # Выбор космического тела
    object_type = st.select_slider(
        "Выберите космический объект (увеличение массы):",
        options=["Земля", "Юпитер", "Солнце", "Нейтронная звезда", "Черная дыра"]
    )
    
    # Задаем глубину прогиба в зависимости от выбора
    mass_weight = {"Земля": 0.5, "Юпитер": 1.2, "Солнце": 3.0, "Нейтронная звезда": 7.0, "Черная дыра": 15.0}
    depth = mass_weight[object_type]
    
    st.info(f"Выбран объект: **{object_type}**. Генерация гравитационной воронки...")
    
    # Рассчитываем воронку гравитации
    x_space = np.linspace(-4, 4, 60)
    y_space = np.linspace(-4, 4, 60)
    X_s, Y_s = np.meshgrid(x_space, y_space)
    
    # Формула гравитационного колодца (потенциал)
    R_s = np.sqrt(X_s**2 + Y_s**2) + 0.5
    Z_s = -depth / (R_s)  # Уходит вниз, образуя воронку
    
    fig_space = plt.figure(figsize=(10, 6))
    ax_s = fig_space.add_subplot(111, projection='3d')
    
    # Отображаем в виде координатной сетки (как ткань пространства)
    ax_s.plot_wireframe(X_s, Y_s, Z_s, color='cyan', linewidth=0.5, rstride=3, cstride=3)
    
    # Рисуем саму планету/дыру в центре воронки
    ax_s.scatter([0], [0], [-depth/0.5], color='red' if object_type=="Черная дыра" else 'orange', s=200, label=object_type)
    
    ax_s.set_zlim(-20, 1)
    ax_s.set_title(f"Искривление пространства-времени объектом: {object_type}")
    ax_s.axis('off') # Убираем лишние оси, оставляя только красивую сетку
    
    st.pyplot(fig_space)
