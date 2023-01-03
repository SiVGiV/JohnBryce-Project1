
class ConsoleMenu:
    """
    A console based menu manager.
    Initializes using a {'choice-name': func} dictionary.
    """
    def __init__(self, option_list: dict):
        """
        :param option_list: {'choice': func} dictionary of all options in the main menu.
        """
        self.__menu = {'exit': {'name': 'Exit this application', 'func': exit}}
        choice_counter = 1
        for choice, func in option_list.items():
            self.__menu[str(choice_counter)] = {'name': choice, 'func': func}
            choice_counter += 1

    def display_main(self, *args, **kwargs):
        """
        Prints main menu and waits for input.
        :return: None
        """
        print(" MAIN MENU ".center(50, '='))
        print("Type in your choice of the following: ")
        for ind in self.__menu.keys():
            print(f"{ind}: {self.__menu[ind]['name']}")
        choice = input("\nAwaiting input: ").lower()
        while choice not in self.__menu:
            choice = input("Input does not match any of the options. Try again: ")
        if choice != "exit":
            self.__menu[choice]['func'](*args, **kwargs)
            input("Press enter to go back to menu...")
        else:
            self.__menu[choice]['func']()

    @staticmethod
    def user_input(prompt_dict: dict):
        """
        Prompts a user with prompts and returns the input. if the prompt is a string does no checks,
        if prompt is a dict: {'result_key': {'prompt': prompt, 'test': func}} runs until func(input) is True.
        :param prompt_dict: {'result_key': 'prompt'} dictionary of all the required prompts and input patterns.
        :return: {'result_key': 'input'} dictionary
        """
        input_dict = {}
        for key, prompt in prompt_dict.items():
            if isinstance(prompt, str):
                input_dict[key] = input(prompt)
            elif callable(prompt['test']):
                temp_input = input(prompt['prompt'])
                while not prompt['test'](temp_input):
                    if 'tip' in prompt:
                        tip = f" ({prompt['tip']})"
                    else:
                        tip = ''
                    temp_input = input(f"Input does not meet requirements{tip}, try again: ")
                input_dict[key] = temp_input
            else:
                raise TypeError('Bad prompt type.')
        return input_dict
