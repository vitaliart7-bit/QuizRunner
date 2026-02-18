from pathlib import Path
import json



def load_test_from_json(file_name):
  path = Path(file_name)


  if not path.exists():
    print(f"Файл {file_name} не найден...")
    return None


  else:
    try:
      with open(file_name,"r") as f:
        data = json.load(f)
        return data


    except json.JSONDecodeError:
      print("Не валидный формат json")
      return None


    except Exception:
      print(f"Ошибка при чтении файла {file_name} произошла ошибка...")
      return None


data = load_test_from_json("tests_data/good_test.json")
print(data)
