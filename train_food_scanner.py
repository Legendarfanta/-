"""
🍎 ОБУЧЕНИЕ МОДЕЛИ - СКАНЕР ПРОДУКТОВ (ИСПРАВЛЕННАЯ ВЕРСИЯ)
"""

import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print("="*60)
print("🍎 ОБУЧЕНИЕ МОДЕЛИ - СКАНЕР ПРОДУКТОВ")
print("="*60)
print(f"TensorFlow версия: {tf.__version__}")

# ===== КОНФИГУРАЦИЯ =====
DATASET_PATH = "data/Fruits-360/Training"  # ← ПРЯМО К ПАПКЕ Training
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 20  # ← Увеличил для лучшего обучения

# Создаем папку models
os.makedirs("models", exist_ok=True)

# ===== ПРОВЕРКА ДАТАСЕТА =====
if not os.path.exists(DATASET_PATH):
    print(f"\n❌ Папка '{DATASET_PATH}' не найдена!")
    print("Создайте папку data/Fruits-360/Training/ с подпапками для каждого продукта")
    exit(1)

# Проверяем, есть ли подпапки
folders = [f for f in os.listdir(DATASET_PATH)
           if os.path.isdir(os.path.join(DATASET_PATH, f))]

if not folders:
    print(f"\n❌ В папке '{DATASET_PATH}' нет подпапок с изображениями!")
    print("Создайте папки для каждого продукта и добавьте туда картинки")
    exit(1)

print(f"\n📁 Найдено классов: {len(folders)}")
for i, f in enumerate(folders[:10]):
    # Проверяем количество файлов
    files = os.listdir(os.path.join(DATASET_PATH, f))
    print(f"   {i+1}. {f} - {len(files)} изображений")

# ===== ПОДГОТОВКА ДАННЫХ (усиленная аугментация) =====
print("\n📂 Загрузка изображений...")

train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    brightness_range=[0.8, 1.2],
    fill_mode='nearest',
    validation_split=0.2
)

val_datagen = ImageDataGenerator(
    rescale=1./255,
    validation_split=0.2
)

train_generator = train_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True  # ← ВАЖНО: перемешиваем
)

validation_generator = val_datagen.flow_from_directory(
    DATASET_PATH,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False
)

print(f"\n📊 Статистика:")
print(f"   - Классов: {train_generator.num_classes}")
print(f"   - Обучающих: {train_generator.samples}")
print(f"   - Валидационных: {validation_generator.samples}")

# ===== СОХРАНЯЕМ КЛАССЫ =====
class_names = list(train_generator.class_indices.keys())
with open("food_classes.txt", "w", encoding="utf-8") as f:
    for class_name in class_names:
        f.write(f"{class_name}\n")
print(f"\n✅ Названия классов сохранены в food_classes.txt")

# ===== СОЗДАНИЕ МОДЕЛИ =====
print("\n🏗️ Создание модели EfficientNetB0...")

base_model = EfficientNetB0(
    weights='imagenet',
    include_top=False,
    input_shape=(224, 224, 3)
)

# Размораживаем верхние слои для тонкой настройки
base_model.trainable = True
for layer in base_model.layers[:100]:
    layer.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dropout(0.3)(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.3)(x)
predictions = Dense(train_generator.num_classes, activation='softmax')(x)

model = Model(inputs=base_model.input, outputs=predictions)

model.compile(
    optimizer=Adam(learning_rate=0.0001),  # ← Меньшая скорость для тонкой настройки
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ===== CALLBACKS =====
callbacks = [
    EarlyStopping(
        monitor='val_accuracy',
        patience=5,
        restore_best_weights=True,
        verbose=1
    ),
    ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=3,
        min_lr=0.00001,
        verbose=1
    )
]

# ===== ОБУЧЕНИЕ =====
print("\n🚀 НАЧАЛО ОБУЧЕНИЯ...")
print("="*60)

history = model.fit(
    train_generator,
    validation_data=validation_generator,
    epochs=EPOCHS,
    callbacks=callbacks,
    verbose=1
)

# ===== РЕЗУЛЬТАТЫ =====
print("\n" + "="*60)
print("📊 РЕЗУЛЬТАТЫ ОБУЧЕНИЯ")
print("="*60)
print(f"✅ Точность на обучении:   {history.history['accuracy'][-1]:.2%}")
print(f"✅ Точность на валидации:  {history.history['val_accuracy'][-1]:.2%}")

# ===== СОХРАНЕНИЕ =====
model.save("models/food_scanner_model.keras")
print("\n✅ Модель сохранена в models/food_scanner_model.keras")

print("\n🎉 ОБУЧЕНИЕ ЗАВЕРШЕНО!")
print("\n🚀 Запустите приложение:")
print("   python food_scanner_gui.py")