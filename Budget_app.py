import math


class Category:
    """
    Classe représentant une catégorie de dépenses.
    Permet de gérer les dépôts, les retraits et le solde d'une catégorie.
    """

    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        """Ajoute un montant à la catégorie."""
        self.ledger.append({'amount': amount, 'description': description})

    def withdraw(self, amount, description=""):
        """Retire un montant de la catégorie si les fonds sont suffisants."""
        if amount > self.get_balance():
            return False
        self.ledger.append({'amount': -amount, 'description': description})
        return True

    def get_balance(self):
        """Calcule le solde actuel de la catégorie."""
        return sum(entry['amount'] for entry in self.ledger)

    def transfer(self, amount, category):
        """Transfère un montant d'une catégorie vers une autre."""
        if not self.check_funds(amount):
            return False

        self.withdraw(amount, f"Transfer to {category.name}")
        category.deposit(amount, f"Transfer from {self.name}")
        return True

    def check_funds(self, amount):
        """Vérifie si le solde est suffisant pour un retrait."""
        return amount <= self.get_balance()

    def __str__(self):
        """Retourne une représentation textuelle du grand livre (ledger)."""
        title = self.name.center(30, "*")
        entries = []

        for entry in self.ledger:
            description = entry['description'][:23]
            amount = f"{entry['amount']:.2f}"[:7]
            entries.append(f"{description:<23}{amount:>7}")

        total = self.get_balance()
        return "\n".join([title, *entries, f"Total: {total:.2f}"])


def create_spend_chart(categories):
    """
    Génère un graphique en barres représentant le pourcentage 
    des dépenses par catégorie.
    """
    spent_amounts = []

    for category in categories:
        spent_amounts.append(
            sum(-entry['amount']
                for entry in category.ledger if entry['amount'] < 0)
        )

    total_spent = sum(spent_amounts)
    percentages = [
        int(amount / total_spent * 100) // 10 * 10 if total_spent else 0
        for amount in spent_amounts
    ]

    chart = "Percentage spent by category\n"
    for level in range(100, -1, -10):
        chart += f"{level:>3}| "
        for percentage in percentages:
            chart += "o  " if percentage >= level else "   "
        chart += "\n"

    chart += "    -" + "---" * len(categories) + "\n"
    longest_name = max((len(category.name)
                       for category in categories), default=0)

    for index in range(longest_//name):
        chart += "     "
        for category in categories:
            chart += (category.name[index] if index <
                      len(category.name) else " ") + "  "
        chart += "\n"

    return chart.rstrip("\n")
