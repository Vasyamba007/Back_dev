import datetime as _dt
import itertools as _it
from dataclasses import dataclass, field
from enum import Enum
import re
from functools import wraps

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

TRANSACTION_HISTORY_HEADER = [
    "timestamp,type,from_card,to_card,amount,mcc,cashback,description"
]
DEFAULT_CASHBACK_TRANSACTION = 0.00
DEPOSIT_DESCRIPTION = "{amount:.2f}₽ → карта #{card_id}"
TRANSFER_DESCRIPTION = "{amount:.2f}₽: карта #{from_card} → карта #{to_card}"
PAY_DESCRIPTION = "{amount:.2f}₽ (MCC: {mcc}) с карты #{card_id}"
BALANCE_DESCRIPTION = "Баланс: {balance:.2f}₽"
CB_DEBIT_PAY_DESCRIPTION = "{amount:.2f}₽ (MCC: {mcc}) с карты #{card_id} (кешбэк {cashback_amount:.2f}₽)"
SAVING_INTEREST_DESCRIPTION = "Начислены проценты {interest:.2f}₽ по накопительной карте #{card_id}"

DEBIT_DEFAULT_CASHBACK_RATE = 0.03 
SAVING_CARD_DEFAULT_INTEREST = 0.015

DEPOSIT_LIMIT = 1000000.00
TRANSFER_LIMIT = 500000.00
PAY_LIMIT = 500000.00
MAX_CASHBACK_RATE = 0.10  # 10%
MAX_SAVING_INTEREST_RATE = 0.3

FORBIDDEN_MCC = {"7995", "4829", "6051"}

RUSSIAN_PATTERN = r'^[А-ЯЁа-яё]+?(\-[А-ЯЁа-яё]+)?$' 

# =============================== ГЕНЕРАТОРЫ ДАННЫХ ===============================
ISSUE_DATE_START = _dt.date(2022, 1, 1)
ISSUE_DATE_GENERATOR = (ISSUE_DATE_START + _dt.timedelta(days=i) for i in _it.count())
EXPIRY_YEARS = 4

TIMESTAMP_START = _dt.datetime(2022, 1, 1, 9, 0, 0)


def timestamp_generator():
    for i in _it.count():
        base_date = TIMESTAMP_START + _dt.timedelta(days=i)
        hour = 9 + (i * 3) % 10        # цикличное смещение часа
        minute = (i * 7) % 60          # цикличное смещение минут
        second = (i * 11) % 60         # цикличное смещение секунд
        yield base_date.replace(hour=hour % 24, minute=minute, second=second)


TIMESTAMP_GENERATOR = timestamp_generator()


def next_timestamp_after(issue_date: _dt.date) -> _dt.datetime:
    """
    Возвращает ближайший timestamp из генератора, который позже issue_date.
    """
    while True:
        ts = next(TIMESTAMP_GENERATOR)
        if ts.date() > issue_date:
            return ts
        

# =============================== ENUM'Ы ===============================
class CardStatus(Enum):
    ACTIVE = "Active"
    CLOSED = "Closed"
    BLOCKED = "Blocked"


CARD_STATUS = CardStatus.ACTIVE


class TransactionType(Enum):
    DEPOSIT = "deposit"
    TRANSFER = "transfer"
    PAY = "pay"
    INTEREST = "interest"


# ======================= КАТАЛОГ СООБЩЕНИЙ ОБ ОШИБКАХ =======================
class BankError(Exception):
    """Базовый класс для всех ошибок банковского приложения."""


class ValidationError(BankError):
    """Ошибка валидации пользовательских данных (форматы, обязательные поля, допустимые значения)."""

    PIN_MISMATCH = "Введенный ПИН-код не соответствует текущему"
    PIN_INVALID = "ПИН-код должен быть строкой из 4 символов"
    PIN_FORMAT_INVALID = "ПИН-код должен состоять только из цифр"
    NAME_INVALID = "Имя и фамилия должны быть на русском, без использования специальных символов"
    AMOUNT_NEGATIVE = "Сумма должна быть положительной"
    DEPOSIT_AMOUNT_NEGATIVE = "Сумма пополнений должна быть положительной"
    CASHBACK_NEGATIVE = "Процент кешбэка на покупки должен быть положительным"
    INTEREST_NEGATIVE = "Ставка по счету должна быть положительной"
    PAY_AMOUNT_NEGATIVE = "Сумма покупки должна быть положительной"
    INVALID_MCC = "Неверный код категории продавца (MCC)"
    PAYMENT_SYSTEM_NOT_SUPPORTED = "Платежная система {payment_system} не поддерживается банком"


