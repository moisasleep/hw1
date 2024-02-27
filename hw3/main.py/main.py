import os
import csv

# File paths
budget_data_path = os.path.join('/Users/morgan.foge/Desktop/hw3/PyBank/Resources/budget_data.csv')
election_data_path = os.path.join('/Users/morgan.foge/Desktop/hw3/PyPoll/Resources/election_data.csv')

# Output paths
budget_output_path = os.path.join("analysis", "budget_analysis.txt")
election_output_path = os.path.join("analysis", "election_analysis.txt")

# Function to calculate average
def calculate_average(changes):
    return sum(changes) / len(changes)

# Function to find winner
def find_winner(candidate_votes):
    winner = max(candidate_votes, key=candidate_votes.get)
    return winner

# Financial analysis variables
months = 0
total_profit_loss = 0
previous_profit_loss = 0
profit_loss_changes = {}
greatest_increase = 0
greatest_decrease = 0

# Election analysis variables
total_votes = 0
candidates = {}
winner = ""

# Reading and processing budget data
with open(budget_data_path) as budget_file:
    budget_reader = csv.reader(budget_file)
    next(budget_reader)
    for row in budget_reader:
        months += 1
        profit_loss = int(row[1])
        total_profit_loss += profit_loss
        if months > 1:
            change = profit_loss - previous_profit_loss
            profit_loss_changes[row[0]] = change
            if change > greatest_increase:
                greatest_increase = change
                greatest_increase_month = row[0]
            elif change < greatest_decrease:
                greatest_decrease = change
                greatest_decrease_month = row[0]
        previous_profit_loss = profit_loss

# Calculating average change
average_change = calculate_average(profit_loss_changes.values())

# Reading and processing election data
with open(election_data_path) as election_file:
    election_reader = csv.reader(election_file)
    next(election_reader)
    for row in election_reader:
        total_votes += 1
        candidate = row[2]
        if candidate in candidates:
            candidates[candidate] += 1
        else:
            candidates[candidate] = 1

# Finding winner
winner = find_winner(candidates)

# Writing financial analysis output
budget_output = (
    f"Financial Analysis\n"
    f"---------------------------\n"
    f"Total Months: {months}\n"
    f"Total: ${total_profit_loss}\n"
    f"Average Change: ${average_change:.2f}\n"
    f"Greatest Increase in Profits: {greatest_increase_month} (${greatest_increase})\n"
    f"Greatest Decrease in Profits: {greatest_decrease_month} (${greatest_decrease})\n"
)

# Writing election analysis output
election_output = (
    f"Election Results\n"
    f"--------------------\n"
    f"Total Votes: {total_votes}\n"
    f"--------------------\n"
)
for candidate, votes in candidates.items():
    percentage = (votes / total_votes) * 100
    election_output += f"{candidate}: {percentage:.3f}% ({votes})\n"
election_output += (
    f"--------------------\n"
    f"Winner: {winner}\n"
    f"--------------------\n"
)

# Printing and saving outputs
print(budget_output)
print(election_output)

with open(budget_output_path, "w") as budget_output_file:
    budget_output_file.write(budget_output)

with open(election_output_path, "w") as election_output_file:
    election_output_file.write(election_output)