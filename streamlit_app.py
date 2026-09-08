import streamlit as st
import streamlit.components.v1 as components
import math
import matplotlib.pyplot as plt
import numpy as np

# ==================== УЛУЧШЕННЫЙ БЛОК ДЛЯ ЗАПУСКА КАК ПРИЛОЖЕНИЕ (PWA) ====================
YOUR_GITHUB_ICON = "https://githubusercontent.com"

pwa_html = f"""
<script>
const manifest = {{
  "short_name": "MatchCentr",
  "name": "Математический Супер-Центр",
  "icons": [
    {{ "src": "{YOUR_GITHUB_ICON}", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }},
    {{ "src": "{YOUR_GITHUB_ICON}", "sizes": "192x192", "type": "image/png" }}
  ],
  "start_url": ".",
  "background_color": "#0e1117",
  "theme_color": "#ff4b4b",
  "display": "standalone",
  "orientation": "portrait"
}};

const stringManifest = JSON.stringify(manifest);
const blob = new Blob([stringManifest], {{type: 'application/json'}});
document.head.appendChild(Object.assign(document.createElement('link'), {{rel: 'manifest', href: URL.createObjectURL(blob)}}));

const swCode = `
  self.addEventListener('install', e => self.skipWaiting());
  self.addEventListener('activate', e => e.waitUntil(self.clients.claim()));
  self.addEventListener('fetch', e => e.respondWith(fetch(e.request)));
`;
const swBlob = new Blob([swCode], {{type: 'application/javascript'}});
navigator.serviceWorker.register(URL.createObjectURL(swBlob));

// Логика кастомной кнопки установки
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {{
  e.preventDefault();
  deferredPrompt = e;
  // Показываем кнопку в Streamlit, посылая сигнал наружу
  window.parent.postMessage({{type: 'SHOW_INSTALL_BTN'}}, '*');
}});

window.addEventListener('message', (e) => {{
  if (e.data.type === 'TRIGGER_INSTALL' && deferredPrompt) {{
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then(() => {{ deferredPrompt = null; }});
  }}
}});
</script>
"""
components.html(pwa_html, height=0, width=0)

# JS-мост для вызова нативного окна Chrome по кнопке из Streamlit
def trigger_install_js():
    components.html("""
    <script>
    window.parent.postMessage({type: 'TRIGGER_INSTALL'}, '*');
    </script>
    """, height=0, width=0)
# =========================================================================================

# НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="Математический Супер-Центр", page_icon="🧮", layout="centered")

# Кнопка установки приложения прямо в шапке сайта
col1, col2 = st.columns([2, 1])
with col1:
    st.title("🧮 СУПЕР-ЦЕНТР")
with col2:
    if st.button("📲 Установить на телефон"):
        trigger_install_js()

# СОЗДАЕМ ЧЕТЫРЕ ВКЛАДКИ
tab1, tab2, tab3, tab4 = st.tabs(["🧮 Калькулятор & Квадратные уравнения", "📈 2D Графики", "🧊 3D Режим", "🌌 Физика"])

# ==================== ВКЛАДКА 1: КАЛЬКУЛЯТОР & ДИСКРИМИНАНТ ====================
with tab1:
    calc_type = st.radio("Выберите тип калькулятора:", ["Обычные вычисления", "Дискриминант (Квадратное уравнение)"])
    
    if calc_type == "Обычные вычисления":
        operation = st.selectbox(
            "Выберите операцию:",
            ["Сложение", "Вычитание", "Умножение", "Деление", "Степень", "Квадратный корень"],
            key="basic_op"
        )
        
        if operation in ["Сложение", "Вычитание", "Умножение", "Деление", "Степень"]:
            num1 = st.number_input("Введите первое число:", value=0.0, key="calc_n1")
            num2 = st.number_input("Введите второе число:", value=0.0, key="calc_n2")
        else:
            num1 = st.number_input("Введите число для корня:", value=0.0, key="calc_sqrt")
            num2 = 0.0

        if st.button("Вычислить", key="btn_basic"):
            try:
                if operation == "Сложение": st.success(f"Результат: {num1 + num2}")
                elif operation == "Вычитание": st.success(f"Результат: {num1 - num2}")
                elif operation == "Умножение": st.success(f"Результат: {num1 * num2}")
                elif operation == "Деление": st.success(f"Результат: {num1 / num2}" if num2 != 0 else "Ошибка: Деление на ноль")
                elif operation == "Степень": st.success(f"Результат: {num1 ** num2}")
                elif operation == "Квадратный корень": st.success(f"Результат: {math.sqrt(num1)}" if num1 >= 0 else "Ошибка: Корень из отрицательного числа")
            except Exception as e:
                st.error(f"Ошибка: {str(e)}")
                
    else:
        st.subheader("Решение уравнения вида $ax^2 + bx + c = 0$")
        a = st.number_input("Введите коэффициент a:", value=1.0, key="quad_a")
        b = st.number_input("Введите коэффициент b:", value=0.0, key="quad_b")
        c = st.number_input("Введите коэффициент c:", value=0.0, key="quad_c")
        
        if st.button("Рассчитать дискриминант", key="btn_discr"):
            if a == 0:
                st.error("Коэффициент 'a' не может быть равен нулю в квадратном уравнении!")
            else:
                D = b**2 - 4*a*c
                st.write(f"**Дискриминант ($D$)** = $b^2 - 4ac$ = {b}^2 - 4 \\cdot {a} \\cdot {c} = **{D}**")
                
                if D > 0:
                    x1 = (-b + math.sqrt(D)) / (2 * a)
                    x2 = (-b - math.sqrt(D)) / (2 * a)
                    st.success(f"Дискриминант > 0. Уравнение имеет два корня:\n\n**x₁** = {x1:.4f}\n\n**x₂** = {x2:.4f}")
                elif D == 0:
                    x = -b / (2 * a)
                    st.success(f"Дискриминант = 0. Уравнение имеет один корень:\n\n**x** = {x:.4f}")
                else:
                    st.error("Дискриминант < 0. Действительных корней нет (корни комплексные).")