class NotFoundError(BankError):
    """Ошибка отсутствия объекта: карта, счёт, пользователь не найдены."""

    RECIPIENT_NOT_FOUND = "Ошибка номером карты. Такой карты не существует."


class AccessError(BankError):
    """Ошибка доступа к объекту или операции: карта/счёт не активны, недоступны или не привязаны."""

    CARD_CLOSED = "Карта закрыта или заблокирована. Невозможно провести операцию."
    ACCOUNT_NOT_LINKED = "Карта не привязана к счёту"
    BANK_NOT_LINKED = "Карта не привязана к банку"
    RECIPIENT_ACCOUNT_NOT_LINKED = "Карта получателя не привязана к счёту"
    RECIPIENT_CARD_CLOSED = "Карта получателя закрыта или заблокирована. Невозможно провести операцию."


class BusinessRuleError(BankError):
    """Ошибка бизнес-логики: нарушено ограничение по правилам банка
    (лимиты, количество, уникальность, запрещённые операции)."""

    DEPOSIT_LIMIT_EXCEEDED = "Превышен лимит депозита. Карта заблокирована до выяснения причин."
    TRANSFER_LIMIT_EXCEEDED = "Подозрение на мошенническую операцию. Карта заблокирована до выяснения причин."
    CASHBACK_LIMIT = "Процент кешбэка завышен, возможна техническая ошибка. Карта заблокирована до выяснения причин."
    TRANSFER_TO_SELF = "Нельзя пересылать деньги самому себе"
    USER_CONFLICT = "Пользователь с таким телефоном уже зарегистрирован"
    TOO_MANY_DEBIT_CARDS = "У пользователя уже есть пять дебетовых карт"
    MCC_FORBIDDEN = "Оплата отклонена. Покупки по {mcc} запрещены банком"
    PURCHASE_LIMIT_EXCEEDED = "Сумма оплаты превышает лимит. Операция заблокирована до выяснения причин."
    PAYMENT_NOT_ALLOWED_FOR_SAVING = "С накопительного счёта нельзя списывать покупки"
    SAVING_RATE_TOO_HIGH = (
        "Ставка накопления завышена, возможна техническая ошибка. "
        "Карта заблокирована до выяснения причины."
    )


class InsufficientFundsError(BankError):
    """Ошибка недостатка денег."""

    INSUFFICIENT_FUNDS_FOR_PAYMENT = "Недостаточно денег для оплаты."
    INSUFFICIENT_FUNDS_FOR_TRANSFER = "Недостаточно денег для осуществления перевода."


def print_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BankError as e:
            print(e)
    return wrapper


# ============================== ОСНОВНЫЕ КЛАССЫ ===============================
@dataclass
class User:
    last_name: str
    first_name: str
    pin: str
    phone: str
    user_id: int

    accounts: list = field(default_factory=list)
    cards: list = field(default_factory=list)

    @print_error
    def change_pin(self, old_pin: str, new_pin: str):
        if not isinstance(old_pin, str) or not isinstance(new_pin, str) or len(old_pin) != 4 or len(new_pin) != 4:
            raise ValidationError(ValidationError.PIN_INVALID)
        if not old_pin.isdigit() or not new_pin.isdigit():
            raise ValidationError(ValidationError.PIN_FORMAT_INVALID)
        if old_pin == self.pin:
            self.pin = new_pin
        else:
            raise ValidationError(ValidationError.PIN_MISMATCH)
    

@dataclass
class Account:
    owner: "User"
    acc_id: str
    balance: float = DEFAULT_ACCOUNT_BALANCE
    cashback_balance: float = DEFAULT_CASHBACK_BALANCE


