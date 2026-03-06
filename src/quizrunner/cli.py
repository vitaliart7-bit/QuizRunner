from .services import load_test_from_json,validate_test,dict_to_testset
from .database import save_test,all_tests,get_test_by_id
import sys
import time
from colorama import Fore, Back, Style, init
def main():
  init(autoreset=True)


  if sys.argv[1] == "import":

    if len(sys.argv) < 3:
      print("Дано 2 аргуманта вместо 3")
      sys.exit("E:10")


    data = load_test_from_json(file_name=sys.argv[2])


    if data is None:
      sys.exit("E:10")

    errors = validate_test(data=data)



    if errors == []:
      new_data = dict_to_testset(data=data)
      test_id = save_test(test=new_data)

      test = all_tests()
      for tests in test:
        print(Style.BRIGHT+f"Тест: {data["title"]} Успешно импортирован!. ID: {tests[0]} Вопросов {len(new_data.questions)}")
        break

    elif errors != []:
      print(errors)
      sys.exit("E:10")

  elif sys.argv[1] == "show":
    try:
      id_show = sys.argv[2]
    except IndexError:
      sys.exit(Back.RED+"E:10")


    print(Back.YELLOW+Fore.BLACK+"Внимание включается режим наблюдателя!!!")
    print(Back.GREEN+Fore.BLACK+"Получаем test с помощи id")
    test = get_test_by_id(test_id=id_show)

    print(Back.GREEN+Fore.BLACK+"Получение test успешно!!!")


    print(Back.GREEN+Fore.BLACK+"Мы преоброзовали test в валидный режим чтение для человека!!!")

    input("Что бы продолжить нажмите Enter")
    print(f"Заголовок: {test.title}")
    print(f"Описание: {test.description}")

    for questions in test.questions:
      print(f"Вопрос {Fore.LIGHTYELLOW_EX+questions.text}")
      choices_list = []
      id_answer = 0


      for choices in questions.choices:
        print(f"{id_answer+1}.|{choices.text}")

        id_answer+=1

        choices_list.append(choices)

      input("Что бы продолжить нажмите Enter")

  elif sys.argv[1] == "list":

    test = all_tests()
    test = test[::-1]
    for tests in test:

      if tests[0] < 10:
        print(Style.BRIGHT+f"|ID {tests[0]} |-|TITLE|-|{tests[1]}|-|CREATED-AT|-|{tests[2]}|")
        time.sleep(0.1)

      else:
        print(Style.BRIGHT+f"|ID {tests[0]}|-|TITLE|-|{tests[1]}|-|CREATED-AT|-|{tests[2]}|")
        time.sleep(0.1)






  elif sys.argv[1] == "run":
    feedback = False
    limit_bool_questions = False
    try:
      if sys.argv[3] == "--instant-feedback":
          feedback = True


    except IndexError:
      pass


    try:
      if sys.argv[3] == "--limit":
        try:
          limit_id_questions = sys.argv[4]
          limit_questions = 0
          limit_bool_questions = True


        except IndexError:
          sys.exit("E:30")


    except IndexError:
      limit_id_questions = 0
      limit_questions = 0

    try:

      test = get_test_by_id(test_id=sys.argv[2])

      if test == None:
        print(f"Тест не найден")
        sys.exit("E:30")

    except IndexError:
      print("Вы не указали 3 аргумент")
      sys.exit("E:30")



    try:
      test_id = sys.argv[2]

      if not test_id.isdigit():
        test_id = int(test_id)

      total = len(test.questions)
      correct = 0
      ball = 0

      start = time.time()
      print(f"Заголовок: {test.title}")
      print(f"Описание: {test.description}")

      for questions in test.questions:
        print(f"Вопрос {Fore.LIGHTYELLOW_EX+questions.text}")
        choices_list = []
        id_answer = 0


        for choices in questions.choices:
          print(f"{id_answer+1}.|{choices.text}")

          id_answer+=1

          choices_list.append(choices)

        print(f"{id_answer+1}.|Пропустить")
        answer = input("Ваш ответ (номер): ")

        if answer.isdigit():
          answer = int(answer)
        if answer == 5:
          continue

        try:
          answer-=1
        except TypeError:
          print("Вы ввели неккоректное значение")
          continue

        try:

          answer_str = str(choices_list[answer])

        except IndexError:

          print("вы ввели неккоректное значение")
          continue



        calculation_answer = answer_str.count("True")

        if feedback:
          if calculation_answer == 1:
            print(Style.DIM+Fore.BLACK+Back.GREEN+"|=|Мы вас поздравляем, вы ответили правильно!|=|")
            correct+=1
            ball+=5


          else:
            print(Style.DIM+Fore.BLACK+Back.RED+"|=|Увы, вы ответили неправильно|=|")

        else:
          if calculation_answer == 1:
            correct+=1
            ball+=5

        if limit_bool_questions:
          limit_questions+=1
          if limit_questions == int(limit_id_questions):
            end = time.time()
            print(f"Процент правильных ответов: {int((correct/limit_questions)*100)}%")
            print(f"У вас {correct} правильных ответа и {len(total-correct)} неправильных ответа ")
            print(f"За {str(end-start)[:4]} секунд вы прошли тест")
            print(f"Вы заработали {ball} балов...")
            sys.exit()







    except KeyboardInterrupt:
      print("Прервано пользователем")
      sys.exit("E:10")
    end = time.time()
    print(f"Процент правильных ответов: {int((correct/total)*100)}%")
    print(f"У вас {correct} правильных ответа и {total-correct} неправильных ответа ")
    print(f"За {str(end-start)[:4]} секунд вы прошли тест")
    print(f"Вы заработали {ball} балов...")



  elif sys.argv[1] == "stats":
    print("stats в разработке")


  elif sys.argv[1] == "--help" or sys.argv[0] == "quiz":
    print("Допустимые команды\n" \
    ">>> quiz stats <TEST_ID>\n" \
    ">>> quiz import <PATH>\n" \
    ">>> quiz run <TEST_ID>\n" \
    ">>> quiz list\n" \
    ">>> quiz show <TEST_ID>")
    sys.exit()

  else:
    print("Для получение помощи введите --help")
    sys.exit("E:2")

if __name__ == "__main__":
  main()
