"""
🖼️ ОБРАБОТКА ИЗОБРАЖЕНИЙ ДЛЯ СКАНЕРА ПРОДУКТОВ
Утилиты для предобработки и улучшения качества изображений
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2


class ImageProcessor:
    def __init__(self):
        self.target_size = (224, 224)

    def preprocess_image(self, image, target_size=None):
        """
        Подготавливает изображение для модели

        Args:
            image: PIL Image объект
            target_size: целевой размер (ширина, высота)

        Returns:
            numpy array: подготовленное изображение
        """
        if target_size is None:
            target_size = self.target_size

        # Конвертация в RGB
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Изменение размера
        image = image.resize(target_size, Image.Resampling.LANCZOS)

        # Преобразование в numpy array
        img_array = np.array(image)

        # Нормализация
        img_array = img_array / 255.0

        # Добавление batch dimension
        img_array = np.expand_dims(img_array, axis=0)

        return img_array

    def enhance_image(self, image, brightness=1.0, contrast=1.0, sharpness=1.0):
        """
        Улучшает качество изображения

        Args:
            image: PIL Image объект
            brightness: яркость (0.5-2.0)
            contrast: контраст (0.5-2.0)
            sharpness: резкость (0.5-2.0)

        Returns:
            PIL Image: улучшенное изображение
        """
        # Яркость
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)

        # Контраст
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)

        # Резкость
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(sharpness)

        return image

    def remove_background(self, image):
        """
        Удаляет фон изображения (упрощенная версия)

        Args:
            image: PIL Image объект

        Returns:
            PIL Image: изображение с удаленным фоном
        """
        # Конвертируем в OpenCV формат
        img_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        # Простое обнаружение краев
        gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)

        # Создаем маску
        kernel = np.ones((5, 5), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        edges = cv2.erode(edges, kernel, iterations=1)

        # Возвращаем оригинальное изображение
        return image

    def crop_center(self, image, crop_size=None):
        """
        Обрезает изображение по центру

        Args:
            image: PIL Image объект
            crop_size: размер обрезки (ширина, высота)

        Returns:
            PIL Image: обрезанное изображение
        """
        if crop_size is None:
            crop_size = self.target_size

        width, height = image.size
        crop_width, crop_height = crop_size

        left = (width - crop_width) // 2
        top = (height - crop_height) // 2
        right = left + crop_width
        bottom = top + crop_height

        return image.crop((left, top, right, bottom))

    def auto_rotate(self, image):
        """
        Автоматический поворот изображения

        Args:
            image: PIL Image объект

        Returns:
            PIL Image: повернутое изображение
        """
        try:
            exif = image._getexif()
            if exif:
                orientation = exif.get(274)
                if orientation == 3:
                    image = image.rotate(180, expand=True)
                elif orientation == 6:
                    image = image.rotate(270, expand=True)
                elif orientation == 8:
                    image = image.rotate(90, expand=True)
        except:
            pass

        return image

    def get_image_stats(self, image):
        """
        Получает статистику изображения

        Args:
            image: PIL Image объект

        Returns:
            dict: статистика изображения
        """
        # Конвертируем в numpy
        img_array = np.array(image)

        stats = {
            'width': image.width,
            'height': image.height,
            'format': image.format if image.format else 'Unknown',
            'mode': image.mode,
            'mean_r': float(np.mean(img_array[:, :, 0])) if image.mode == 'RGB' else 0,
            'mean_g': float(np.mean(img_array[:, :, 1])) if image.mode == 'RGB' else 0,
            'mean_b': float(np.mean(img_array[:, :, 2])) if image.mode == 'RGB' else 0,
            'std': float(np.std(img_array)),
            'min': float(np.min(img_array)),
            'max': float(np.max(img_array))
        }

        return stats

    def is_clear_image(self, image, threshold=50):
        """
        Проверяет качество изображения (четкость)

        Args:
            image: PIL Image объект
            threshold: порог четкости

        Returns:
            bool: True если изображение четкое
        """
        # Конвертируем в оттенки серого
        gray = image.convert('L')

        # Вычисляем градиент
        img_array = np.array(gray)
        dx = np.gradient(img_array, axis=0)
        dy = np.gradient(img_array, axis=1)

        # Вычисляем резкость
        sharpness = np.mean(np.sqrt(dx ** 2 + dy ** 2))

        return sharpness > threshold

    def resize_to_square(self, image, size=None):
        """
        Изменяет размер изображения до квадрата с сохранением пропорций

        Args:
            image: PIL Image объект
            size: размер стороны

        Returns:
            PIL Image: квадратное изображение
        """
        if size is None:
            size = max(self.target_size)

        width, height = image.size
        max_dim = max(width, height)

        # Создаем новое изображение с отступами
        new_image = Image.new('RGB', (max_dim, max_dim), (255, 255, 255))

        # Вставляем оригинальное изображение по центру
        x = (max_dim - width) // 2
        y = (max_dim - height) // 2
        new_image.paste(image, (x, y))

        # Изменяем размер
        new_image = new_image.resize((size, size), Image.Resampling.LANCZOS)

        return new_image