class Card:
    def __init__(
        self,
        account,
        card_id,
        payment_system=DEFAULT_PAYMENT_SYSTEM,
        pan=EMPTY_PAN,
        issue_date=None,
        expiry_date=None,
        currency=CARD_CURRENCY,
        status=CARD_STATUS,
        bank=None,
    ):
        self.account = account
        self.card_id = card_id
        self.payment_system = payment_system
        self.pan = pan
        self.issue_date = issue_date
        self.expiry_date = expiry_date
        self.currency = currency
        self.status = status
        self.bank = bank

        # Обновляем дату заведения и срок окончания карты
        if self.issue_date is None:
            self.issue_date = next(ISSUE_DATE_GENERATOR)
        if self.expiry_date is None and self.issue_date is not None:
            self.expiry_date = _dt.date(
                self.issue_date.year + EXPIRY_YEARS,
                self.issue_date.month,
                self.issue_date.day,
            )

    @print_error
    def get_card_info(self, fields: list = None):
        if self.account is None:
            raise AccessError(AccessError.ACCOUNT_NOT_LINKED)
        if self.status in (CardStatus.CLOSED, CardStatus.BLOCKED):
            raise AccessError(AccessError.CARD_CLOSED)
        
        user = self.account.owner
        data = {
            "bank_name": f"Банк:          {self.bank.name}",
            "bank_bic": f"БИК банка:     {self.bank.bic}",
            "card_id": f"Карта #{self.card_id}",
            "user_id": f"Пользователь:  {user.user_id} — {user.last_name} {user.first_name}",
            "phone": f"Телефон:       {user.phone}",
            "pan": f"PAN:           {self.pan}",
            "acc_id": f"Счёт:          {self.account.acc_id}",
            "payment_system": f"Плат. система: {self.payment_system}",
            "currency": f"Валюта:        {self.currency}",
            "status": f"Статус:        {self.status.value}",
            "issue_date": f"Выпуск:        {self.issue_date}",
            "expiry_date": f"Срок:          {self.expiry_date}",
            "user_cards": f"Карты пользователя: {[card.pan for card in user.cards]}",
            "cashback_balance": f"Кешбэк:        {self.account.cashback_balance:.2f}₽",
            "balance": f"Баланс:        {self.account.balance:.2f}₽"
        }
        
        if fields is None:
            fields = DEFAULT_CARD_INFO_FIELDS

        return (
            "\n".join([data[field] for field in fields if field in data])
            + "\n"
            + "-" * 50
        )

    def __repr__(self):
        return (
            f"Card(card_id={self.card_id}, pan={self.pan}, account={self.account}, "
            f"status={self.status}, issue_date={self.issue_date}, expiry_date={self.expiry_date})"
        )
    
    @print_error
    def get_balance(self):
        if self.account is None:
            raise AccessError(AccessError.ACCOUNT_NOT_LINKED)
        if self.status in (CardStatus.CLOSED, CardStatus.BLOCKED):
            raise AccessError(AccessError.CARD_CLOSED)
        return BALANCE_DESCRIPTION.format(balance=self.account.balance)

    @print_error 
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValidationError(ValidationError.DEPOSIT_AMOUNT_NEGATIVE)
        if not self.account:
            raise AccessError(AccessError.ACCOUNT_NOT_LINKED)
        if self.status in (CardStatus.CLOSED, CardStatus.BLOCKED):
            raise AccessError(AccessError.CARD_CLOSED)
        if amount > DEPOSIT_LIMIT:
            self.status = CardStatus.BLOCKED
            raise BusinessRuleError(BusinessRuleError.DEPOSIT_LIMIT_EXCEEDED)

        self.account.balance += amount
        trans = Transaction(None, 
                            self.card_id, 
                            amount, 
                            TransactionType.DEPOSIT,
                            None,
                            DEPOSIT_DESCRIPTION.format(amount=amount, card_id=self.card_id), 
                            next_timestamp_after(self.issue_date))
        self.bank.transaction_log.append(trans)

    @print_error
    def transfer(self, to_card, amount: float):
        if amount <= 0:
            raise ValidationError(ValidationError.AMOUNT_NEGATIVE)
        if to_card is None:
            raise NotFoundError(NotFoundError.RECIPIENT_NOT_FOUND)
        if self.account is None:
            raise AccessError(AccessError.ACCOUNT_NOT_LINKED)
        if to_card.account is None:
            raise AccessError(AccessError.RECIPIENT_ACCOUNT_NOT_LINKED)
        if self.status in (CardStatus.CLOSED, CardStatus.BLOCKED):
            raise AccessError(AccessError.CARD_CLOSED)
        if to_card.status in (CardStatus.CLOSED, CardStatus.BLOCKED):
            raise AccessError(AccessError.RECIPIENT_CARD_CLOSED)
        if self.card_id == to_card.card_id:
            raise BusinessRuleError(BusinessRuleError.TRANSFER_TO_SELF)
        if amount > TRANSFER_LIMIT:
            self.status = CardStatus.BLOCKED
            raise BusinessRuleError(BusinessRuleError.TRANSFER_LIMIT_EXCEEDED)
        if self.account.balance < amount:
            raise InsufficientFundsError(InsufficientFundsError.INSUFFICIENT_FUNDS_FOR_TRANSFER)

        self.account.balance -= amount
        to_card.account.balance += amount
        trans = Transaction(self.card_id, 
                            to_card.card_id, 
                            amount, 
                            TransactionType.TRANSFER,
                            None,
                            TRANSFER_DESCRIPTION.format(
                                                        amount=amount,
                                                        from_card=self.card_id,
                                                        to_card=to_card.card_id
                            ), 
                            next_timestamp_after(max(self.issue_date, to_card.issue_date))
                            )
        self.bank.transaction_log.append(trans)

    @print_error
    def pay(self, amount: float, mcc: str):
        if amount <= 0:
            raise ValidationError(ValidationError.PAY_AMOUNT_NEGATIVE)
        if not isinstance(mcc, str) or len(mcc) != 4 or not mcc.isdigit():
            raise ValidationError(ValidationError.INVALID_MCC)
        if self.account is None:
            raise AccessError(AccessError.ACCOUNT_NOT_LINKED)
        if self.status in (CardStatus.CLOSED, CardStatus.BLOCKED):
            raise AccessError(AccessError.CARD_CLOSED)
        if mcc in FORBIDDEN_MCC:
            raise BusinessRuleError(BusinessRuleError.MCC_FORBIDDEN.format(mcc=mcc))
        if amount > PAY_LIMIT:
            self.status = CardStatus.BLOCKED
            raise BusinessRuleError(BusinessRuleError.PURCHASE_LIMIT_EXCEEDED)
        if self.account.balance < amount:
            raise InsufficientFundsError(InsufficientFundsError.INSUFFICIENT_FUNDS_FOR_PAYMENT)

        self.account.balance -= amount
        trans = Transaction(self.card_id, 
                            None, 
                            amount, 
                            TransactionType.PAY,
                            mcc,
                            PAY_DESCRIPTION.format(amount=amount, mcc=mcc, card_id=self.card_id), 
                            next_timestamp_after(self.issue_date)
                            )
        self.bank.transaction_log.append(trans)

    def close(self):
        self.status = CardStatus.CLOSED

    @print_error
    def get_transaction_history(self):
        if not self.account:
            raise AccessError(AccessError.ACCOUNT_NOT_LINKED)
        if not self.bank:
            raise AccessError(AccessError.BANK_NOT_LINKED)
        if self.status in (CardStatus.CLOSED, CardStatus.BLOCKED):
            raise AccessError(AccessError.CARD_CLOSED)

        res = []
        for log in self.bank.get_global_history():
            log = {key: value for key, value in zip(TRANSACTION_HISTORY_HEADER[0].split(','), log.split(','))}
            if log['from_card'] == str(self.card_id) or log['to_card'] == str(self.card_id):
                if log['type'] in (TransactionType.DEPOSIT.value, TransactionType.INTEREST.value) or \
                        (log['type'] == TransactionType.TRANSFER.value and log['to_card'] == str(self.card_id)):
                    log['amount'] = '+' + log['amount']
                else:
                    log['amount'] = '-' + log['amount']
                res.append(','.join([log[attr] for attr in TRANSACTION_HISTORY_HEADER[0].split(',')]))
        return res
        

