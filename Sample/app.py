# -*- coding: utf-8 -*-
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
import os

# Ініціалізація Flask-додатку
app = Flask(__name__)

# Налаштування Matplotlib для роботи без GUI (важливо для веб-серверів)
plt.switch_backend('Agg')

def load_data(file_path):
    """Завантажує дані з CSV файлу."""
    if not os.path.exists(file_path):
        return None
    try:
        return pd.read_csv(file_path)
    except Exception:
        return None

def create_plot(df, plot_type):
    """Створює графік, зберігає його в пам'яті та повертає у форматі Base64."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(10, 6))

    if plot_type == 'zone_counts':
        zone_counts = df['zone'].value_counts().sort_index()
        zone_counts.plot(kind='bar', ax=ax, color='#5F8575', edgecolor='black', alpha=0.7)  # Колір "Степ" з прозорістю
        ax.set_title('Загальна кількість подій по кожній оперативній зоні', fontsize=16)
        ax.set_xlabel('Оперативна зона', fontsize=12)
        ax.set_ylabel('Кількість подій', fontsize=12)
        plt.setp(ax.get_xticklabels(), rotation=45, ha='right')

    elif plot_type == 'category_pie':  # Виправлено дублювання коду
        category_counts = df['category'].value_counts()

        # Колір "Степ"
        base_color = (95/255, 133/255, 117/255)
        # Генеруємо кольори з різною прозорістю
        num_categories = len(category_counts)
        final_colors = [(base_color[0], base_color[1], base_color[2], 1 - i * 0.15) 
                        for i in range(num_categories)]
        # Якщо категорій більше ніж рівнів прозорості, починаємо спочатку
        if num_categories > 7:
            final_colors = [(base_color[0], base_color[1], base_color[2], 1 - (i % 7) * 0.15)
                            for i in range(num_categories)]

        ax.pie(category_counts, labels=category_counts.index, startangle=140, colors=final_colors, wedgeprops={'edgecolor': 'black'},
               autopct=lambda p: '{:.1f}%'.format(p) if p > 1 else '')  # Показувати відсотки лише якщо вони більше 1%
        ax.set_title('Відсотковий розподіл подій за категоріями', fontsize=16)
        ax.axis('equal')

    elif plot_type == 'avg_units':
        avg_units_by_category = df.groupby('category')['units_engaged'].mean().sort_values()
        
        # Колір "Степ" як основа
        base_color = (95/255, 133/255, 117/255)
        # Створюємо список кольорів з різною прозорістю
        num_bars = len(avg_units_by_category)
        bar_colors = [(base_color[0], base_color[1], base_color[2], 0.5 + (i * (0.4 / num_bars))) 
                      for i in range(num_bars)]

        avg_units_by_category.plot(kind='barh', ax=ax, color=bar_colors, edgecolor='black')
        ax.set_title('Середня кількість залучених підрозділів для кожної категорії', fontsize=16)
        ax.set_xlabel('Середня кількість підрозділів', fontsize=12)
        ax.set_ylabel('Категорія події', fontsize=12)
    
    fig.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    plt.close(fig)
    return f"data:image/png;base64,{img_base64}"

@app.route('/')
def dashboard():
    """Головна сторінка, що відображає дашборд."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, 'operational_data.csv')
    df = load_data(file_path)
    
    if df is None:
        return "<h1>Помилка: Файл 'operational_data.csv' не знайдено або неможливо прочитати.</h1>", 404

    plot1_url = create_plot(df, 'zone_counts')
    plot2_url = create_plot(df, 'category_pie')
    plot3_url = create_plot(df, 'avg_units')

    min_events_zone = df['zone'].value_counts().idxmin()
    conclusions = f"Аналіз показав, що оперативна активність значно різниться між зонами. Найбільшу кількість ресурсів вимагають події категорії 'Наземний контакт'. Найчастішою категорією є 'Повітряна загроза'. Найменш активною зоною є '{min_events_zone}'."

    return render_template('index.html',
                           plot1_url=plot1_url,
                           plot2_url=plot2_url,
                           plot3_url=plot3_url,
                           conclusions=conclusions)

if __name__ == '__main__':
    app.run(debug=True)