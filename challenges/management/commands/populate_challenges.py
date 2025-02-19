from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from challenges.models import Category, Challenge, Attachment, Solution
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Populates the database with 10 Euler-style challenges with structured content and hints'

    def handle(self, *args, **options):
        self.stdout.write('Creating Euler Problems challenges...')

        # Create a single category for Euler Problems
        category_data = {
            "name": "Euler Problems",
            "description": "A series of 10 Project Euler-style challenges designed to hone problem-solving and programming skills.",
            "icon": "fa-calculator",
            "order": 1,
        }
        category, _ = Category.objects.get_or_create(name=category_data['name'], defaults=category_data)

        # Define 10 Euler problems with structured content
        euler_challenges = [
            {
                "title": "Multiples of 3 and 5",
                "description": "Find the sum of all the multiples of 3 or 5 below 1000.",
                "content": (
                    "## Multiples of 3 and 5\n\n"
                    "### Problem Statement\n"
                    "Find the sum of all the multiples of 3 or 5 below 1000.\n\n"
                    "### Hints\n"
                    "- Use a loop or list comprehension to iterate through numbers.\n"
                    "- Consider checking divisibility by 3 or 5.\n"
                    "- You might use arithmetic progression for an optimized solution.\n\n"
                    "![Multiples Image](https://example.com/images/multiples.png)\n"
                ),
                "difficulty": "easy",
                "points": 10,
                "estimated_time": 20,
            },
            {
                "title": "Even Fibonacci Numbers",
                "description": "Calculate the sum of even Fibonacci numbers not exceeding four million.",
                "content": (
                    "## Even Fibonacci Numbers\n\n"
                    "### Problem Statement\n"
                    "Calculate the sum of all even-valued Fibonacci numbers below four million.\n\n"
                    "### Hints\n"
                    "- Generate the Fibonacci sequence iteratively.\n"
                    "- Filter the sequence to include only even numbers before summing.\n\n"
                    "![Fibonacci Image](https://example.com/images/fibonacci.png)\n"
                ),
                "difficulty": "easy",
                "points": 10,
                "estimated_time": 25,
            },
            {
                "title": "Largest Prime Factor",
                "description": "Determine the largest prime factor of the number 600851475143.",
                "content": (
                    "## Largest Prime Factor\n\n"
                    "### Problem Statement\n"
                    "Find the largest prime factor of 600851475143.\n\n"
                    "### Hints\n"
                    "- Use trial division, optimizing by only checking up to the square root.\n"
                    "- Consider dividing the number by found factors iteratively.\n\n"
                    "![Prime Factorization](https://example.com/images/prime_factor.png)\n"
                ),
                "difficulty": "medium",
                "points": 15,
                "estimated_time": 30,
            },
            {
                "title": "Largest Palindrome Product",
                "description": "Find the largest palindrome made from the product of two 3-digit numbers.",
                "content": (
                    "## Largest Palindrome Product\n\n"
                    "### Problem Statement\n"
                    "Identify the largest palindrome number that is the product of two 3-digit numbers.\n\n"
                    "### Hints\n"
                    "- A palindrome is a number that reads the same forwards and backwards.\n"
                    "- Consider iterating through potential factors in reverse order to find the largest product sooner.\n\n"
                    "![Palindrome](https://example.com/images/palindrome.png)\n"
                ),
                "difficulty": "medium",
                "points": 15,
                "estimated_time": 35,
            },
            {
                "title": "Smallest Multiple",
                "description": "Find the smallest positive number that is evenly divisible by all of the numbers from 1 to 20.",
                "content": (
                    "## Smallest Multiple\n\n"
                    "### Problem Statement\n"
                    "Determine the smallest positive number that is evenly divisible by all numbers from 1 to 20.\n\n"
                    "### Hints\n"
                    "- Think about using prime factorization to calculate the Least Common Multiple (LCM).\n"
                    "- Multiplying the highest powers of all prime factors in the range could be a strategy.\n\n"
                    "![LCM](https://example.com/images/lcm.png)\n"
                ),
                "difficulty": "medium",
                "points": 20,
                "estimated_time": 40,
            },
            {
                "title": "Sum Square Difference",
                "description": "Find the difference between the sum of the squares and the square of the sum of the first 100 natural numbers.",
                "content": (
                    "## Sum Square Difference\n\n"
                    "### Problem Statement\n"
                    "Compute the difference between the sum of the squares and the square of the sum of the first 100 natural numbers.\n\n"
                    "### Hints\n"
                    "- Use mathematical formulas for the sum of natural numbers and the sum of their squares.\n"
                    "- Both iterative and formula-based solutions can work here.\n\n"
                    "![Squares](https://example.com/images/squares.png)\n"
                ),
                "difficulty": "medium",
                "points": 20,
                "estimated_time": 30,
            },
            {
                "title": "10001st Prime",
                "description": "Find the 10001st prime number.",
                "content": (
                    "## 10001st Prime\n\n"
                    "### Problem Statement\n"
                    "Determine the 10001st prime number.\n\n"
                    "### Hints\n"
                    "- Implement a prime number generator, possibly using the Sieve of Eratosthenes.\n"
                    "- After 2, consider iterating only over odd numbers for efficiency.\n\n"
                    "![Primes](https://example.com/images/primes.png)\n"
                ),
                "difficulty": "hard",
                "points": 25,
                "estimated_time": 45,
            },
            {
                "title": "Largest Product in a Series",
                "description": "Find the largest product of thirteen consecutive digits in a 1000-digit number.",
                "content": (
                    "## Largest Product in a Series\n\n"
                    "### Problem Statement\n"
                    "Within a given 1000-digit number, find the thirteen adjacent digits that yield the greatest product.\n\n"
                    "### Hints\n"
                    "- Use a sliding window of 13 digits to calculate products.\n"
                    "- Handle cases with zeros carefully to avoid unnecessary calculations.\n\n"
                    "![Series](https://example.com/images/series.png)\n"
                ),
                "difficulty": "hard",
                "points": 25,
                "estimated_time": 50,
            },
            {
                "title": "Special Pythagorean Triplet",
                "description": "Find the product of the Pythagorean triplet for which a + b + c = 1000.",
                "content": (
                    "## Special Pythagorean Triplet\n\n"
                    "### Problem Statement\n"
                    "Identify the unique Pythagorean triplet (a, b, c) for which a + b + c = 1000, then find the product a * b * c.\n\n"
                    "### Hints\n"
                    "- Consider solving for one variable in terms of the others to reduce the search space.\n"
                    "- A brute-force search with some algebraic manipulation may be effective.\n\n"
                    "![Triplet](https://example.com/images/triplet.png)\n"
                ),
                "difficulty": "hard",
                "points": 30,
                "estimated_time": 50,
            },
            {
                "title": "Summation of Primes",
                "description": "Calculate the sum of all prime numbers below two million.",
                "content": (
                    "## Summation of Primes\n\n"
                    "### Problem Statement\n"
                    "Find the sum of all the prime numbers below two million.\n\n"
                    "### Hints\n"
                    "- Use an efficient algorithm like the Sieve of Eratosthenes to generate primes.\n"
                    "- Ensure your solution is optimized for performance with large datasets.\n\n"
                    "![Summation](https://example.com/images/summation.png)\n"
                ),
                "difficulty": "hard",
                "points": 30,
                "estimated_time": 55,
            },
        ]

        # Create challenges in the Euler Problems category
        for challenge_data in euler_challenges:
            challenge, created = Challenge.objects.get_or_create(
                title=challenge_data["title"],
                category=category,
                defaults={
                    "description": challenge_data["description"],
                    "content": challenge_data["content"],
                    "difficulty": challenge_data["difficulty"],
                    "points": challenge_data["points"],
                    "estimated_time": challenge_data["estimated_time"],
                }
            )

            # For medium and hard challenges, add an extra attachment with additional hints
            if created and challenge_data["difficulty"] in ["medium", "hard"]:
                file_name = f"{slugify(challenge_data['title'])}_hint.txt"
                attachment_content = (
                    f"Extra hints for {challenge_data['title']}:\n"
                    "1. Consider edge cases in your implementation.\n"
                    "2. Optimize your algorithm to run in reasonable time.\n"
                    "3. Check online resources for similar problem-solving techniques."
                )
                attachment = self.create_attachment(file_name, attachment_content, "hint", "Extra hints for the challenge")
                challenge.attachments.add(attachment)

            # Create sample solutions for the challenge
            self.create_sample_solutions(challenge)

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with 10 Euler challenges'))

    def create_attachment(self, title, content, file_type, description):
        attachment, created = Attachment.objects.get_or_create(
            title=title,
            defaults={
                "file_type": file_type,
                "description": description
            }
        )
        if created:
            attachment.file.save(title, ContentFile(content.encode()))
        return attachment

    def create_sample_solutions(self, challenge):
        # You can adjust or expand these sample solutions as needed.
        sample_solutions = [
            {"user_id": 1, "code": "def solution():\n    # Write your code here\n    pass", "language": "Python", "status": "accepted"},
            {"user_id": 1, "code": "function solution() {\n    // Write your code here\n}", "language": "JavaScript", "status": "pending"},
        ]
        for sol in sample_solutions:
            Solution.objects.get_or_create(
                user_id=sol["user_id"],
                challenge=challenge,
                defaults={
                    "code": sol["code"],
                    "language": sol["language"],
                    "status": sol["status"]
                }
            )
