# from .models import Choice, Question, TestSet
from pathlib import Path
# from typing import Any,Dict,Optional
import json



def load_test_from_json(file_name):
  path = Path(file_name)


  if not path.exists():
    print(f"Файл {file_name} не найден...")
    return None


  else:
    try:
      with open(file_name,"r",encoding="utf-8") as f:
        data = json.load(f)
        return data


    except json.JSONDecodeError:
      print("Не валидный формат json")
      return None


    except Exception:
      print(f"Ошибка при чтении файла {file_name} произошла ошибка...")
      return None


data = load_test_from_json("tests_data/good_test.json")
def validate_test(data):
  errors = []
  if not "title" in data:
    errors.append("Ошибка нету блока title")

  title = data["title"]

  try:

    title_probel = title.strip()

    if len(title_probel) == 0:
      errors.append("Ошибка в title не может быть пустой строкой или состоять из пробелов")

  except AttributeError:
    if title != str(title):
      errors.append("Ошибка в title должнен быть строкой")


  if len(title) < 1 or len(title) > 120:
    errors.append("Ошибка в title не может быть больше 120 символов")

  try:

    description_strip = data["description"]

    if description_strip.strip() == "":
      errors.append("Проблема в description не может состоять из пробелов или быть пустым")

  except KeyError:
    if not "questions" in data:
      errors.append("Ошибка нету блока questions")
    if not "description" in data:
      errors.append("Ошибка нету блока description ")

  if len(data["questions"][0]["text"]) == 0:
    errors.append("Вопрос не может быть пустым")


  
  print(errors)
validate_test(data)
