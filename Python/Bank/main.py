import datetime as _dt
import itertools as _it
from dataclasses import dataclass, field
from enum import Enum


# =============================== КОНСТАНТЫ ===============================
DEFAULT_CARD_INFO_FIELDS = [
    "card_id",
    "user_id",
    "phone",
    "bank_name",
    "bank_bic",
    "acc_id",
    "pan",
    "payment_system",
    "currency",
    "status",
    "issue_date",
    "expiry_date",
    "balance",
    "cashback_balance",
    "user_cards",
]
DEFAULT_ACCOUNT_BALANCE = 0.00
DEFAULT_CASHBACK_BALANCE = 0.00
CARD_CURRENCY = "RUB"
DEFAULT_PAYMENT_SYSTEM = "MIR"

ACCOUNT_TYPE_CODE = "40817"  # тип счета для физлиц
ACCOUNT_BRANCH = "0000"  # отсутствие филиалов у банка
ACCOUNT_CURRENCY = "810"  # идентификатор для рублёвых операций

EMPTY_PAN = "0000000000000000"

BIN_BY_SYSTEM = {
    "MIR": "220400",
    "VISA": "400000",
    "MASTERCARD": "510000",
}

# =============================== ГЕНЕРАТОРЫ ДАННЫХ ===============================
ISSUE_DATE_START = _dt.date(2022, 1, 1)
ISSUE_DATE_GENERATOR = (ISSUE_DATE_START + _dt.timedelta(days=i) for i in _it.count())
EXPIRY_YEARS = 4

# =============================== ENUM'Ы ===============================
class CardStatus(Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"
    BLOCKED = "Blocked"


CARD_STATUS = CardStatus.ACTIVE

# ============================== ОСНОВНЫЕ КЛАССЫ ===============================
@dataclass
class User:
    last_name: str
    first_name: str
    phone: str
    user_id: int

    accounts: list = field(default_factory=list)
    cards: list = field(default_factory=list)


@dataclass
class Account:
    owner: User
    account_number: str
    balance: float = DEFAULT_ACCOUNT_BALANCE


class Card:

    def __init__(self, card_id: int, payment_system: str, pan: str):
        self.card_id = card_id
        self.payment_system = payment_system
        self.pan = pan
        self.issue_date = next(ISSUE_DATE_GENERATOR)
        self.expiry_date = 


@dataclass
class Bank:
    name: str
    bic: str

    _user_id_seq: int = field(default_factory=lambda: _it.count(1), init=False)
    _account_number_seq: int = field(default_factory=lambda: _it.count(1), init=False)
    _cards_id_seq: int = field(default_factory=lambda: _it.count(1), init=False)
    _pan_seq: int = field(default_factory=lambda: _it.count(1), init=False)

    customers: dict = field(default_factory=dict, init=False)
    accounts: dict = field(default_factory=dict, init=False)
    cards: dict = field(default_factory=dict, init=False)

    def _next_account_number(self):
        prefix_left = ACCOUNT_TYPE_CODE + ACCOUNT_CURRENCY
        prefix_right = ACCOUNT_BRANCH
        bic_tail = self.bic[-3:]
        serial = f"{next(self._account_number_seq):07d}"

        for control_digit in range(10):
            candidate_account_number = prefix_left + str(control_digit) + prefix_right + serial
            digits = [int(d) for d in bic_tail + candidate_account_number]
            weights = [7, 1, 3] * 8
            weighted = [a * b for a, b in zip(digits, weights[:23])]
            control_sum = sum(x % 10 for x in weighted)
            if control_sum % 10 == 0:
                return candidate_account_number
    
    def _generate_pan(self, system):
        bin_code = BIN_BY_SYSTEM.get(system.upper(), BIN_BY_SYSTEM[DEFAULT_PAYMENT_SYSTEM])
        seq = f"{next(self._pan_seq):09d}"
        partial = bin_code + seq
        check = self._luhn(partial)
        return partial + str(check)

    def _luhn(self, number15):
        digits = [int(d) for d in number15[::-1]]
        for i in range(1, len(digits), 2):
            doubled = digits[i] * 2
            digits[i] = doubled - 9 if doubled > 9 else doubled
        return (10 - sum(digits) % 10) % 10

    def apply_for_card(self, last_name: str, first_name: str, phone: str, pin: str,  payment_system: str=DEFAULT_PAYMENT_SYSTEM) -> None:
        
        for id, user in self.customers.items():
            if (user.last_name, user.first_name, user.phone) == (last_name, first_name, phone):
                user_id = id
                break
        else:
            user_id = next(self._user_id_seq)
            self.customers[user_id] = User(last_name, first_name, phone, user_id)

        user = self.customers[user_id]
        new_account = Account(user, self._next_account_number())
        self.accounts[new_account.account_number] = new_account
        user.accounts.append(new_account)

        new_card = Card(next(self._cards_id_seq), payment_system, self._generate_pan(payment_system),
                        
                        
                        )



bank = Bank("Demo Bank", "044452345")
bank.apply_for_card('Kovalchuck', 'Artem', '8-800-555-35-35', '1234')
bank.apply_for_card('Titov', 'Vasiliy', '8-800-666-36-36', '1416')
bank.apply_for_card('Titov', 'Vasiliy', '8-800-666-36-36', '2416')

print(*bank.customers.values(), sep='\n')