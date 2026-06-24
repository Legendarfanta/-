"""
🍎 СКАНЕР ПРОДУКТОВ ПИТАНИЯ - ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
Приложение для распознавания фруктов и овощей с помощью ИИ
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk, font
from PIL import Image, ImageTk
import numpy as np
import tensorflow as tf
import os
import sys
from datetime import datetime
import json
import webbrowser

# Добавляем пути для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from product_database import ProductDatabase
from image_processor import ImageProcessor
from nutrition_calculator import NutritionCalculator

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class FoodScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍎 Сканер продуктов питания")
        self.root.geometry("1200x900")
        self.root.minsize(1000, 700)
        self.root.configure(bg='#f5f5f5')

        # Установка иконки
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass

        # Инициализация компонентов
        self.load_model()
        self.db = ProductDatabase()
        self.image_processor = ImageProcessor()
        self.nutrition_calculator = NutritionCalculator()

        # Переменные состояния
        self.current_path = None
        self.photo = None
        self.current_prediction = None
        self.scan_history = []
        self.history_file = "scan_history.json"
        self.load_history()

        # Стиль
        self.setup_styles()

        # Интерфейс
        self.setup_ui()

    def setup_styles(self):
        """Настройка цветовой схемы и стилей"""
        self.colors = {
            'bg': '#f5f5f5',
            'primary': '#2e7d32',
            'primary_light': '#4caf50',
            'primary_dark': '#1b5e20',
            'accent': '#ff6f00',
            'accent_light': '#ffa726',
            'text': '#1a1a1a',
            'text_light': '#666666',
            'white': '#ffffff',
            'card': '#ffffff',
            'shadow': '#d0d0d0',
            'success': '#43a047',
            'warning': '#ff9800',
            'danger': '#e53935',
            'info': '#1e88e5'
        }

        # Шрифты
        self.fonts = {
            'title': ('Segoe UI', 24, 'bold'),
            'heading': ('Segoe UI', 16, 'bold'),
            'subheading': ('Segoe UI', 12, 'bold'),
            'body': ('Segoe UI', 10),
            'small': ('Segoe UI', 9),
            'mono': ('Consolas', 10)
        }

    def load_model(self):
        """Загрузка модели и классов"""
        model_path = "models/food_scanner_model.keras"
        classes_path = "food_classes.txt"

        try:
            if not os.path.exists(model_path):
                self.model_loaded = False
                self.class_names = []
                print(f"❌ Модель не найдена в {model_path}")
                return

            self.model = tf.keras.models.load_model(model_path)

            if os.path.exists(classes_path):
                with open(classes_path, "r", encoding="utf-8") as f:
                    self.class_names = [line.strip() for line in f]
                self.model_loaded = True
                print(f"✅ Модель загружена. Классов: {len(self.class_names)}")
            else:
                self.model_loaded = False
                self.class_names = []
                print(f"❌ Файл классов не найден: {classes_path}")

        except Exception as e:
            self.model = None
            self.class_names = []
            self.model_loaded = False
            print(f"❌ Ошибка загрузки модели: {e}")

    def setup_ui(self):
        """Создание интерфейса"""
        # Основной контейнер
        main_frame = tk.Frame(self.root, bg=self.colors['bg'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # ===== ВЕРХНЯЯ ПАНЕЛЬ =====
        header_frame = self.create_header(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))

        # ===== ПАНЕЛЬ КНОПОК =====
        btn_frame = self.create_button_panel(main_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 15))

        # ===== ОСНОВНАЯ ОБЛАСТЬ =====
        content_frame = tk.Frame(main_frame, bg=self.colors['bg'])
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Левая колонка - изображение
        left_frame = self.create_image_panel(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Правая колонка - результаты
        right_frame = self.create_results_panel(content_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        # ===== ПРОГРЕСС БАР =====
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400,
            style='green.Horizontal.TProgressbar'
        )

        # Статус бар
        self.status_bar = tk.Label(
            self.root,
            text="Готов к работе | Модель: " + ("✅ Загружена" if self.model_loaded else "❌ Не загружена"),
            bg=self.colors['primary_dark'],
            fg='white',
            font=self.fonts['small'],
            anchor='w',
            padx=15,
            pady=5
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # Показываем приветствие
        self.show_welcome()

    def create_header(self, parent):
        """Создание заголовка"""
        header = tk.Frame(parent, bg=self.colors['bg'])

        # Логотип и заголовок
        title_frame = tk.Frame(header, bg=self.colors['bg'])
        title_frame.pack(side=tk.LEFT)

        title = tk.Label(
            title_frame,
            text="🍎 Сканер продуктов питания",
            font=self.fonts['title'],
            bg=self.colors['bg'],
            fg=self.colors['primary_dark']
        )
        title.pack(anchor='w')

        subtitle = tk.Label(
            title_frame,
            text="Распознавание фруктов и овощей с помощью искусственного интеллекта",
            font=self.fonts['body'],
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        )
        subtitle.pack(anchor='w')

        # Статус модели
        status_frame = tk.Frame(header, bg=self.colors['bg'])
        status_frame.pack(side=tk.RIGHT)

        status_color = self.colors['success'] if self.model_loaded else self.colors['danger']
        status_text = "🟢" if self.model_loaded else "🔴"

        status_label = tk.Label(
            status_frame,
            text=f"{status_text} Модель {'готова' if self.model_loaded else 'не загружена'}",
            font=self.fonts['body'],
            bg=self.colors['bg'],
            fg=status_color
        )
        status_label.pack()

        if self.model_loaded:
            class_count = tk.Label(
                status_frame,
                text=f"Классов: {len(self.class_names)}",
                font=self.fonts['small'],
                bg=self.colors['bg'],
                fg=self.colors['text_light']
            )
            class_count.pack()

        return header

    def create_button_panel(self, parent):
        """Создание панели кнопок"""
        btn_frame = tk.Frame(parent, bg=self.colors['bg'])

        # Стиль кнопок
        btn_style = {
            'font': self.fonts['body'],
            'padx': 20,
            'pady': 10,
            'cursor': 'hand2',
            'relief': tk.FLAT,
            'bd': 0
        }

        # Кнопки
        buttons = [
            ("📷 Загрузить фото", self.load_image, self.colors['primary']),
            ("🔍 Сканировать", self.scan_product, self.colors['accent']),
            ("🗑️ Очистить", self.clear_all, self.colors['danger']),
            ("📜 История", self.show_history, self.colors['info']),
            ("📊 Сравнить", self.compare_products, self.colors['primary_light']),
            ("❓ Помощь", self.show_help, self.colors['text_light'])
        ]

        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                btn_frame,
                text=text,
                command=command,
                bg=color,
                fg='white',
                **btn_style
            )
            if i == 0:
                self.btn_load = btn
            elif i == 1:
                self.btn_scan = btn
                btn.config(state=tk.DISABLED)
            elif i == 2:
                self.btn_clear = btn
                btn.config(state=tk.DISABLED)
            btn.pack(side=tk.LEFT, padx=5)

        return btn_frame

    def create_image_panel(self, parent):
        """Создание панели изображения"""
        frame = tk.LabelFrame(
            parent,
            text=" 📷 Загруженный продукт ",
            font=self.fonts['heading'],
            bg=self.colors['white'],
            fg=self.colors['primary_dark'],
            relief=tk.RAISED,
            bd=2
        )
        frame.pack(fill=tk.BOTH, expand=True)

        self.image_label = tk.Label(
            frame,
            text="🖼️\n\nЗагрузите фотографию\nфрукта или овоща",
            bg='#fafafa',
            font=('Segoe UI', 14),
            fg='#999'
        )
        self.image_label.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Информация об изображении
        self.image_info = tk.Label(
            frame,
            text="",
            font=self.fonts['small'],
            bg='#fafafa',
            fg=self.colors['text_light']
        )
        self.image_info.pack(pady=(0, 10))

        return frame

    def create_results_panel(self, parent):
        """Создание панели результатов"""
        frame = tk.LabelFrame(
            parent,
            text=" 📊 Информация о продукте ",
            font=self.fonts['heading'],
            bg=self.colors['white'],
            fg=self.colors['primary_dark'],
            relief=tk.RAISED,
            bd=2
        )
        frame.pack(fill=tk.BOTH, expand=True)

        # Контейнер для текста с прокруткой
        text_container = tk.Frame(frame, bg=self.colors['white'])
        text_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Текстовое поле
        self.result_text = tk.Text(
            text_container,
            font=('Segoe UI', 10),
            wrap=tk.WORD,
            bg='#ffffff',
            fg=self.colors['text'],
            relief=tk.FLAT,
            bd=0,
            highlightthickness=0
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Скроллбар
        scrollbar = tk.Scrollbar(
            text_container,
            command=self.result_text.yview,
            bg=self.colors['bg']
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)

        # Настройка тегов для форматирования текста
        self.result_text.tag_configure('title', font=('Segoe UI', 14, 'bold'), foreground=self.colors['primary_dark'])
        self.result_text.tag_configure('heading', font=('Segoe UI', 12, 'bold'), foreground=self.colors['primary'])
        self.result_text.tag_configure('subheading', font=('Segoe UI', 11, 'bold'), foreground=self.colors['accent'])
        self.result_text.tag_configure('highlight', background='#e8f5e9', foreground=self.colors['primary_dark'])
        self.result_text.tag_configure('success', foreground=self.colors['success'])
        self.result_text.tag_configure('warning', foreground=self.colors['warning'])
        self.result_text.tag_configure('danger', foreground=self.colors['danger'])
        self.result_text.tag_configure('info', foreground=self.colors['info'])
        self.result_text.tag_configure('emoji', font=('Segoe UI', 14))
        self.result_text.tag_configure('code', font=('Consolas', 10), foreground=self.colors['primary_dark'])
        self.result_text.tag_configure('separator', foreground=self.colors['text_light'])

        return frame

    def show_welcome(self):
        """Показывает приветственное сообщение"""
        welcome_text = """
