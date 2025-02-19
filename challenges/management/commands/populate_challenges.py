from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from challenges.models import Category, Challenge, Attachment, Solution
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Populates the database with structured programming challenges, solutions, and attachments'

    def handle(self, *args, **options):
        self.stdout.write('Creating focused categories and challenges...')
        
        categories = [
            {"name": "Programming Basics", "description": "Master fundamental programming concepts", "icon": "fa-code", "order": 1},
            {"name": "Modular Programming", "description": "Learn to structure and organize code effectively", "icon": "fa-puzzle-piece", "order": 2},
            {"name": "Object-Oriented Programming", "description": "Understand and apply OOP principles", "icon": "fa-cubes", "order": 3},
        ]
        
        for category_data in categories:
            category, created = Category.objects.get_or_create(name=category_data['name'], defaults=category_data)
            self.create_challenges_for_category(category)
        
        self.stdout.write(self.style.SUCCESS('Successfully populated the database with structured programming challenges'))

    def create_challenges_for_category(self, category):
        challenge_templates = {
            "Programming Basics": [
                "Variables and Data Types",
                "Control Structures (if-else, loops)",
                "Functions and Scope",
                "Basic Input/Output Operations",
                "Error Handling and Debugging",
                "Working with Data Structures (Lists, Tuples, Dictionaries)",
                "String Manipulation and Formatting",
                "Recursion Fundamentals",
            ],
            "Modular Programming": [
                "Creating and Using Modules",
                "Understanding Imports and Namespaces",
                "Code Reusability and Refactoring",
                "Unit Testing and Test-Driven Development",
                "Managing Dependencies and Packages",
                "Writing and Using Configuration Files",
                "Creating Command-Line Tools",
                "Using Virtual Environments for Dependency Management",
            ],
            "Object-Oriented Programming": [
                "Introduction to OOP Concepts",
                "Classes and Objects",
                "Encapsulation and Data Hiding",
                "Inheritance and Polymorphism",
                "Design Patterns and Best Practices",
                "Abstract Classes and Interfaces",
                "Method Overloading and Overriding",
                "Static and Class Methods",
                "Building an OOP-Based Mini Project",
            ]
        }
        
        challenges = challenge_templates.get(category.name, [])
        for title in challenges:
            challenge, created = Challenge.objects.get_or_create(category=category, title=title, defaults={
                "description": f"Master {title} with hands-on practice",
                "content": f"## {title}\nLearn and complete tasks on {title}.",
                "difficulty": "easy" if "Basics" in category.name else "medium" if "Modular" in category.name else "hard",
                "points": random.randint(10, 50),
                "estimated_time": random.randint(20, 60)
            })
            
            # Attachments for challenges
            if category.name in ["Modular Programming", "Object-Oriented Programming"]:
                content = f"# Sample Code for {title}\n\ndef example():\n    pass"
                attachment = self.create_attachment(f"{slugify(title)}.py", content, "template", "Example script for challenge")
                challenge.attachments.add(attachment)
                
            # Generate sample solutions
            self.create_sample_solutions(challenge)

    def create_attachment(self, title, content, file_type, description):
        attachment, created = Attachment.objects.get_or_create(title=title, defaults={
            "file_type": file_type,
            "description": description
        })
        if created:
            attachment.file.save(title, ContentFile(content.encode()))
        return attachment
    
    def create_sample_solutions(self, challenge):
        sample_solutions = [
            {"user_id": 1, "code": "def solution():\n    return 'Hello World'", "language": "Python", "status": "accepted"},
            {"user_id": 3, "code": "function solution() { return 'Hello World'; }", "language": "JavaScript", "status": "pending"},
            {"user_id": 3, "code": "public class Solution { public String getSolution() { return 'Hello World'; } }", "language": "Java", "status": "rejected"},
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