class SimpleDebitCard(Card):
    pass


class CashbackDebitCard(Card):
    def __init__(
        self,
        account,
        card_id,
        payment_system=DEFAULT_PAYMENT_SYSTEM,
        pan=EMPTY_PAN,
        issue_date=None,
        expiry_date=None,
        currency=CARD_CURRENCY,
        status=CARD_STATUS,
        bank=None,
        cashback_rate=DEBIT_DEFAULT_CASHBACK_RATE
    ):
        super().__init__(
            account,
            card_id,
            payment_system,
            pan,
            issue_date,
            expiry_date,
            currency,
            status,
            bank
        )
        self.cashback_rate = cashback_rate
    
    @print_error
    def pay(self, amount: float, mcc: str):
        # т.к. порядок вызова исключений отличается от порядка в родительском классе,
        # то заново переопределяем весь метод
        if amount <= 0:
            raise ValidationError(ValidationError.PAY_AMOUNT_NEGATIVE)
        if not isinstance(mcc, str) or len(mcc) != 4 or not mcc.isdigit():
            raise ValidationError(ValidationError.INVALID_MCC)
        if self.cashback_rate < 0:
            raise ValidationError(ValidationError.CASHBACK_NEGATIVE)
        if self.account is None:
            raise AccessError(AccessError.ACCOUNT_NOT_LINKED)
        if self.status in (CardStatus.CLOSED, CardStatus.BLOCKED):
            raise AccessError(AccessError.CARD_CLOSED)
        if self.cashback_rate >= MAX_CASHBACK_RATE:
            self.status = CardStatus.BLOCKED
            raise BusinessRuleError(BusinessRuleError.CASHBACK_LIMIT)
        if mcc in FORBIDDEN_MCC:
            raise BusinessRuleError(BusinessRuleError.MCC_FORBIDDEN.format(mcc=mcc))
        if amount > PAY_LIMIT:
            self.status = CardStatus.BLOCKED
            raise BusinessRuleError(BusinessRuleError.PURCHASE_LIMIT_EXCEEDED)
        if self.account.balance < amount:
            raise InsufficientFundsError(InsufficientFundsError.INSUFFICIENT_FUNDS_FOR_PAYMENT)

        cashback_amount = round((amount * self.cashback_rate), 2)
        self.account.cashback_balance += cashback_amount
        self.account.balance -= amount
        trans = Transaction(self.card_id, 
                            None, 
                            amount, 
                            TransactionType.PAY,
                            mcc,
                            CB_DEBIT_PAY_DESCRIPTION.format(
                                                            amount=amount,
                                                            mcc=mcc,
                                                            card_id=self.card_id,
                                                            cashback_amount=cashback_amount
                            ), 
                            next_timestamp_after(self.issue_date),
                            cashback_amount
                            )
        self.bank.transaction_log.append(trans)


