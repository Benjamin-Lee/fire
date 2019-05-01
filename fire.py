import click

def parse(ctx, param, money: str) -> float:
	return float(money.replace("$", "").replace(",", ""))

@click.command()
@click.option("--checking", prompt=True, callback=parse)
@click.option("--credit", prompt="Credit balance", callback=parse)
@click.option("--checking-target", default="$1000.00", callback=parse)
@click.option("--savings-ratio", default=0.2)
def budget(checking, credit, checking_target, savings_ratio):

	# how much money I have left in checking after paying credit card
	after_paying_credit = checking - credit

	# if I don't have enough money to cover the credit card bill without dropping below target
	if after_paying_credit < checking_target:
		click.secho("Make more money or spend less. You have to live like no one else so later you can live like no one else!", fg="red")
		to_savings = -1 * credit # draw from savings so as not to empty checking
		to_retirement = 0 # no money to retirement


	# how much money I have left over
	income = after_paying_credit - checking_target

	# if I have anything left over, allocate to savings and retirement
	if income >= 0:
		to_savings = income * savings_ratio
		to_retirement = income - to_savings

	# prettify the numbers
	credit, to_savings, to_retirement = map(lambda x: "%.2f" % x, (credit, to_savings, to_retirement))

	printout = f"""
To\tAmount
--\t------
Credit card\t${credit}
Savings\t${to_savings}
Retirement\t${to_retirement}
""".expandtabs(15)

	print(printout)

if __name__ == '__main__':
	budget()
