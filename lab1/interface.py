from system_shell import SystemShell


def inner(user_action, choice):
	shell.set_value(user_action, choice)
	return shell.get_value("Действие")


def parsing(action):
	if action == "Насадить":
		print("Тебе нужно насадить наживку 🍤 на крючок!")
	elif action == "Перезабросить":
		print("Тебе нужно перезабросить удочку! 🌊")
	elif action == "Вытянуть":
		print("Тебе нужно вытянуть удочку! 🎣")
	elif action == "Ждать":
		print("Прояви терпение, тебе нужно немного подождать! ⏱")
	elif action == "Подкормить":
		print("Тебе нужно подкормить рыбу! 🐟")
	else:
		print("Я запутался 🤯")

class Interface:
	def __init__(self, index, true_ans, false_ans):
		self.index = index
		self.true_ans = {"yes", "yeah", "yep", "да", "1", "берег", "с берега"} | true_ans
		self.false_ans = {"no", "nope", "not", "нет", "не", "2", "лодка", "с лодки"} | false_ans
		self.history = []

	def bait(self):
		action = "НаживкаНасажена"
		print("Наживка 🍤 насажена?")
		print("1. Да")
		print("2. Нет")
		answer = input().lower()

		if answer in self.true_ans:
			answer = True
		elif answer in self.false_ans:
			answer = False
		else:
			while True:
				print("Я тебя не понял 🤯, введи \"да\" или \"нет\"")
				answer = input().lower()

				if answer in self.true_ans:
					answer = True
					break
				elif answer in self.false_ans:
					answer = False
					break
		return action, answer


	def fishing_place(self):
		action = "ТипРыбалки"
		print("Рыбачишь с берега 🌴 или с лодки 🛥?")
		print("1. Берег")
		print("2. Лодка")
		answer = input().lower()
		if answer in self.true_ans:
			answer = "Берег"
		elif answer in self.false_ans:
			answer = "Лодка"
			self.index += 1
		else:
			while True:
				print("Я тебя не понял 🤯, \"с бегера\" или \"с лодки\"")
				answer = input().lower()

				if answer in self.true_ans:
					answer = True
					break
				elif answer in self.false_ans:
					answer = False
					break
		return action, answer


	def distance(self):
		action = "ДальностьЗаброса"
		print("Какова дальность заброса ☄️? (в метрах)")
		answer = input()
		while not answer.isdigit():
			print("Я тебя не понял 🤯, положительное введи число")
			print("Циферками!")
			answer = input()
		answer = float(answer)
		return action, answer


	def fishing_time(self):
		action = "ВремяПодкормки"
		print("Сколько минут назад ты подкармливал рыбу? ⏱")
		answer = input()
		while not answer.isdigit():
			print("Я тебя не понял 🤯, положительное введи число")
			print("Циферками!")
			answer = input()
		answer = float(answer)
		return action, answer


	def fish_action(self):
		action = "Клюет"
		print("Клюет? 🐟")
		print("1. Да")
		print("2. Нет")
		answer = input().lower()
		if answer in self.true_ans:
			answer = True
		elif answer in self.false_ans:
			answer = False
		else:
			while True:
				print("Я тебя не понял 🤯, введи \"да\" или \"нет\"")
				answer = input().lower()

				if answer in self.true_ans:
					answer = True
					break
				elif answer in self.false_ans:
					answer = False
					break
		return action, answer


	def question(self, obj):
		function = [obj.bait, obj.fishing_place, obj.distance, obj.fishing_time, obj.fish_action]
		lst = function[self.index]()
		self.index += 1
		self.history.append(lst)
		return lst


	def additional_question(self):
		print()
		print("Интересно почему тебе нужно сделать именно так? 🤔")
		print("1. Да")
		print("2. Нет")
		answer = input().lower()
		while True:
			if answer in self.true_ans:
				print()
				print('Потому что:')
				n = 1
				for i in self.history:
					print('\t%i.' % n, end=' ')
					n += 1
					if i[0] == "НаживкаНасажена":
						if inner(i[0], i[1]) != 'Насадить':
							print('Ты насадил наживку. 😎')
						else:
							print('Ты пока не насадил наживку, думаю, самое время заняться этим сейчас. 💪')
					elif i[0] == "ТипРыбалки":
						fishingType = i[0]
						if inner(i[0], i[1]):
							print('Ты рыбачишь с берега. 🌴')
						else:
							print('Ты закинул удочку с лодки, красота. 🛥')
					elif i[0] == "ДальностьЗаброса":
						if inner(i[0], i[1]) != 'Перезабросить':
							if fishingType:
								print('Ты замечательно закинул наживку. С берега это сделать не так уж и просто. 👍')
							else:
								print('С лодки не обязательно далеко закидывать наживку. У тебя всё получилось. 🙂')
						else:
							print('Но ты закинул наживку слишком близко. 🌊 Попробуй метра на три от берега хотябы.')
					elif i[0] == "ВремяПодкормки":
						if inner(i[0], i[1]) != 'Подкормить':
							print('Рыба уже у твоей наживки и жадно пожирает подкормку. 🍤')
						else:
							print('Воможно, рыба уже всё съела и уплыла. 🐟 Посмотрим, клюёт или нет.')
					elif i[0] == "Клюет":
						if inner(i[0], i[1]) == 'Вытянуть':
							print('Клюёт, подсекай скорее! 🎣')
						else:
							for j in range(len(self.history)):
								if inner(self.history[j][0], self.history[j][1]) == 'Подкормить':
									break
							if inner(self.history[j][0], self.history[j][1]) == 'Подкормить':
								print('Не клюёт, потому что корм закончился. 🍤 Нужно подкинуть еще что-нибудь.')
							elif inner(self.history[j][0], self.history[j][1]) == 'Ждать':
								print('Пока не клюёт. Но ты всё сделал правильно 👍, остаётся только немного подождать. 🐟 Не отчаивайся, друг мой.')
				break
			elif answer in self.false_ans:
				print("Ну и ладно!")
				break
			else:
				while True:
					print("Я тебя не понял 🤯, введи \"да\" или \"нет\"")
					answer = input().lower()

					if answer in self.true_ans:
						break
					elif answer in self.false_ans:
						break
		print()


	def continue_fishing(self):
		while(True):
			self.history.clear()
			print("Хочешь еще порыбачить?")
			answer = input()
			if answer in self.true_ans:
				answer = True
				shell.clear_storage()
				print("Тогда начнем нашу рыбалку, мой юный падаван!")
				break
			elif answer in self.false_ans:
				answer = False
				shell.clear_storage()
				print("Жду тебя снова, мой юный падаван!")
				print("Да прибудет с тобой Сила! 💪")
				break
			else:
				print("Я не очень понял твой ответ. Введи \"да\" или \"нет\" 🤯")
		return answer

def q_and_a(interf):
	criteria = None
	while (criteria == None):
		user_action, choice = interf.question(interf)
		criteria = inner(user_action, choice)
	parsing(criteria)
	interf.additional_question()


def introduction():
	print("Hello 👋 there!")
	print("I'm general Obi-Wan Kenobi, and I gonna help you with fishing 🎣!")
	print("May the Force 💪 be with you!")
	print()


def this_is_there_the_fun_begins():
	introduction()
	fun = True
	while(fun):
		interf = Interface(0, set(), set())
		q_and_a(interf)
		fun = interf.continue_fishing()


if __name__ == '__main__':
	shell = SystemShell()
	shell.compile_file("fishing.max")
	this_is_there_the_fun_begins()
