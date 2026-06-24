"""
🍎 БАЗА ДАННЫХ ПРОДУКТОВ ПИТАНИЯ
Содержит информацию о пищевой ценности, витаминах, рецептах и советах
"""

import json
from typing import Dict, List, Optional, Tuple


class ProductDatabase:
    def __init__(self):
        """Инициализация базы данных продуктов"""
        self.database = self.load_database()
        print(f"✅ Загружено {len(self.database)} продуктов в базу данных")

    def load_database(self) -> Dict:
        """Загружает базу данных продуктов с полной информацией"""

        database = {
            # ===== ФРУКТЫ =====
            "Apple": {
                "name": "Яблоко",
                "category": "Фрукт",
                "emoji": "🍎",
                "calories": 52,
                "protein": 0.3,
                "carbs": 14.0,
                "fat": 0.2,
                "fiber": 2.4,
                "sugar": 10.4,
                "vitamins": ["Витамин C", "Витамин A", "Витамин K", "Калий"],
                "minerals": ["Калий", "Магний", "Железо"],
                "season": "Сентябрь - Октябрь",
                "origin": "Центральная Азия",
                "storage": "Хранить в холодильнике до 2-3 недель",
                "recipes": [
                    "Шарлотка",
                    "Яблочный пирог",
                    "Свежевыжатый сок",
                    "Яблочный компот",
                    "Яблочный уксус"
                ],
                "benefits": "Укрепляет иммунитет, улучшает пищеварение, снижает холестерин",
                "description": "Один из самых популярных и полезных фруктов в мире",
                "interesting_facts": "В мире существует более 7500 сортов яблок"
            },

            "Banana": {
                "name": "Банан",
                "category": "Фрукт",
                "emoji": "🍌",
                "calories": 89,
                "protein": 1.1,
                "carbs": 23.0,
                "fat": 0.3,
                "fiber": 2.6,
                "sugar": 12.2,
                "vitamins": ["Витамин B6", "Витамин C", "Калий"],
                "minerals": ["Калий", "Магний", "Марганец"],
                "season": "Круглый год",
                "origin": "Юго-Восточная Азия",
                "storage": "Хранить при комнатной температуре",
                "recipes": [
                    "Банановый хлеб",
                    "Банановый смузи",
                    "Банановые панкейки",
                    "Шоколад с бананом",
                    "Банановое мороженое"
                ],
                "benefits": "Источник энергии, полезен для сердца, улучшает настроение",
                "description": "Богат калием и углеводами, отличный перекус",
                "interesting_facts": "Банан - это ягода, а не фрукт!"
            },

            "Orange": {
                "name": "Апельсин",
                "category": "Фрукт",
                "emoji": "🍊",
                "calories": 47,
                "protein": 0.9,
                "carbs": 12.0,
                "fat": 0.1,
                "fiber": 2.4,
                "sugar": 9.4,
                "vitamins": ["Витамин C", "Витамин A", "Витамин B1"],
                "minerals": ["Кальций", "Магний", "Калий"],
                "season": "Январь - Март",
                "origin": "Южный Китай",
                "storage": "Хранить в холодильнике до 2 недель",
                "recipes": [
                    "Свежевыжатый сок",
                    "Цукаты",
                    "Фруктовый салат",
                    "Апельсиновый джем",
                    "Апельсиновый кекс"
                ],
                "benefits": "Укрепляет иммунитет, антиоксидант, улучшает кожу",
                "description": "Отличный источник витамина C и антиоксидантов",
                "interesting_facts": "Апельсины - самый популярный цитрусовый в мире"
            },

            "Strawberry": {
                "name": "Клубника",
                "category": "Ягода",
                "emoji": "🍓",
                "calories": 32,
                "protein": 0.7,
                "carbs": 7.7,
                "fat": 0.3,
                "fiber": 2.0,
                "sugar": 4.9,
                "vitamins": ["Витамин C", "Витамин B9", "Витамин K"],
                "minerals": ["Марганец", "Калий", "Фосфор"],
                "season": "Июнь - Июль",
                "origin": "Европа",
                "storage": "Хранить в холодильнике до 3 дней",
                "recipes": [
                    "Клубничное варенье",
                    "Клубничный пирог",
                    "Клубничное мороженое",
                    "Клубничный смузи",
                    "Клубничный соус"
                ],
                "benefits": "Богата антиоксидантами, полезна для кожи, укрепляет сердце",
                "description": "Ароматная и полезная ягода, низкокалорийная",
                "interesting_facts": "Клубника - единственная ягода с семенами снаружи"
            },

            "Grape": {
                "name": "Виноград",
                "category": "Ягода",
                "emoji": "🍇",
                "calories": 69,
                "protein": 0.7,
                "carbs": 18.0,
                "fat": 0.2,
                "fiber": 0.9,
                "sugar": 15.5,
                "vitamins": ["Витамин C", "Витамин K", "Витамин B6"],
                "minerals": ["Калий", "Медь", "Железо"],
                "season": "Август - Сентябрь",
                "origin": "Кавказ, Средиземноморье",
                "storage": "Хранить в холодильнике до 1 недели",
                "recipes": [
                    "Виноградный сок",
                    "Изюм",
                    "Вино",
                    "Фруктовый салат",
                    "Смузи с виноградом"
                ],
                "benefits": "Улучшает работу сердца, антиоксидант, укрепляет кости",
                "description": "Богат антиоксидантами и полезными веществами",
                "interesting_facts": "Виноград - одна из древнейших культур в мире"
            },

            "Pear": {
                "name": "Груша",
                "category": "Фрукт",
                "emoji": "🍐",
                "calories": 57,
                "protein": 0.4,
                "carbs": 15.0,
                "fat": 0.1,
                "fiber": 3.1,
                "sugar": 9.8,
                "vitamins": ["Витамин C", "Витамин K", "Витамин B2"],
                "minerals": ["Калий", "Медь", "Железо"],
                "season": "Август - Сентябрь",
                "origin": "Восточная Азия",
                "storage": "Хранить в холодильнике до 1 недели",
                "recipes": [
                    "Грушевый пирог",
                    "Компот из груш",
                    "Груша в сиропе",
                    "Салат с грушей"
                ],
                "benefits": "Улучшает пищеварение, богата клетчаткой",
                "description": "Сочный и ароматный фрукт, богатый клетчаткой",
                "interesting_facts": "Груши не созревают на дереве, их нужно дозаривать"
            },

            # ===== ОВОЩИ =====
            "Tomato": {
                "name": "Помидор",
                "category": "Овощ",
                "emoji": "🍅",
                "calories": 18,
                "protein": 0.9,
                "carbs": 3.9,
                "fat": 0.2,
                "fiber": 1.2,
                "sugar": 2.6,
                "vitamins": ["Витамин C", "Витамин K", "Витамин A", "Ликопин"],
                "minerals": ["Калий", "Магний", "Фосфор"],
                "season": "Июль - Сентябрь",
                "origin": "Южная Америка",
                "storage": "Хранить при комнатной температуре",
                "recipes": [
                    "Салат из помидоров",
                    "Томатный суп",
                    "Томатный соус",
                    "Лечо",
                    "Помидоры фаршированные"
                ],
                "benefits": "Богат ликопином, полезен для зрения, укрепляет сердце",
                "description": "Популярный овощ, богатый витаминами и антиоксидантами",
                "interesting_facts": "Ботанически помидор - это ягода, а не овощ!"
            },

            "Potato": {
                "name": "Картофель",
                "category": "Овощ",
                "emoji": "🥔",
                "calories": 77,
                "protein": 2.0,
                "carbs": 17.0,
                "fat": 0.1,
                "fiber": 2.2,
                "sugar": 0.8,
                "vitamins": ["Витамин C", "Витамин B6", "Витамин B3"],
                "minerals": ["Калий", "Магний", "Железо"],
                "season": "Август - Октябрь",
                "origin": "Южная Америка",
                "storage": "Хранить в темном прохладном месте",
                "recipes": [
                    "Картофельное пюре",
                    "Жареный картофель",
                    "Запеченный картофель",
                    "Картофельный суп",
                    "Драники"
                ],
                "benefits": "Источник энергии, богат калием, полезен для нервной системы",
                "description": "Основной продукт питания во многих странах мира",
                "interesting_facts": "В мире существует более 5000 сортов картофеля"
            },

            "Carrot": {
                "name": "Морковь",
                "category": "Овощ",
                "emoji": "🥕",
                "calories": 41,
                "protein": 0.9,
                "carbs": 9.6,
                "fat": 0.2,
                "fiber": 2.8,
                "sugar": 4.7,
                "vitamins": ["Витамин A", "Витамин B1", "Витамин B2", "Витамин C"],
                "minerals": ["Калий", "Кальций", "Магний"],
                "season": "Круглый год",
                "origin": "Афганистан",
                "storage": "Хранить в холодильнике до 2 недель",
                "recipes": [
                    "Салат из моркови",
                    "Морковный сок",
                    "Морковный кекс",
                    "Морковь по-корейски",
                    "Морковный суп"
                ],
                "benefits": "Полезна для зрения, улучшает кожу, укрепляет иммунитет",
                "description": "Лидер по содержанию бета-каротина среди овощей",
                "interesting_facts": "Морковь была фиолетовой до 17 века!"
            },

            "Cucumber": {
                "name": "Огурец",
                "category": "Овощ",
                "emoji": "🥒",
                "calories": 15,
                "protein": 0.6,
                "carbs": 3.6,
                "fat": 0.1,
                "fiber": 0.5,
                "sugar": 1.7,
                "vitamins": ["Витамин K", "Витамин C", "Витамин B1"],
                "minerals": ["Калий", "Магний", "Кальций"],
                "season": "Июнь - Август",
                "origin": "Индия",
                "storage": "Хранить в холодильнике до 1 недели",
                "recipes": [
                    "Салат из огурцов",
                    "Окрошка",
                    "Маринованные огурцы",
                    "Холодный суп",
                    "Огуречный смузи"
                ],
                "benefits": "Увлажняет кожу, низкокалорийный, полезен для суставов",
                "description": "Очень низкокалорийный овощ, богат водой и витаминами",
                "interesting_facts": "Огурец состоит на 95% из воды"
            },

            "Pepper": {
                "name": "Перец болгарский",
                "category": "Овощ",
                "emoji": "🫑",
                "calories": 26,
                "protein": 1.0,
                "carbs": 6.0,
                "fat": 0.3,
                "fiber": 2.1,
                "sugar": 4.2,
                "vitamins": ["Витамин C", "Витамин A", "Витамин B6"],
                "minerals": ["Калий", "Магний", "Железо"],
                "season": "Июль - Сентябрь",
                "origin": "Центральная Америка",
                "storage": "Хранить в холодильнике до 1 недели",
                "recipes": [
                    "Салат с перцем",
                    "Фаршированный перец",
                    "Лечо",
                    "Перец гриль",
                    "Закуска из перца"
                ],
                "benefits": "Богат витамином С, улучшает зрение, укрепляет сосуды",
                "description": "Яркий и полезный овощ, рекордсмен по витамину С",
                "interesting_facts": "Красный перец содержит больше витамина С, чем цитрусовые!"
            },

            "Onion": {
                "name": "Лук репчатый",
                "category": "Овощ",
                "emoji": "🧅",
                "calories": 40,
                "protein": 1.1,
                "carbs": 9.3,
                "fat": 0.1,
                "fiber": 1.7,
                "sugar": 4.2,
                "vitamins": ["Витамин C", "Витамин B6", "Витамин B9"],
                "minerals": ["Калий", "Кальций", "Фосфор"],
                "season": "Круглый год",
                "origin": "Центральная Азия",
                "storage": "Хранить в сухом темном месте",
                "recipes": [
                    "Луковый суп",
                    "Жареный лук",
                    "Маринованный лук",
                    "Салаты",
                    "Соусы"
                ],
                "benefits": "Укрепляет иммунитет, антибактериальное действие",
                "description": "Незаменимый продукт в кулинарии, богат витаминами",
                "interesting_facts": "Лук - один из древнейших овощей в истории человечества"
            },

            # ===== САЛАТНЫЕ =====
            "Lettuce": {
                "name": "Салат листовой",
                "category": "Зелень",
                "emoji": "🥬",
                "calories": 15,
                "protein": 1.4,
                "carbs": 2.9,
                "fat": 0.2,
                "fiber": 1.3,
                "sugar": 0.8,
                "vitamins": ["Витамин A", "Витамин K", "Витамин C"],
                "minerals": ["Калий", "Кальций", "Железо"],
                "season": "Май - Октябрь",
                "origin": "Средиземноморье",
                "storage": "Хранить в холодильнике до 3 дней",
                "recipes": [
                    "Салат из зелени",
                    "Бургеры",
                    "Смузи",
                    "Сэндвичи"
                ],
                "benefits": "Богат витаминами, улучшает пищеварение",
                "description": "Низкокалорийная зелень, богатая витаминами",
                "interesting_facts": "Салат выращивали еще в Древнем Египте"
            }
        }

        return database

    def get_product_info(self, class_name: str) -> Dict:
        """
        Получает информацию о продукте по названию класса

        Args:
            class_name: Название класса из модели (например, 'Apple' или 'Tomato')

        Returns:
            Dict: Информация о продукте
        """
        # Очищаем название и ищем в базе
        clean_name = class_name.replace('_', ' ').strip().lower()

        # Прямой поиск
        for key, value in self.database.items():
            if key.lower() == class_name.lower():
                return value

        # Поиск по частичному совпадению
        for key, value in self.database.items():
            if key.lower() in clean_name or clean_name in key.lower():
                return value

        # Поиск по русскому названию
        for key, value in self.database.items():
            if value['name'].lower() in clean_name or clean_name in value['name'].lower():
                return value

        # Если не найдено - возвращаем информацию по умолчанию
        return self.get_default_info(class_name)

    def get_default_info(self, class_name: str) -> Dict:
        """Возвращает базовую информацию, если продукт не найден в базе"""
        return {
            "name": class_name.replace('_', ' ').title(),
            "category": "Продукт",
            "emoji": "🍽️",
            "calories": "N/A",
            "protein": "N/A",
            "carbs": "N/A",
            "fat": "N/A",
            "fiber": "N/A",
            "sugar": "N/A",
            "vitamins": ["Информация отсутствует"],
            "minerals": ["Информация отсутствует"],
            "season": "Неизвестно",
            "origin": "Неизвестно",
            "storage": "Информация отсутствует",
            "recipes": ["Информация отсутствует"],
            "benefits": "Информация отсутствует",
            "description": "Продукт не найден в базе данных",
            "interesting_facts": "Добавьте информацию в базу данных"
        }

    def get_nutrition_facts(self, product_info: Dict) -> Dict:
        """
        Получает структурированную информацию о пищевой ценности

        Returns:
            Dict: Структурированная информация
        """
        return {
            "calories": product_info.get('calories', 'N/A'),
            "protein": product_info.get('protein', 'N/A'),
            "carbs": product_info.get('carbs', 'N/A'),
            "fat": product_info.get('fat', 'N/A'),
            "fiber": product_info.get('fiber', 'N/A'),
            "sugar": product_info.get('sugar', 'N/A')
        }

    def get_nutrition_tips(self, product_info: Dict) -> List[str]:
        """
        Генерирует советы по питанию на основе пищевой ценности

        Returns:
            List[str]: Список советов
        """
        tips = []

        # Советы по калорийности
        calories = product_info.get('calories', 0)
        if calories != "N/A":
            if calories < 30:
                tips.append("✅ Низкокалорийный продукт - отлично подходит для диеты")
            elif calories < 70:
                tips.append("✅ Умеренно калорийный - хороший выбор для перекуса")
            elif calories < 120:
                tips.append("⚠️ Умеренно-высококалорийный - употребляйте в меру")
            else:
                tips.append("⚡ Высококалорийный продукт - ограничьте порцию")

        # Советы по клетчатке
        fiber = product_info.get('fiber', 0)
        if fiber != "N/A" and fiber > 2.5:
            tips.append("🌾 Богат клетчаткой - полезно для пищеварения")

        # Советы по белку
        protein = product_info.get('protein', 0)
        if protein != "N/A" and protein > 2.0:
            tips.append("💪 Хороший источник белка")

        # Советы по сахару
        sugar = product_info.get('sugar', 0)
        if sugar != "N/A" and sugar > 10:
            tips.append("⚠️ Высокое содержание сахара - не переусердствуйте")

        # Советы по витаминам
        vitamins = product_info.get('vitamins', [])
        if len(vitamins) > 2:
            tips.append(f"🌟 Богат витаминами: {', '.join(vitamins[:3])}")

        # Совет по сезонности
        season = product_info.get('season', '')
        if season and season != "Неизвестно" and season != "Круглый год":
            tips.append(f"📅 Сезонный продукт ({season}) - самый полезный")

        return tips

    def get_category_emoji(self, category: str) -> str:
        """Возвращает эмодзи для категории продукта"""
        category_emojis = {
            "Фрукт": "🍎",
            "Овощ": "🥕",
            "Ягода": "🫐",
            "Зелень": "🌿",
            "Цитрус": "🍊",
            "Корнеплод": "🥔"
        }
        return category_emojis.get(category, "🍽️")

    def search_products(self, query: str) -> List[Dict]:
        """
        Поиск продуктов по ключевому слову

        Args:
            query: Поисковый запрос

        Returns:
            List[Dict]: Список найденных продуктов
        """
        query = query.lower()
        results = []

        for key, value in self.database.items():
            if (query in key.lower() or
                    query in value['name'].lower() or
                    query in value['category'].lower()):
                results.append(value)

        return results