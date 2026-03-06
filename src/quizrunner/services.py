from .models import Choice, Question, TestSet
from pathlib import Path
# from typing import Any,Dict,Optional
import json



def load_test_from_json(*,file_name):
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
      exit()
    except Exception:
      print(f"Ошибка при чтении файла {file_name} произошла ошибка...")
      exit()
data = load_test_from_json(file_name="tests_data/good_test.json")

def validate_test(data):
  errors = []

  if not "title" in data:
    errors.append("Ошибка, title[0] не существует!")


  else:

    data_title = data["title"]

    try:

      title_strip = data_title.strip()

      if len(title_strip) == 0:
        errors.append("Ошибка, title[0] не может быть пустым или состоять из пробелов!")


    except AttributeError:

      if type(data_title) != str(data_title):
        errors.append("Ошибка, title[0] должен быть типом string")


    if len(data_title) > 120:
      errors.append("Ошибка, title[0] не может быть больше 120 символов")


  try:

    data_description = data["description"]


    if len(data_description) > 500:
      errors.append("Ошибка, description[0] не может быть больше 500 символов")

    if type(data_description) != type(str(data_title)):
        errors.append("Ошибка, description[0] должен быть типом string")



  except KeyError:
    if not "description" in data:
      errors.append("Ошибка, description[0] не существует")




  # index = 0
  # index_2 = 0
  # try:
  #   for i in range(len(data["questions"])):


  #     print(data["questions"][index]["choices"][index_2]["is_correct"])
  #     print(len(data["questions"][index]["choices"]),'\n',data["questions"][index]["choices"][index_2])
  #     index +=1
  #     index_2+=1
  #     if index_2 == len(data["questions"][index]["choices"]):
  #       index_2=0
  # except IndexError:
  #   pass

  return errors

errors = validate_test(data=data)

def dict_to_testset(*,data):
  title = data["title"]
  description = data.get("description","")
  question_list = []


  for index, question_dict in enumerate(data["questions"]):
    choice_list = []
    for j, choice_dict in enumerate(question_dict["choices"]):
      choice = Choice(text=choice_dict["text"], is_correct=choice_dict["is_correct"])
      choice_list.append(choice)


    question = Question(text=question_dict["text"], choices=choice_list)
    question_list.append(question)


  test = TestSet(title=title, description=description, questions=question_list)
  return test