🍎 ДОБРО ПОЖАЛОВАТЬ В СКАНЕР ПРОДУКТОВ!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 КАК ЭТО РАБОТАЕТ:

1️⃣ Нажмите кнопку "Загрузить фото"
2️⃣ Выберите фотографию фрукта или овоща
3️⃣ Нажмите "Сканировать" для анализа

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 ЧТО ВЫ УЗНАЕТЕ:

• Название продукта и категорию
• Пищевую ценность (калории, БЖУ)
• Содержание витаминов и минералов
• Сезонность и происхождение
• Советы по хранению
• Идеи для рецептов
• Рекомендации по питанию

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 СОВЕТ: Снимайте продукт на контрастном фоне
при хорошем освещении для лучшего распознавания!

📱 Поддерживается: яблоки, бананы, апельсины,
помидоры, картофель, морковь, огурцы и другие.
"""
        self.result_text.insert(tk.END, welcome_text)

    def load_image(self):
        """Загрузка изображения"""
        path = filedialog.askopenfilename(
            title="Выберите фото продукта",
            filetypes=[
                ("Изображения", "*.jpg *.jpeg *.png *.bmp *.webp"),
                ("Все файлы", "*.*")
            ]
        )

        if path:
            try:
                self.current_path = path

                # Загружаем и отображаем изображение
                img = Image.open(path)

                # Показываем информацию об изображении
                size = img.size
                format_str = img.format if img.format else "Неизвестно"
                self.image_info.config(text=f"Размер: {size[0]}x{size[1]} | Формат: {format_str}")

                # Изменяем размер для отображения
                display_size = (400, 400)
                img_display = img.copy()
                img_display.thumbnail(display_size, Image.Resampling.LANCZOS)
                self.photo = ImageTk.PhotoImage(img_display)
                self.image_label.config(image=self.photo, text="")

                # Активируем кнопки
                self.btn_scan.config(state=tk.NORMAL)
                self.btn_clear.config(state=tk.NORMAL)

                # Очищаем результат
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "🔍 Нажмите 'Сканировать' для анализа продукта...")

                self.status_bar.config(text=f"✅ Изображение загружено: {os.path.basename(path)}")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{str(e)}")

    def scan_product(self):
        """Сканирование продукта"""
        if not self.model_loaded:
            messagebox.showerror(
                "Ошибка",
                "Модель не загружена!\n\nПожалуйста, сначала обучите модель:\npython training/train_food_scanner.py"
            )
            return

        if not self.current_path:
            messagebox.showwarning("Предупреждение", "Пожалуйста, сначала загрузите изображение")
            return

        try:
            # Показываем прогресс
            self.progress.pack(pady=10)
            self.progress.start()
            self.status_bar.config(text="🔄 Анализ изображения...")
            self.root.update()

            # Подготовка изображения
            img = Image.open(self.current_path)
            processed_img = self.image_processor.preprocess_image(img, (224, 224))

            # Предсказание
            predictions = self.model.predict(processed_img)
            predicted_class = np.argmax(predictions[0])
            confidence = predictions[0][predicted_class] * 100

            # Получаем топ-3 предсказания
            top_indices = np.argsort(predictions[0])[-3:][::-1]
            top_predictions = [
                (self.class_names[i], predictions[0][i] * 100)
                for i in top_indices
            ]

            # Получаем название продукта
            product_name = self.class_names[predicted_class]

            # Останавливаем прогресс
            self.progress.stop()
            self.progress.pack_forget()

            # Получаем информацию из базы
            product_info = self.db.get_product_info(product_name)

            # Сохраняем в историю
            self.add_to_history(product_info['name'], confidence)

            # Обновляем интерфейс
            self.image_info.config(
                text=f"✅ Распознано: {product_info['name']} | Уверенность: {confidence:.1f}%"
            )

            # Отображаем результат
            self.display_result(product_name, confidence, product_info, top_predictions)

            self.status_bar.config(text=f"✅ Сканирование завершено: {product_info['name']}")

        except Exception as e:
            self.progress.stop()
            self.progress.pack_forget()
            messagebox.showerror("Ошибка", f"Не удалось выполнить сканирование:\n{str(e)}")
            self.status_bar.config(text="❌ Ошибка при сканировании")

    def display_result(self, product_name, confidence, info, top_predictions):
        """Отображение результата сканирования"""
        self.result_text.delete(1.0, tk.END)

        # Заголовок
        emoji = info.get('emoji', '🍽️')
        name = info.get('name', product_name.replace('_', ' ').title())
        category = info.get('category', 'Продукт')

        self.result_text.insert(tk.END, f"{emoji}  {name.upper()}\n", 'title')
        self.result_text.insert(tk.END, f"Категория: {category}\n\n", 'subheading')

        # Уверенность
        confidence_color = 'success' if confidence > 80 else ('warning' if confidence > 60 else 'danger')
        self.result_text.insert(tk.END, "📊 ДОСТОВЕРНОСТЬ РАСПОЗНАВАНИЯ\n", 'heading')
        self.result_text.insert(tk.END, f"   {confidence:.1f}% - ", 'subheading')

        if confidence > 80:
            self.result_text.insert(tk.END, "Высокая уверенность ✅\n", 'success')
        elif confidence > 60:
            self.result_text.insert(tk.END, "Средняя уверенность ⚠️\n", 'warning')
        else:
            self.result_text.insert(tk.END, "Низкая уверенность ❌\n", 'danger')

        self.result_text.insert(tk.END, "\n" + "─"*50 + "\n", 'separator')

        # Топ-3 альтернативы
        self.result_text.insert(tk.END, "🔄 АЛЬТЕРНАТИВНЫЕ ВАРИАНТЫ:\n", 'heading')
        for i, (name_pred, conf) in enumerate(top_predictions[:3], 1):
            if conf < confidence:  # Показываем только альтернативы
                clean_name = name_pred.replace('_', ' ').title()
                self.result_text.insert(tk.END, f"   {i}. {clean_name} - {conf:.1f}%\n")

        self.result_text.insert(tk.END, "\n" + "─"*50 + "\n", 'separator')

        # Пищевая ценность
        self.result_text.insert(tk.END, "📊 ПИЩЕВАЯ ЦЕННОСТЬ (на 100г)\n", 'heading')

        nutrition = self.db.get_nutrition_facts(info)
        self.result_text.insert(tk.END, f"   🔥 Калории:      {nutrition['calories']} ккал\n")
        self.result_text.insert(tk.END, f"   💪 Белки:        {nutrition['protein']} г\n")
        self.result_text.insert(tk.END, f"   🍞 Углеводы:     {nutrition['carbs']} г\n")
        self.result_text.insert(tk.END, f"   🧈 Жиры:         {nutrition['fat']} г\n")
        self.result_text.insert(tk.END, f"   🌾 Клетчатка:    {nutrition['fiber']} г\n")
        if nutrition.get('sugar') and nutrition['sugar'] != 'N/A':
            self.result_text.insert(tk.END, f"   🍬 Сахар:        {nutrition['sugar']} г\n")

        self.result_text.insert(tk.END, "\n" + "─"*50 + "\n", 'separator')

        # Витамины и минералы
        vitamins = info.get('vitamins', [])
        minerals = info.get('minerals', [])

        if vitamins and vitamins != ['Информация отсутствует']:
            self.result_text.insert(tk.END, "💊 ВИТАМИНЫ\n", 'heading')
            self.result_text.insert(tk.END, f"   {', '.join(vitamins)}\n\n")

        if minerals and minerals != ['Информация отсутствует']:
            self.result_text.insert(tk.END, "🧪 МИНЕРАЛЫ\n", 'heading')
            self.result_text.insert(tk.END, f"   {', '.join(minerals)}\n\n")

        # Дополнительная информация
        self.result_text.insert(tk.END, "─"*50 + "\n", 'separator')

        self.result_text.insert(tk.END, "🌍 ПРОИСХОЖДЕНИЕ\n", 'heading')
        self.result_text.insert(tk.END, f"   {info.get('origin', 'Неизвестно')}\n\n")

        self.result_text.insert(tk.END, "📅 СЕЗОН\n", 'heading')
        self.result_text.insert(tk.END, f"   {info.get('season', 'Неизвестно')}\n\n")

        self.result_text.insert(tk.END, "📦 ХРАНЕНИЕ\n", 'heading')
        self.result_text.insert(tk.END, f"   {info.get('storage', 'Информация отсутствует')}\n\n")

        # Рецепты
        recipes = info.get('recipes', [])
        if recipes and recipes != ['Информация отсутствует']:
            self.result_text.insert(tk.END, "🍳 РЕЦЕПТЫ\n", 'heading')
            for recipe in recipes[:3]:
                self.result_text.insert(tk.END, f"   • {recipe}\n")
            if len(recipes) > 3:
                self.result_text.insert(tk.END, f"   ... и еще {len(recipes)-3} рецептов\n")
            self.result_text.insert(tk.END, "\n")

        # Советы по питанию
        tips = self.db.get_nutrition_tips(info)
        if tips:
            self.result_text.insert(tk.END, "💡 СОВЕТЫ ПО ПИТАНИЮ\n", 'heading')
            for tip in tips:
                self.result_text.insert(tk.END, f"   {tip}\n")
            self.result_text.insert(tk.END, "\n")

        # Интересные факты
        fact = info.get('interesting_facts', '')
        if fact:
            self.result_text.insert(tk.END, "✨ ИНТЕРЕСНЫЙ ФАКТ\n", 'heading')
            self.result_text.insert(tk.END, f"   {fact}\n\n")

        # Описание
        description = info.get('description', '')
        if description:
            self.result_text.insert(tk.END, "📝 ОПИСАНИЕ\n", 'heading')
            self.result_text.insert(tk.END, f"   {description}\n")

        self.result_text.insert(tk.END, "\n" + "─"*50 + "\n", 'separator')
        self.result_text.insert(tk.END, "🔬 Распознано с помощью ИИ", 'info')
        self.result_text.insert(tk.END, f"   {datetime.now().strftime('%d.%m.%Y %H:%M')}", 'small')

    def clear_all(self):
        """Очистка всех данных"""
        self.current_path = None
        self.current_prediction = None

        # Очищаем изображение
        self.image_label.config(
            image='',
            text="🖼️\n\nЗагрузите фотографию\nфрукта или овоща"
        )
        self.image_info.config(text="")

        # Отключаем кнопки
        self.btn_scan.config(state=tk.DISABLED)
        self.btn_clear.config(state=tk.DISABLED)

        # Очищаем результат
        self.result_text.delete(1.0, tk.END)
        self.show_welcome()

        self.status_bar.config(text="🗑️ Очищено")

    def add_to_history(self, product_name, confidence):
        """Добавляет запись в историю"""
        entry = {
            'product': product_name,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }
        self.scan_history.append(entry)
        self.save_history()

    def load_history(self):
        """Загружает историю из файла"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.scan_history = json.load(f)
        except:
            self.scan_history = []

    def save_history(self):
        """Сохраняет историю в файл"""
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.scan_history, f, ensure_ascii=False, indent=2)
        except:
            pass

    def show_history(self):
        """Показывает историю сканирований"""
        if not self.scan_history:
            messagebox.showinfo("История", "История сканирований пуста")
            return

        # Создаем окно истории
        history_window = tk.Toplevel(self.root)
        history_window.title("📜 История сканирований")
        history_window.geometry("600x500")
        history_window.configure(bg=self.colors['bg'])
        history_window.transient(self.root)
        history_window.grab_set()

        # Заголовок
        tk.Label(
            history_window,
            text="📜 История сканирований",
            font=self.fonts['heading'],
            bg=self.colors['bg'],
            fg=self.colors['primary_dark']
        ).pack(pady=15)

        # Статистика
        stats = f"Всего сканирований: {len(self.scan_history)}"
        tk.Label(
            history_window,
            text=stats,
            font=self.fonts['body'],
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        ).pack(pady=(0, 10))

        # Список
        list_frame = tk.Frame(history_window, bg=self.colors['bg'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        history_list = tk.Listbox(
            list_frame,
            font=('Consolas', 10),
            height=20,
            bg='white',
            selectmode=tk.SINGLE,
            yscrollcommand=scrollbar.set
        )
        history_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=history_list.yview)

        # Заполняем список (новые сверху)
        for entry in reversed(self.scan_history):
            product = entry['product']
            confidence = entry['confidence']
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime('%d.%m %H:%M')
            history_list.insert(tk.END, f"{product}  {confidence:.1f}%  [{timestamp}]")

        # Кнопки
        btn_frame = tk.Frame(history_window, bg=self.colors['bg'])
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="🗑️ Очистить историю",
            command=lambda: self.clear_history(history_window),
            bg=self.colors['danger'],
            fg='white',
            font=self.fonts['body'],
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="Закрыть",
            command=history_window.destroy,
            bg=self.colors['primary'],
            fg='white',
            font=self.fonts['body'],
            padx=15,
            pady=5,
            cursor='hand2'
        ).pack(side=tk.LEFT, padx=5)

    def clear_history(self, window):
        """Очищает историю"""
        if messagebox.askyesno("Подтверждение", "Удалить всю историю сканирований?"):
            self.scan_history = []
            self.save_history()
            window.destroy()
            self.show_history()

    def compare_products(self):
        """Сравнение продуктов"""
        if not self.scan_history:
            messagebox.showinfo("Сравнение", "Сначала выполните сканирование продуктов")
            return

        # Получаем последние 2 сканирования
        recent = self.scan_history[-2:] if len(self.scan_history) >= 2 else self.scan_history

        if len(recent) < 2:
            messagebox.showinfo("Сравнение", "Нужно как минимум 2 сканирования для сравнения")
            return

        # Получаем информацию о продуктах
        product1 = recent[0]
        product2 = recent[1]

        info1 = self.db.get_product_info(product1['product'])
        info2 = self.db.get_product_info(product2['product'])

        # Создаем окно сравнения
        compare_window = tk.Toplevel(self.root)
        compare_window.title("📊 Сравнение продуктов")
        compare_window.geometry("800x600")
        compare_window.configure(bg=self.colors['bg'])
        compare_window.transient(self.root)
        compare_window.grab_set()

        # Заголовок
        tk.Label(
            compare_window,
            text="📊 Сравнение продуктов",
            font=self.fonts['heading'],
            bg=self.colors['bg'],
            fg=self.colors['primary_dark']
        ).pack(pady=15)

        # Таблица сравнения
        table_frame = tk.Frame(compare_window, bg=self.colors['bg'])
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Создаем таблицу
        headers = ["Параметр", f"{info1['emoji']} {info1['name']}", f"{info2['emoji']} {info2['name']}"]
        params = [
            ("Калории", info1.get('calories', 'N/A'), info2.get('calories', 'N/A')),
            ("Белки", info1.get('protein', 'N/A'), info2.get('protein', 'N/A')),
            ("Углеводы", info1.get('carbs', 'N/A'), info2.get('carbs', 'N/A')),
            ("Жиры", info1.get('fat', 'N/A'), info2.get('fat', 'N/A')),
            ("Клетчатка", info1.get('fiber', 'N/A'), info2.get('fiber', 'N/A')),
            ("Сезон", info1.get('season', 'N/A'), info2.get('season', 'N/A')),
            ("Происхождение", info1.get('origin', 'N/A'), info2.get('origin', 'N/A'))
        ]

        # Стиль для заголовков таблицы
        header_style = {
            'font': ('Segoe UI', 11, 'bold'),
            'bg': self.colors['primary_dark'],
            'fg': 'white',
            'padx': 10,
            'pady': 5
        }

        cell_style = {
            'font': ('Segoe UI', 10),
            'bg': 'white',
            'padx': 10,
            'pady': 5,
            'anchor': 'w'
        }

        # Заголовки
        for i, header in enumerate(headers):
            tk.Label(
                table_frame,
                text=header,
                **header_style
            ).grid(row=0, column=i, sticky='ew', padx=1, pady=1)

        # Данные
        for row, (param, val1, val2) in enumerate(params, 1):
            tk.Label(table_frame, text=param, **cell_style).grid(row=row, column=0, sticky='ew', padx=1, pady=1)
            tk.Label(table_frame, text=str(val1), **cell_style).grid(row=row, column=1, sticky='ew', padx=1, pady=1)
            tk.Label(table_frame, text=str(val2), **cell_style).grid(row=row, column=2, sticky='ew', padx=1, pady=1)

        # Делаем столбцы растягиваемыми
        table_frame.columnconfigure(0, weight=1)
        table_frame.columnconfigure(1, weight=2)
        table_frame.columnconfigure(2, weight=2)

        # Рекомендация
        rec_frame = tk.Frame(compare_window, bg=self.colors['bg'])
        rec_frame.pack(fill=tk.X, padx=20, pady=10)

        # Сравнение калорий
        cal1 = info1.get('calories', 0)
        cal2 = info2.get('calories', 0)

        if cal1 != 'N/A' and cal2 != 'N/A' and cal1 != 0 and cal2 != 0:
            lower_cal = info1['name'] if cal1 < cal2 else info2['name']
            higher_cal = info2['name'] if cal1 < cal2 else info1['name']

            tk.Label(
                rec_frame,
                text=f"💡 {lower_cal} менее калорийный, чем {higher_cal}",
                font=self.fonts['body'],
                bg=self.colors['bg'],
                fg=self.colors['text']
            ).pack()

        # Кнопка закрыть
        tk.Button(
            compare_window,
            text="Закрыть",
            command=compare_window.destroy,
            bg=self.colors['primary'],
            fg='white',
            font=self.fonts['body'],
            padx=20,
            pady=5,
            cursor='hand2'
        ).pack(pady=15)

    def show_help(self):
        """Показывает помощь"""
        help_window = tk.Toplevel(self.root)
        help_window.title("❓ Помощь")
        help_window.geometry("600x500")
        help_window.configure(bg=self.colors['bg'])
        help_window.transient(self.root)
        help_window.grab_set()

        # Заголовок
        tk.Label(
            help_window,
            text="❓ Помощь",
            font=self.fonts['heading'],
            bg=self.colors['bg'],
            fg=self.colors['primary_dark']
        ).pack(pady=15)

        # Текст помощи
        help_text = """
📌 КАК ПОЛЬЗОВАТЬСЯ СКАНЕРОМ:

1. ЗАГРУЗИТЕ ФОТО
   • Нажмите "Загрузить фото"
   • Выберите изображение фрукта или овоща
   • Поддерживаются: JPG, PNG, BMP, WEBP

2. СКАНИРУЙТЕ
   • Нажмите "Сканировать"
   • Подождите несколько секунд
   • Получите полную информацию

3. ПОЛУЧИТЕ ИНФОРМАЦИЮ
   • Название и категория
   • Пищевая ценность (калории, БЖУ)
   • Витамины и минералы
   • Сезонность и происхождение
   • Советы по хранению
   • Рецепты
   • Советы по питанию

💡 ПОЛЕЗНЫЕ СОВЕТЫ:

• Фотографируйте продукт целиком
• Используйте контрастный фон
• Хорошее освещение улучшает результат
• Продукт должен занимать 70-80% кадра

🔧 ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ:

• История сканирований
• Сравнение продуктов
• Экспорт результатов

❓ ВОЗНИКЛИ ПРОБЛЕМЫ?

• Убедитесь, что модель загружена
• Проверьте правильность пути к датасету
• Перезапустите приложение
• Свяжитесь с разработчиком
"""

        text_widget = tk.Text(
            help_window,
            font=('Segoe UI', 10),
            wrap=tk.WORD,
            bg='white',
            fg=self.colors['text'],
            padx=15,
            pady=15
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)

        # Кнопка закрыть
        tk.Button(
            help_window,
            text="Закрыть",
            command=help_window.destroy,
            bg=self.colors['primary'],
            fg='white',
            font=self.fonts['body'],
            padx=20,
            pady=5,
            cursor='hand2'
        ).pack(pady=15)


def main():
    root = tk.Tk()
    app = FoodScannerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()