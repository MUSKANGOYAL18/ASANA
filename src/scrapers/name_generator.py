"""Generate realistic user names based on US Census data."""
import random
from typing import Tuple
import logging

logger = logging.getLogger(__name__)

class NameGenerator:
    """Generate realistic names using census-based frequency data."""
    
    # Top 100 first names from US Census (2020)
    # Source: https://www.ssa.gov/oact/babynames/decades/century.html
    FIRST_NAMES_MALE = [
        "James", "Michael", "Robert", "John", "David", "William", "Richard", "Joseph",
        "Thomas", "Christopher", "Charles", "Daniel", "Matthew", "Anthony", "Mark",
        "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin", "Brian",
        "George", "Timothy", "Ronald", "Edward", "Jason", "Jeffrey", "Ryan", "Jacob",
        "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry", "Justin", "Scott",
        "Brandon", "Benjamin", "Samuel", "Raymond", "Gregory", "Frank", "Alexander",
        "Patrick", "Jack", "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Adam",
        "Nathan", "Henry", "Douglas", "Zachary", "Peter", "Kyle", "Noah", "Ethan",
        "Jeremy", "Walter", "Christian", "Keith", "Roger", "Terry", "Austin", "Sean",
        "Gerald", "Carl", "Harold", "Dylan", "Arthur", "Lawrence", "Jordan", "Jesse",
        "Bryan", "Billy", "Bruce", "Gabriel", "Joe", "Logan", "Alan", "Juan",
        "Albert", "Willie", "Elijah", "Randy", "Wayne", "Eugene", "Vincent", "Russell"
    ]
    
    FIRST_NAMES_FEMALE = [
        "Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan",
        "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Margaret", "Sandra",
        "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Carol", "Amanda", "Melissa",
        "Deborah", "Stephanie", "Dorothy", "Rebecca", "Sharon", "Laura", "Cynthia",
        "Amy", "Kathleen", "Angela", "Shirley", "Anna", "Brenda", "Pamela", "Emma",
        "Nicole", "Helen", "Samantha", "Katherine", "Christine", "Debra", "Rachel",
        "Carolyn", "Janet", "Catherine", "Maria", "Heather", "Diane", "Ruth", "Julie",
        "Olivia", "Joyce", "Virginia", "Victoria", "Kelly", "Lauren", "Christina",
        "Joan", "Evelyn", "Judith", "Megan", "Andrea", "Cheryl", "Hannah", "Jacqueline",
        "Martha", "Madison", "Teresa", "Gloria", "Sara", "Janice", "Jean", "Abigail",
        "Kathryn", "Alice", "Ann", "Doris", "Sophia", "Marie", "Isabella", "Alexis",
        "Grace", "Rose", "Theresa", "Judy", "Charlotte", "Beverly", "Denise", "Amber"
    ]
    
    # Top 100 last names from US Census (2010)
    # Source: https://www.census.gov/topics/population/genealogy/data/2010_surnames.html
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
        "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
        "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
        "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
        "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson", "Watson",
        "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza", "Ruiz",
        "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers", "Long"
    ]
    
    def __init__(self, seed: int = 42):
        self.rng = random.Random(seed)
        
    def generate_name(self) -> Tuple[str, str]:
        """Generate a random first and last name."""
        # 50/50 gender distribution
        if self.rng.random() < 0.5:
            first_name = self.rng.choice(self.FIRST_NAMES_MALE)
        else:
            first_name = self.rng.choice(self.FIRST_NAMES_FEMALE)
            
        last_name = self.rng.choice(self.LAST_NAMES)
        
        return first_name, last_name
        
    def generate_email(self, first_name: str, last_name: str, domain: str) -> str:
        """Generate email address from name."""
        # Common email patterns
        patterns = [
            f"{first_name.lower()}.{last_name.lower()}@{domain}",  # 70%
            f"{first_name[0].lower()}{last_name.lower()}@{domain}",  # 20%
            f"{first_name.lower()}{last_name[0].lower()}@{domain}",  # 10%
        ]
        
        weights = [0.7, 0.2, 0.1]
        return self.rng.choices(patterns, weights=weights)[0]