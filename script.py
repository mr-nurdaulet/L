import os

# --------------- НАСТРОЙКИ ----------------
# 1. Путь до папки practice 2
practice_folder = "/Users/nurdaulet/Desktop/W3school/python/practice 2"

# 2. Названия тем
topics = [
    "Bolean Values",
    "Loops",
    "Booleans as Comparison Results",
    "Boolean Operators",
    "If Statement",
    "If Else",
    "If Elif Else",
    "Short Hand If Else",
    "While Loops",
    "While Loop Break",
    "While Loop Continue",
    "For Loops",
    "For Loop Continue",
    "For Loop Break"
]

# 3. Сколько файлов на тему
files_per_topic = 5

# 4. Сколько примеров в каждом файле
examples_per_file = 5
# ------------------------------------------

for topic in topics:
    topic_path = os.path.join(practice_folder, topic)
    os.makedirs(topic_path, exist_ok=True)

    for i in range(1, files_per_topic + 1):
        file_name = f"ex{i}.py"
        file_path = os.path.join(topic_path, file_name)

        with open(file_path, "w") as f:
            for j in range(1, examples_per_file + 1):
                f.write(f"# Example {j} for {file_name}\n")
                f.write(f"print('Example {j} from {file_name}')\n\n")

print("✅ Все файлы созданы и заполнены примерами!")
