class Category:
    def __str__(self):
      out = self.name.center(30, "*")
      out += ("\n")
      for i in self.ledger:
        out += (f"{i['description'][:23]:<23}{i['amount']:>7.2f}\n")
      out += (f"Total: {self.get_balance():.2f}")
      return out
      

      
    def __init__(self, name):
      self.name = name
      self.ledger = []
      self.current_bal = 0
      
    def deposit(self, amount, description = ""):
      self.current_bal += amount
      self.ledger.append({"amount": amount, "description": description})
      
    def withdraw(self, amount, description = ""):
      if self.check_funds(amount):
        self.current_bal -= amount
        self.ledger.append({"amount": -amount, "description": description})
        return True
      return False

    def get_balance(self):
      return self.current_bal

    def transfer(self, amount, category):
      if self.check_funds(amount):
        self.withdraw(amount, f"Transfer to {category.name}")
        category.deposit(amount, f"Transfer from {self.name}")
        return True
      else:
        return False
        

    def check_funds(self, amount):
      return not amount > self.current_bal

    def get_withdrawals(self):
      # Calculate total withdrawals
      withdrawals = sum(item['amount'] for item in self.ledger if item['amount'] < 0)
      return withdrawals
      

def create_spend_chart(categories):
  chart = "Percentage spent by category\n"
  # Calculate the total withdrawals
  total_withdrawals = sum(category.get_withdrawals() for category in categories)

  # Calculate the percentage spent in each category
  percentages = [(category.get_withdrawals() / total_withdrawals) * 100 if total_withdrawals != 0 else 0 for category in categories]


  # Create the chart
  for i in range(100, -1, -10):
      chart += str(i).rjust(3) + "| "
      for percent in percentages:
          chart += "o" if percent >= i else " "
          chart += "  "
      chart += "\n"

  chart += "    -" + "---" * len(categories) + "\n"

  # Write category names vertically
  max_length = max(len(category.name) for category in categories)
  for i in range(max_length):
      chart += "     "
      for category in categories:
          if i < len(category.name):
              chart += category.name[i] + "  "
          else:
              chart += "   "
      chart += "\n" if i < max_length - 1 else ""
  return chart