class SavingCard(Card):
    def __init__(
        self,
        account,
        card_id,
        payment_system=DEFAULT_PAYMENT_SYSTEM,
        pan=EMPTY_PAN,
        issue_date=None,
        expiry_date=None,
        currency=CARD_CURRENCY,
        status=CARD_STATUS,
        bank=None,
        interest_rate=SAVING_CARD_DEFAULT_INTEREST
    ):
        super().__init__(
            account,
            card_id,
            payment_system,
            pan,
            issue_date,
            expiry_date,
            currency,
            status,
            bank
        )
        self.interest_rate = interest_rate
    
    @print_error
    def accrue_interest(self):
        # т.к. порядок вызова исключений отличается от порядка в родительском классе,
        # то заново переопределяем весь метод
        if self.interest_rate < 0:
            raise ValidationError(ValidationError.INTEREST_NEGATIVE)
        if self.account is None:
            raise AccessError(AccessError.ACCOUNT_NOT_LINKED)
        if self.status in (CardStatus.CLOSED, CardStatus.BLOCKED):
            raise AccessError(AccessError.CARD_CLOSED)
        if self.interest_rate >= MAX_SAVING_INTEREST_RATE:
            self.status = CardStatus.BLOCKED
            raise BusinessRuleError(BusinessRuleError.SAVING_RATE_TOO_HIGH)

        interest = round((self.account.balance * self.interest_rate), 2)
        self.account.balance += interest
        trans = Transaction(None, 
                            self.card_id, 
                            interest, 
                            TransactionType.INTEREST,
                            None,
                            SAVING_INTEREST_DESCRIPTION.format(interest=interest, card_id=self.card_id), 
                            next_timestamp_after(self.issue_date))
        self.bank.transaction_log.append(trans)
    
    @print_error
    def pay(self, *args, **kwargs):
        raise BusinessRuleError(BusinessRuleError.PAYMENT_NOT_ALLOWED_FOR_SAVING)


