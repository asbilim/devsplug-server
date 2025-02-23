from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from challenges.models import Category, Challenge, Attachment, Solution
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the database with 10 beginner-friendly challenges focused on programming fundamentals'

    def handle(self, *args, **options):
        self.stdout.write('Creating Programming Fundamentals challenges...')

        # Create or get the category
        category_data = {
            "name": "Programming Fundamentals",
            "description": "A series of challenges to help beginners learn the basics of programming.",
            "icon": "fa-code",
            "order": 1,
        }
        category, created = Category.objects.get_or_create(name=category_data['name'], defaults=category_data)
        if created:
            self.stdout.write(f"Created category: {category.name}")
        else:
            self.stdout.write(f"Category {category.name} already exists, skipping creation.")

        # Define 10 beginner-friendly challenges
        challenges_data = [
            {
                "title": "Hello, World!",
                "description": "Write a program that prints 'Hello, World!' to the console.",
                "content": (
                    "## Hello, World!\n\n"
                    "### Problem Statement\n"
                    "Write a program that prints 'Hello, World!' to the console.\n\n"
                    "### Description\n"
                    "This is your first step into programming! Printing output is a basic skill that lets you display messages to users. "
                    "Imagine sending a greeting card—your program will 'send' 'Hello, World!' to the screen.\n\n"
                    "### Hints\n"
                    "- In Python, you might use a function called `print`.\n"
                    "- Other languages have similar ways to show text—look for a 'print' or 'log' command.\n"
                    "- Keep it simple: one line can do the trick!\n"
                ),
                "difficulty": "easy",
                "points": 10,
                "estimated_time": 10,
                "attachments": [
                    {
                        "title": "Getting Started",
                        "content": (
                            "To start programming in Python:\n"
                            "1. Download Python from python.org.\n"
                            "2. Open a terminal or command prompt.\n"
                            "3. Create a file (e.g., 'hello.py').\n"
                            "4. Run it with 'python hello.py'.\n"
                            "You’re ready to see 'Hello, World!' on your screen!"
                        ),
                        "file_type": "text/plain",
                        "description": "Instructions to set up and run your first program."
                    }
                ],
                "solutions": [
                    {"user_id": 1, "code": 'print("Hello, World!")', "language": "Python", "status": "accepted"},
                    {"user_id": 1, "code": 'console.log("Hello, World!");', "language": "JavaScript", "status": "accepted"},
                    {"user_id": 1, "code": 'public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}', "language": "Java", "status": "accepted"}
                ]
            },
            {
                "title": "Simple Calculator",
                "description": "Write a program that takes two numbers as input and prints their sum, difference, product, and quotient.",
                "content": (
                    "## Simple Calculator\n\n"
                    "### Problem Statement\n"
                    "Write a program that takes two numbers as input and prints their sum, difference, product, and quotient.\n\n"
                    "### Description\n"
                    "Math is everywhere in programming! In this challenge, you’ll build a mini-calculator. You’ll ask the user for two numbers, "
                    "do some basic math (like adding or multiplying), and show the results. Think of it as helping a friend with quick calculations.\n\n"
                    "### Hints\n"
                    "- Use a way to get input from the user (e.g., `input()` in Python).\n"
                    "- Store the numbers in variables—think of them as little boxes holding values.\n"
                    "- Use symbols like `+`, `-`, `*`, and `/` for math.\n"
                    "- Watch out: dividing by zero doesn’t work, so plan for that!\n"
                ),
                "difficulty": "easy",
                "points": 15,
                "estimated_time": 20,
                "attachments": [
                    {
                        "title": "Math in Programming",
                        "content": (
                            "Here’s how math works in code:\n"
                            "- Addition: +\n"
                            "- Subtraction: -\n"
                            "- Multiplication: *\n"
                            "- Division: /\n"
                            "Example: If you have 5 and 2, their sum is 5 + 2 = 7.\n"
                            "Tip: Always check if a number is zero before dividing!"
                        ),
                        "file_type": "text/plain",
                        "description": "A guide to basic math operations."
                    }
                ],
                "solutions": [
                    {"user_id": 1, "code": 'num1 = float(input("Enter first number: "))\nnum2 = float(input("Enter second number: "))\nprint("Sum:", num1 + num2)\nprint("Difference:", num1 - num2)\nprint("Product:", num1 * num2)\nif num2 != 0:\n    print("Quotient:", num1 / num2)\nelse:\n    print("Cannot divide by zero")', "language": "Python", "status": "accepted"},
                    {"user_id": 1, "code": 'let num1 = parseFloat(prompt("Enter first number:"));\nlet num2 = parseFloat(prompt("Enter second number:"));\nconsole.log("Sum:", num1 + num2);\nconsole.log("Difference:", num1 - num2);\nconsole.log("Product:", num1 * num2);\nif (num2 !== 0) {\n    console.log("Quotient:", num1 / num2);\n} else {\n    console.log("Cannot divide by zero");\n}', "language": "JavaScript", "status": "accepted"}
                ]
            },
            {
                "title": "Variable Fun",
                "description": "Declare variables of different types (integer, float, string, boolean) and print their values.",
                "content": (
                    "## Variable Fun\n\n"
                    "### Problem Statement\n"
                    "Declare variables of different types (integer, float, string, boolean) and print their values.\n\n"
                    "### Description\n"
                    "Variables are like labeled boxes where you store information. In this challenge, you’ll create boxes for different kinds of data: "
                    "whole numbers (integers), decimals (floats), text (strings), and true/false values (booleans). Then, display what’s inside each box!\n\n"
                    "### Hints\n"
                    "- In Python, just name the variable and assign a value (e.g., `age = 10`).\n"
                    "- Try a number with a decimal, some text in quotes, and `True` or `False`.\n"
                    "- Print each one to see what’s stored.\n"
                ),
                "difficulty": "easy",
                "points": 15,
                "estimated_time": 15,
                "attachments": [
                    {
                        "title": "Data Types Explained",
                        "content": (
                            "Common data types:\n"
                            "- Integer: Whole numbers (e.g., 5, -3)\n"
                            "- Float: Decimal numbers (e.g., 3.14)\n"
                            "- String: Text (e.g., 'hello')\n"
                            "- Boolean: True or False\n"
                            "Variables hold these types so you can use them later!"
                        ),
                        "file_type": "text/plain",
                        "description": "A summary of variable types."
                    }
                ],
                "solutions": [
                    {"user_id": 1, "code": 'age = 25\nheight = 5.9\nname = "Alex"\nis_student = True\nprint(age)\nprint(height)\nprint(name)\nprint(is_student)', "language": "Python", "status": "accepted"}
                ]
            },
            # Add 7 more challenges here (e.g., Conditionals, Loops, Functions, Lists, Strings, Input/Output, Simple Algorithm)
            # Example for a more complex challenge:
            {
                "title": "Find the Maximum",
                "description": "Write a function that takes a list of numbers and returns the largest one.",
                "content": (
                    "## Find the Maximum\n\n"
                    "### Problem Statement\n"
                    "Write a function that takes a list of numbers and returns the largest one.\n\n"
                    "### Description\n"
                    "Imagine you’re searching a treasure chest for the biggest gem. In this challenge, you’ll create a function—a reusable tool—that looks through a list of numbers and finds the largest. This teaches you how to work with lists and compare values step-by-step.\n\n"
                    "### Hints\n"
                    "- Start by assuming the first number is the biggest.\n"
                    "- Check each number in the list one by one.\n"
                    "- If you find a bigger one, update your ‘biggest’ value.\n"
                    "- Here’s a starting point:\n"
                    "```python\n"
                    "def find_max(numbers):\n"
                    "    # Your code here\n"
                    "    pass\n"
                    "```\n"
                ),
                "difficulty": "medium",
                "points": 30,
                "estimated_time": 30,
                "attachments": [
                    {
                        "title": "How Lists Work",
                        "content": (
                            "A list is like a row of boxes, each holding a value.\n"
                            "Example: `[3, 5, 1, 9]` has 4 numbers.\n"
                            "You can loop through them to check each one.\n"
                            "Tip: Use a variable to track the largest number you’ve seen!"
                        ),
                        "file_type": "text/plain",
                        "description": "A guide to lists and finding the maximum."
                    }
                ],
                "solutions": [
                    {"user_id": 1, "code": 'def find_max(numbers):\n    max_num = numbers[0]\n    for num in numbers:\n        if num > max_num:\n            max_num = num\n    return max_num\nprint(find_max([3, 5, 1, 9]))', "language": "Python", "status": "accepted"}
                ]
            }
        ]

        
        # These 6 challenges complete the set of 10 when added to your existing 4
        challenge_data += [
            {
                "title": "Even or Odd",
                "description": "Write a program that takes an integer as input and prints whether it is even or odd.",
                "content": (
                    "## Even or Odd\n\n"
                    "### Problem Statement\n"
                    "Write a program that takes an integer as input and prints whether it is even or odd.\n\n"
                    "### Description\n"
                    "Numbers can be split into two teams: even and odd. Even numbers are like twins—they pair up perfectly (like 2, 4, 6), "
                    "while odd numbers stand alone (like 1, 3, 5). Your job is to build a program that checks which team a number belongs to!\n\n"
                    "### Hints\n"
                    "- Ask the user for a number using an input function.\n"
                    "- You can use the `%` symbol—it tells you what’s left after dividing (e.g., 5 % 2 leaves 1).\n"
                    "- If the remainder when divided by 2 is 0, it’s even. Otherwise, it’s odd.\n"
                ),
                "difficulty": "easy",
                "points": 15,
                "estimated_time": 15,
                "attachments": [
                    {
                        "title": "Conditionals Guide",
                        "content": (
                            "Conditionals let your program make decisions:\n"
                            "- Use 'if' to check something.\n"
                            "- Add 'else' for what happens if it’s not true.\n"
                            "Example: If a number divided by 2 has no remainder, it’s even!"
                        ),
                        "file_type": "text/plain",
                        "description": "A simple guide to if-else statements."
                    }
                ],
                "solutions": [
                    {
                        "user_id": 1,
                        "code": 'num = int(input("Enter a number: "))\nif num % 2 == 0:\n    print("Even")\nelse:\n    print("Odd")',
                        "language": "Python",
                        "status": "accepted"
                    }
                ]
            },
            {
                "title": "Sum of Numbers",
                "description": "Write a program that calculates the sum of all integers from 1 to N, where N is provided by the user.",
                "content": (
                    "## Sum of Numbers\n\n"
                    "### Problem Statement\n"
                    "Write a program that calculates the sum of all integers from 1 to N, where N is provided by the user.\n\n"
                    "### Description\n"
                    "Imagine stacking blocks from 1 up to a number you choose. If you pick 5, you’d add 1 + 2 + 3 + 4 + 5. "
                    "Your program will do this stacking for you, adding every number up to N and showing the total!\n\n"
                    "### Hints\n"
                    "- Get a number N from the user.\n"
                    "- You can use a loop to add each number from 1 to N, step by step.\n"
                    "- Start with a variable set to 0, then keep adding to it.\n"
                ),
                "difficulty": "easy",
                "points": 20,
                "estimated_time": 20,
                "attachments": [
                    {
                        "title": "Loops Explained",
                        "content": (
                            "Loops repeat actions:\n"
                            "- A 'for' loop can count from 1 to N.\n"
                            "Example: 'for i in range(1, 6)' counts 1, 2, 3, 4, 5.\n"
                            "- Add each number to a total as you go!"
                        ),
                        "file_type": "text/plain",
                        "description": "A beginner’s guide to loops."
                    }
                ],
                "solutions": [
                    {
                        "user_id": 1,
                        "code": 'n = int(input("Enter N: "))\ntotal = 0\nfor i in range(1, n + 1):\n    total += i\nprint("Sum:", total)',
                        "language": "Python",
                        "status": "accepted"
                    }
                ]
            },
            {
                "title": "Area Calculator",
                "description": "Write a function that takes the length and width of a rectangle and returns its area.",
                "content": (
                    "## Area Calculator\n\n"
                    "### Problem Statement\n"
                    "Write a function that takes the length and width of a rectangle and returns its area.\n\n"
                    "### Description\n"
                    "Think of a function as a little machine: you put in two numbers—length and width—and it gives you the area of a rectangle. "
                    "The area is just length times width, like counting squares in a grid. Build this machine to help someone measure space!\n\n"
                    "### Hints\n"
                    "- Start with `def` to make a function, and give it two names for the inputs.\n"
                    "- Multiply the two numbers with `*`.\n"
                    "- Use `return` to send the answer back.\n"
                    "- Here’s a start:\n"
                    "```python\n"
                    "def calculate_area(length, width):\n"
                    "    # Your code here\n"
                    "    pass\n"
                    "```\n"
                ),
                "difficulty": "easy",
                "points": 20,
                "estimated_time": 20,
                "attachments": [
                    {
                        "title": "Functions 101",
                        "content": (
                            "Functions are reusable tools:\n"
                            "- Define them with 'def name(inputs):'.\n"
                            "- Use 'return' to give back a result.\n"
                            "Example: A function can take 2 and 3, multiply them, and return 6."
                        ),
                        "file_type": "text/plain",
                        "description": "A guide to creating functions."
                    }
                ],
                "solutions": [
                    {
                        "user_id": 1,
                        "code": 'def calculate_area(length, width):\n    return length * width\nprint(calculate_area(5, 3))',
                        "language": "Python",
                        "status": "accepted"
                    }
                ]
            },
            {
                "title": "String Reverser",
                "description": "Write a program that takes a string as input and prints its reverse.",
                "content": (
                    "## String Reverser\n\n"
                    "### Problem Statement\n"
                    "Write a program that takes a string as input and prints its reverse.\n\n"
                    "### Description\n"
                    "Strings are like words or sentences in code. Imagine taking 'cat' and flipping it to 'tac'. Your program will be a mirror, "
                    "showing any text backward. This helps you learn how to work with letters and order in programming!\n\n"
                    "### Hints\n"
                    "- Get a string from the user with an input function.\n"
                    "- You could use a loop to build the reverse, one letter at a time.\n"
                    "- Or, look for a trick with slicing (like `[::-1]` in Python—but explore it yourself!).\n"
                ),
                "difficulty": "medium",
                "points": 25,
                "estimated_time": 25,
                "attachments": [
                    {
                        "title": "String Manipulation",
                        "content": (
                            "Strings are text in quotes:\n"
                            "- You can loop through each letter.\n"
                            "- Or use special tricks to flip them.\n"
                            "Example: 'hello'[0] gives 'h'—can you go backward?"
                        ),
                        "file_type": "text/plain",
                        "description": "Tips for working with strings."
                    }
                ],
                "solutions": [
                    {
                        "user_id": 1,
                        "code": 'text = input("Enter a string: ")\nreversed_text = text[::-1]\nprint(reversed_text)',
                        "language": "Python",
                        "status": "accepted"
                    }
                ]
            },
            {
                "title": "List Average",
                "description": "Write a program that calculates the average of a list of numbers.",
                "content": (
                    "## List Average\n\n"
                    "### Problem Statement\n"
                    "Write a program that calculates the average of a list of numbers.\n\n"
                    "### Description\n"
                    "A list is like a basket of numbers. To find the average, you add them all up and divide by how many there are—like finding "
                    "the middle ground of a group of friends’ heights. Your program will do this math for any list you give it!\n\n"
                    "### Hints\n"
                    "- Use a list like `[1, 2, 3, 4, 5]` to start.\n"
                    "- Add all numbers together (you can loop or use a sum function).\n"
                    "- Divide by the number of items (find the length of the list).\n"
                ),
                "difficulty": "medium",
                "points": 25,
                "estimated_time": 25,
                "attachments": [
                    {
                        "title": "Working with Lists",
                        "content": (
                            "Lists hold multiple values:\n"
                            "- Example: [1, 2, 3] has 3 numbers.\n"
                            "- Use 'len()' to count items.\n"
                            "- Add them with a loop or 'sum()'."
                        ),
                        "file_type": "text/plain",
                        "description": "A beginner’s guide to lists."
                    }
                ],
                "solutions": [
                    {
                        "user_id": 1,
                        "code": 'numbers = [1, 2, 3, 4, 5]\navg = sum(numbers) / len(numbers)\nprint("Average:", avg)',
                        "language": "Python",
                        "status": "accepted"
                    }
                ]
            },
            {
                "title": "Simple Guessing Game",
                "description": "Implement a game where the computer picks a random number between 1 and 100, and the user guesses it.",
                "content": (
                    "## Simple Guessing Game\n\n"
                    "### Problem Statement\n"
                    "Implement a game where the computer picks a random number between 1 and 100, and the user has to guess it.\n\n"
                    "### Description\n"
                    "Let’s play hide and seek with numbers! The computer hides a number, and you guess until you find it. After each guess, "
                    "it’ll tell you if you’re too high or too low. This mixes loops, decisions, and a bit of randomness into a fun challenge!\n\n"
                    "### Hints\n"
                    "- Use a random number generator (like `random.randint` in Python).\n"
                    "- Keep asking for guesses with a loop.\n"
                    "- Compare the guess to the number and give a hint:\n"
                    "  - Too high? Say so.\n"
                    "  - Too low? Say that instead.\n"
                    "  - Spot on? End the game!\n"
                ),
                "difficulty": "medium",
                "points": 30,
                "estimated_time": 30,
                "attachments": [
                    {
                        "title": "Random Numbers",
                        "content": (
                            "Randomness adds fun:\n"
                            "- In Python, 'import random' lets you use it.\n"
                            "- 'random.randint(1, 100)' picks a number from 1 to 100.\n"
                            "- Hide it and let the guessing begin!"
                        ),
                        "file_type": "text/plain",
                        "description": "How to use random numbers."
                    }
                ],
                "solutions": [
                    {
                        "user_id": 1,
                        "code": 'import random\nnumber = random.randint(1, 100)\nwhile True:\n    guess = int(input("Guess: "))\n    if guess == number:\n        print("Correct!")\n        break\n    elif guess < number:\n        print("Too low")\n    else:\n        print("Too high")',
                        "language": "Python",
                        "status": "accepted"
                    }
                ]
            }
        ]
        # Process each challenge
        for challenge_data in challenges_data:
            if Challenge.objects.filter(title=challenge_data["title"], category=category).exists():
                self.stdout.write(f"Challenge '{challenge_data['title']}' already exists, skipping.")
                continue

            challenge = Challenge.objects.create(
                title=challenge_data["title"],
                category=category,
                description=challenge_data["description"],
                content=challenge_data["content"],
                difficulty=challenge_data["difficulty"],
                points=challenge_data["points"],
                estimated_time=challenge_data["estimated_time"],
            )
            self.stdout.write(f"Created challenge: {challenge.title}")

            # Add attachments
            for attachment_data in challenge_data.get("attachments", []):
                file_name = f"{slugify(attachment_data['title'])}.txt"
                attachment = self.create_attachment(file_name, attachment_data["content"], attachment_data["file_type"], attachment_data["description"])
                challenge.attachments.add(attachment)

            # Add sample solutions
            for solution_data in challenge_data.get("solutions", []):
                Solution.objects.get_or_create(
                    user_id=solution_data["user_id"],
                    challenge=challenge,
                    language=solution_data["language"],
                    defaults={
                        "code": solution_data["code"],
                        "status": solution_data["status"]
                    }
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 10 programming fundamentals challenges'))

    def create_attachment(self, title, content, file_type, description):
        if Attachment.objects.filter(title=title).exists():
            self.stdout.write(f"Attachment '{title}' already exists, skipping.")
            return Attachment.objects.get(title=title)

        attachment = Attachment.objects.create(
            title=title,
            file_type=file_type,
            description=description
        )
        attachment.file.save(title, ContentFile(content.encode()))
        self.stdout.write(f"Created attachment: {title}")
        return attachment