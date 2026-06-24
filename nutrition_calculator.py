"""
🧮 КАЛЬКУЛЯТОР ПИЩЕВОЙ ЦЕННОСТИ
Расчет и анализ пищевой ценности продуктов
"""

import math
from typing import Dict, List, Tuple


class NutritionCalculator:
    def __init__(self):
        self.daily_requirements = {
            'calories': 2000,
            'protein': 50,
            'carbs': 300,
            'fat': 70,
            'fiber': 25
        }

    def calculate_nutrition_score(self, nutrition: Dict) -> float:
        """
        Рассчитывает общую оценку пищевой ценности (0-100)

        Args:
            nutrition: словарь с пищевой ценностью

        Returns:
            float: оценка питательности
        """
        score = 0

        # Калории (низкая калорийность - хорошо для большинства продуктов)
        calories = nutrition.get('calories', 0)
        if calories != 'N/A' and calories > 0:
            if calories < 50:
                score += 20
            elif calories < 100:
                score += 15
            elif calories < 200:
                score += 10
            else:
                score += 5

        # Белки (высокое содержание - хорошо)
        protein = nutrition.get('protein', 0)
        if protein != 'N/A' and protein > 0:
            if protein > 3:
                score += 20
            elif protein > 1.5:
                score += 15
            else:
                score += 10

        # Клетчатка (высокое содержание - хорошо)
        fiber = nutrition.get('fiber', 0)
        if fiber != 'N/A' and fiber > 0:
            if fiber > 3:
                score += 20
            elif fiber > 1.5:
                score += 15
            else:
                score += 10

        # Углеводы (умеренное содержание - хорошо)
        carbs = nutrition.get('carbs', 0)
        if carbs != 'N/A' and carbs > 0:
            if carbs < 15:
                score += 20
            elif carbs < 30:
                score += 15
            else:
                score += 10

        # Жиры (низкое содержание - хорошо)
        fat = nutrition.get('fat', 0)
        if fat != 'N/A' and fat > 0:
            if fat < 1:
                score += 20
            elif fat < 3:
                score += 15
            else:
                score += 10

        return min(100, score)

    def get_nutrition_grade(self, nutrition_score: float) -> Tuple[str, str]:
        """
        Возвращает буквенную оценку и цвет

        Args:
            nutrition_score: оценка питательности (0-100)

        Returns:
            Tuple[str, str]: (буква, цвет)
        """
        if nutrition_score >= 80:
            return 'A', '#4caf50'  # Зеленый
        elif nutrition_score >= 60:
            return 'B', '#8bc34a'  # Светло-зеленый
        elif nutrition_score >= 40:
            return 'C', '#ffeb3b'  # Желтый
        elif nutrition_score >= 20:
            return 'D', '#ff9800'  # Оранжевый
        else:
            return 'E', '#f44336'  # Красный

    def calculate_daily_percentage(self, nutrition: Dict, weight: float = 100) -> Dict:
        """
        Рассчитывает процент от дневной нормы

        Args:
            nutrition: словарь с пищевой ценностью
            weight: вес порции в граммах

        Returns:
            Dict: проценты от дневной нормы
        """
        result = {}

        for key, daily_value in self.daily_requirements.items():
            value = nutrition.get(key, 0)
            if value != 'N/A' and value > 0:
                # Пересчет на указанный вес
                value_per_100 = value
                value_per_portion = value_per_100 * (weight / 100)

                # Расчет процента
                percentage = (value_per_portion / daily_value) * 100
                result[key] = min(100, percentage)
            else:
                result[key] = 0

        return result

    def get_serving_suggestion(self, nutrition: Dict) -> Dict:
        """
        Предлагает размер порции на основе пищевой ценности

        Args:
            nutrition: словарь с пищевой ценностью

        Returns:
            Dict: рекомендации по порции
        """
        calories = nutrition.get('calories', 0)

        if calories == 'N/A' or calories == 0:
            return {
                'serving_size': 100,
                'recommendation': 'Стандартная порция - 100г',
                'emoji': '⚖️'
            }

        # Расчет оптимального размера порции
        if calories < 30:
            serving = 200
            recommendation = 'Низкокалорийный продукт - можно есть больше'
            emoji = '✅'
        elif calories < 70:
            serving = 150
            recommendation = 'Умеренно калорийный - хороший перекус'
            emoji = '👍'
        elif calories < 120:
            serving = 100
            recommendation = 'Стандартная порция - 100г'
            emoji = '⚖️'
        else:
            serving = 70
            recommendation = 'Высококалорийный продукт - умерьте порцию'
            emoji = '⚠️'

        return {
            'serving_size': serving,
            'recommendation': recommendation,
            'emoji': emoji
        }

    def get_nutrition_summary(self, nutrition: Dict) -> str:
        """
        Возвращает краткую сводку по пищевой ценности

        Args:
            nutrition: словарь с пищевой ценностью

        Returns:
            str: текстовая сводка
        """
        calories = nutrition.get('calories', 0)
        protein = nutrition.get('protein', 0)
        carbs = nutrition.get('carbs', 0)
        fat = nutrition.get('fat', 0)
        fiber = nutrition.get('fiber', 0)

        # Анализ
        summary = []

        # Калории
        if calories != 'N/A' and calories > 0:
            if calories < 30:
                summary.append("низкокалорийный")
            elif calories < 70:
                summary.append("умеренно калорийный")
            else:
                summary.append("высококалорийный")

        # Белки
        if protein != 'N/A' and protein > 0:
            if protein > 3:
                summary.append("богат белком")

        # Клетчатка
        if fiber != 'N/A' and fiber > 0:
            if fiber > 2.5:
                summary.append("богат клетчаткой")

        # Углеводы
        if carbs != 'N/A' and carbs > 0:
            if carbs < 5:
                summary.append("низкоуглеводный")
            elif carbs > 15:
                summary.append("богат углеводами")

        # Жиры
        if fat != 'N/A' and fat > 0:
            if fat < 1:
                summary.append("с низким содержанием жиров")
            elif fat > 3:
                summary.append("с высоким содержанием жиров")

        if not summary:
            summary.append("продукт с неизвестной пищевой ценностью")

        return f"Продукт {', '.join(summary)}"

    def compare_nutrition(self, nutrition1: Dict, nutrition2: Dict) -> Dict:
        """
        Сравнивает пищевую ценность двух продуктов

        Args:
            nutrition1: словарь с пищевой ценностью первого продукта
            nutrition2: словарь с пищевой ценностью второго продукта

        Returns:
            Dict: результаты сравнения
        """
        comparison = {}

        keys = ['calories', 'protein', 'carbs', 'fat', 'fiber']
        labels = {
            'calories': 'Калории',
            'protein': 'Белки',
            'carbs': 'Углеводы',
            'fat': 'Жиры',
            'fiber': 'Клетчатка'
        }

        for key in keys:
            val1 = nutrition1.get(key, 0)
            val2 = nutrition2.get(key, 0)

            if val1 != 'N/A' and val2 != 'N/A' and val1 > 0 and val2 > 0:
                diff = val2 - val1
                percent = (diff / val1) * 100 if val1 > 0 else 0

                comparison[labels[key]] = {
                    'product1': val1,
                    'product2': val2,
                    'difference': diff,
                    'percent_diff': percent,
                    'higher': 'product1' if val1 > val2 else 'product2'
                }

        return comparison