@dataclass
class Bank:
    name: str
    bic: str

    _user_seq: int = field(default_factory=lambda: _it.count(1), init=False)
    _account_seq: int = field(default_factory=lambda: _it.count(1), init=False)
    _card_seq: int = field(default_factory=lambda: _it.count(1), init=False)
    _pan_seq: int = field(default_factory=lambda: _it.count(1), init=False)

    customers: dict = field(default_factory=dict)
    accounts: dict = field(default_factory=dict)
    cards: dict = field(default_factory=dict)
    transaction_log: list = field(default_factory=list)

    def _next_account_number(self):
        prefix_left = ACCOUNT_TYPE_CODE + ACCOUNT_CURRENCY
        prefix_right = ACCOUNT_BRANCH
        bic_tail = self.bic[-3:]
        serial = f"{next(self._account_seq):07d}"

        for control_digit in range(10):
            candidate_account_number = prefix_left + str(control_digit) + prefix_right + serial
            digits = [int(d) for d in bic_tail + candidate_account_number]
            weights = [7, 1, 3] * 8
            weighted = [a * b for a, b in zip(digits, weights[:23])]
            control_sum = sum(x % 10 for x in weighted)
            if control_sum % 10 == 0:
                return candidate_account_number

    def _generate_pan(self, system):
        bin_code = BIN_BY_SYSTEM.get(
            system.upper(), BIN_BY_SYSTEM[DEFAULT_PAYMENT_SYSTEM]
        )
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

    def issue_simple_debit_card(self, last_name, first_name, pin, phone, payment_system, **kwargs):
        return self.apply_for_card(
            last_name,
            first_name,
            pin,
            phone,
            payment_system,
            card_class=SimpleDebitCard,
            **kwargs
        )

    def issue_cashback_debit_card(self, last_name, first_name, pin, phone, payment_system, **kwargs):
        return self.apply_for_card(
            last_name,
            first_name,
            pin,
            phone,
            payment_system,
            card_class=CashbackDebitCard,
            **kwargs
        )

    def issue_saving_card(self, last_name, first_name, pin, phone, payment_system, **kwargs):
        return self.apply_for_card(
            last_name,
            first_name,
            pin,
            phone,
            payment_system,
            card_class=SavingCard,
            **kwargs
        )

    @print_error
    def apply_for_card(
        self,
        last_name,
        first_name,
        pin,
        phone,
        payment_system=DEFAULT_PAYMENT_SYSTEM,
        card_class: type = Card,
        **kwargs
    ):
        if not (isinstance(pin, str) and pin.isdigit()):
            raise ValidationError(ValidationError.PIN_FORMAT_INVALID)
        if not (isinstance(pin, str) and len(pin) == 4):
            raise ValidationError(ValidationError.PIN_INVALID)
        if re.match(RUSSIAN_PATTERN, last_name) is None:
            raise ValidationError(ValidationError.NAME_INVALID)
        if re.match(RUSSIAN_PATTERN, first_name) is None:
            raise ValidationError(ValidationError.NAME_INVALID)
        if payment_system.upper() not in BIN_BY_SYSTEM:
            raise ValidationError(ValidationError.PAYMENT_SYSTEM_NOT_SUPPORTED.format(payment_system=payment_system))

        for id, user in self.customers.items():
            if (user.last_name, user.first_name, user.phone) == (last_name, first_name, phone):
                user_id = id
                break
            if user.phone == phone:
                raise BusinessRuleError(BusinessRuleError.USER_CONFLICT)
        else:
            user_id = next(self._user_seq)
            self.customers[user_id] = User(last_name, first_name, pin, phone, user_id)

        user = self.customers[user_id]

        if len(user.cards) >= 5:
            raise BusinessRuleError(BusinessRuleError.TOO_MANY_DEBIT_CARDS)

        account = Account(user, self._next_account_number())
        self.accounts[account.acc_id] = account
        user.accounts.append(account)

        card = card_class(
            account,
            next(self._card_seq),
            payment_system,
            self._generate_pan(payment_system),
            bank=self,
            **kwargs
        )
        self.cards[card.card_id] = card
        user.cards.append(card)

        return card
        
    def get_global_history(self):
        print(TRANSACTION_HISTORY_HEADER[0])
        self.transaction_log.sort(key=lambda trans: trans.timestamp)
        for log in self.transaction_log:
            history = []
            for attr in TRANSACTION_HISTORY_HEADER[0].split(','):
                if attr == 'type':
                    history.append(log.type.value)
                elif attr == 'amount' or attr == 'cashback':
                    history.append(f'{getattr(log, attr):.2f}₽')
                elif getattr(log, attr) is None:
                    history.append('')
                else:
                    history.append(str(getattr(log, attr)))
            yield ','.join(history)
  
          
@dataclass
class Transaction:
    from_card: int | None
    to_card: int | None
    amount: float
    type: TransactionType
    mcc: str | None
    description: str
    timestamp: _dt.datetime
    cashback: float = DEFAULT_CASHBACK_TRANSACTION


# TO DO Добавить новые методы: оплату кешбэком, перевод в другой банк, ввести таблицу кешбэка на разные товары
# TO DO Выпустить новые карты: кредитная, VIP карта (два в одном и кредитка и дебетовая).
# TO DO Использовать модуль Decimal для работы с десятичными дробями