from dataclasses import dataclass

@dataclass
class User:
    user_id: str
    emoji: str # Emoji shortcode such as :smirk:
    name: str
    balance: int
    is_admin: bool = False

@dataclass
class Transaction:
    owner_id: str
    amount: int
    description: str
    location: str | None # Optional
    is_approved: bool
    approved_id: str
    approved_at: int # Unix timestamp
    created_at: int # Unix timestamp

def get_users():
    return [
        User(user_id="alice5000", emoji=":smirk:", name="Alice", balance=7650)
    ]

def get_recent_transactions():
    # TODO Trim some fields to hide needless data, but realistically proper db will return via tailored SELECT
    return [
        (t.amount, t.description, t.location, t.is_approved, t.approved_id, t.approved_at, t.created_at)
        for t in get_transactions()
    ]

def get_transactions():
    return [
        Transaction("user_001", 2500, "Grocery shopping", "Walmart", True, "admin_001", 1791583472, 1791580921),
        Transaction("user_002", 1500, "Weekly allowance", None, True, "admin_001", 1791497238, 1791493564),
        Transaction("user_003", 450, "School supplies", "Staples", False, "", 0, 1791407159),
        Transaction("user_001", 800, "Lunch money", "School cafeteria", True, "admin_002", 1791320831, 1791316947),
        Transaction("user_004", 3200, "Birthday gift", None, True, "admin_001", 1791234386, 1791230672),
        Transaction("user_002", 1200, "Book purchase", "Bookstore", False, "", 0, 1791144379),
        Transaction("user_005", 500, "Chores", None, True, "admin_002", 1791057934, 1791054218),
        Transaction("user_003", 700, "Movie tickets", "Cinema", True, "admin_001", 1790971582, 1790967836),
        Transaction("user_001", 1800, "New shoes", "Shoe store", False, "", 0, 1790881571),
        Transaction("user_004", 600, "Ice cream", "Local ice cream shop", True, "admin_002", 1790795126, 1790791439),
        Transaction("user_005", 2000, "Monthly allowance", None, True, "admin_001", 1790708400, 1790704800),
        Transaction("user_002", 350, "Snacks", "Convenience store", False, "", 0, 1790622000),
        Transaction("user_003", 1100, "Art supplies", "Craft store", True, "admin_002", 1790535600, 1790532000),
        Transaction("user_001", 900, "Video game", "Game store", False, "", 0, 1790445600),
        Transaction("user_004", 400, "Household chores", None, True, "admin_001", 1790359200, 1790355600),
        Transaction("user_005", 750, "Pizza night", "Pizza restaurant", True, "admin_002", 1790272800, 1790269200),
        Transaction("user_002", 1300, "Sports equipment", "Sporting goods store", False, "", 0, 1790182800),
        Transaction("user_003", 500, "Pet sitting", None, True, "admin_001", 1790096400, 1790092800),
        Transaction("user_001", 650, "Breakfast", "Coffee shop", True, "admin_002", 1790010000, 1790006400),
        Transaction("user_004", 2200, "Winter jacket", "Clothing store", False, "", 0, 1789920000),
        Transaction("user_005", 1000, "Garden work", None, True, "admin_001", 1789833600, 1789830000),
        Transaction("user_002", 550, "Craft supplies", "Craft store", True, "admin_002", 1789747200, 1789743600),
        Transaction("user_003", 1400, "Board game", "Toy store", False, "", 0, 1789657200),
        Transaction("user_001", 300, "Lemonade stand", None, True, "admin_001", 1789570800, 1789567200),
        Transaction("user_004", 850, "Swimming pool", "Community center", True, "admin_002", 1789484400, 1789480800),
        Transaction("user_005", 1600, "Allowance", None, True, "admin_001", 1789398000, 1789394400),
        Transaction("user_002", 450, "Comic books", "Comic shop", False, "", 0, 1789308000),
        Transaction("user_003", 950, "Science project", "Hobby store", True, "admin_002", 1789221600, 1789218000),
        Transaction("user_001", 1200, "Backpack", "Department store", False, "", 0, 1789135200),
        Transaction("user_004", 400, "Car wash help", None, True, "admin_001", 1789048800, 1789045200),
        Transaction("user_005", 700, "Sandwich", "Deli", True, "admin_002", 1788958800, 1788955200),
        Transaction("user_002", 1800, "Concert ticket", "Ticket office", False, "", 0, 1788872400),
        Transaction("user_003", 600, "Dog walking", None, True, "admin_001", 1788786000, 1788782400),
        Transaction("user_001", 950, "Birthday card and gift", "Gift shop", True, "admin_002", 1788699600, 1788696000),
        Transaction("user_004", 300, "Candy", "Candy store", False, "", 0, 1788609600),
        Transaction("user_005", 1250, "Tutoring", None, True, "admin_001", 1788523200, 1788519600),
        Transaction("user_002", 800, "School trip", "School office", True, "admin_002", 1788436800, 1788433200),
        Transaction("user_003", 500, "Yard work", None, False, "", 0, 1788346800),
        Transaction("user_001", 2000, "Savings deposit", None, True, "admin_001", 1788260400, 1788256800),
        Transaction("user_004", 650, "Smoothie", "Smoothie shop", False, "", 0, 1788174000),
        Transaction("user_005", 900, "Helping neighbor", None, True, "admin_002", 1788087600, 1788084000),
        Transaction("user_002", 350, "Stationery", "Office supply store", True, "admin_001", 1787997600, 1787994000),
        Transaction("user_003", 1700, "New headphones", "Electronics store", False, "", 0, 1787911200),
        Transaction("user_001", 450, "Bike repair", "Bike shop", True, "admin_002", 1787824800, 1787821200),
        Transaction("user_004", 1000, "Pet care", "Pet store", False, "", 0, 1787738400),
        Transaction("user_005", 500, "Extra chores", None, True, "admin_001", 1787648400, 1787644800),
        Transaction("user_002", 750, "Lunch with friends", "Cafe", False, "", 0, 1787562000),
        Transaction("user_003", 1300, "School project materials", "Hardware store", True, "admin_002", 1787475600, 1787472000),
        Transaction("user_001", 600, "Weekend allowance", None, False, "", 0, 1787389200),
        Transaction("user_004", 400, "Book return refund", "Bookstore", True, "admin_001", 1787299200, 1787295600),
    ]

def get_current_user():
    return get_users()[0]

def calc_balance_delta():
    return 5 # TODO Determine our balance delta from the most recent 2 weeks