# ==================== ВКЛАДКА 2: 2D ГРАФИКИ ====================
with tab2:
    st.subheader("Построение тригонометрических 2D графиков")
    graph_op = st.selectbox("Выберите функцию для графика:", ["Синус", "Косинус"], key="graph_op_select")
    deg = st.number_input("Введите точку (угол в градусах) для отметки на графике:", value=0.0, key="graph_deg")
    
    if st.button("Показать 2D График", key="btn_2d_tab"):
        x = np.linspace(-2 * np.pi, 2 * np.pi, 1000)
        fig, ax = plt.subplots(figsize=(8, 4))
        
        if graph_op == "Синус":
            y = np.sin(x)
            current_y = math.sin(math.radians(deg))
            ax.plot(np.degrees(x), y, label='y = sin(x)', color='blue', linewidth=2)
            ax.scatter(deg, current_y, color='red', s=120, zorder=5, label=f'Ваша точка ({deg}°, {current_y:.2f})')
        else:
            y = np.cos(x)
            current_y = math.cos(math.radians(deg))
            ax.plot(np.degrees(x), y, label='y = cos(x)', color='green', linewidth=2)
            ax.scatter(deg, current_y, color='red', s=120, zorder=5, label=f'Ваша точка ({deg}°, {current_y:.2f})')
            
        ax.axhline(0, color='black', linewidth=0.5)
        ax.axvline(0, color='black', linewidth=0.5)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_xlabel('Градусы')
        ax.set_ylabel('Значение')
        ax.set_title(f"2D График функции {graph_op}")
        ax.legend()
        st.pyplot(fig)

# ==================== ВКЛАДКА 3: 3D РЕЖИМ ====================
with tab3:
    st.subheader("Визуализация 3D Поверхностей")
    st.write("Построение трехмерной волны: $z = \\sin(\\sqrt{{x^2 + y^2}})$")
    grid_size = st.slider("Разрешение сетки:", 20, 100, 50, key="grid_slider")
    
    if st.button("Сгенерировать 3D График", key="btn_3d_tab"):
        x = np.linspace(-5, 5, grid_size)
        y = np.linspace(-5, 5, grid_size)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        Z = np.sin(R)

        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(111, projection='3d')
        surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)
        ax.set_title("3D Поверхность")
        fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10)
        st.pyplot(fig)

# ==================== ВКЛАДКА 4: ФИЗИКА ====================
with tab4:
    st.subheader("🌌 Искривление пространства-времени (Гравитация Эйнштейна)")
    object_type = st.select_slider(
        "Выберите космический объект:",
        options=["Земля", "Юпитер", "Солнце", "Нейтронная звезда", "Черная дыра"],
        key="physics_slider"
    )
    
    mass_weight = {"Земля": 0.5, "Юпитер": 1.2, "Солнце": 3.0, "Нейтронная звезда": 7.0, "Черная дыра": 15.0}
    depth = mass_weight[object_type]
    
    x_space = np.linspace(-4, 4, 60)
    y_space = np.linspace(-4, 4, 60)
    X_s, Y_s = np.meshgrid(x_space, y_space)
    R_s = np.sqrt(X_s**2 + Y_s**2) + 0.5
    Z_s = -depth / R_s
    
    fig_space = plt.figure(figsize=(10, 6))
    ax_s = fig_space.add_subplot(111, projection='3d')
    ax_s.plot_wireframe(X_s, Y_s, Z_s, color='cyan', linewidth=0.5, rstride=3, cstride=3)
    ax_s.scatter(0, 0, -depth/0.5, color='red' if object_type=="Черная дыра" else 'orange', s=200)
    ax_s.set_zlim(-20, 1)
    ax_s.axis('off')
    st.pyplot(fig_space)
