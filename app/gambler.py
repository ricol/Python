#!/usr/bin/env python
#-*- coding: utf-8 -*-

class gambler():
    def __init__(self):
        self.deposit = 1e6
        self.bet = 2e4
        self.usury = 0
        self.lose = 0

Cathala = gambler()
Cathala.bet = 1e8
Cathala.deposit = 1e8

Geralt = gambler()

bet = 1000
count = 0
gambling_list = []

def gambling(gambler_a, gambler_b, bet, count):
    point = random.randint(2, 12)
    guess = random.randint(0, 1)
    if (point > 7 and guess == 1) or (point <= 7 and guess == 0):
        Geralt.bet += bet
        Cathala.bet -= bet
        return True
    else:
        Geralt.bet -= bet
        Cathala.bet += bet
        return False

def one_day_gambling():
    Geralt.bet = 2e4
    bet = 1000
    count = 0
    while True:
        gambling_list.append(gambling(Cathala, Geralt, bet, count))
        count += 1
        if count > 3 and gambling_list[count - 3] == gambling_list[count - 2] == gambling_list[count - 1] == False:
            bet *= 1.5
        if Geralt.bet <= -5e3 or count >= 100:
            break
    return Geralt.bet - 2e4

def record_daily_gambling():
    debt = []
    for i in range(3000):
        n = one_day_gambling()
        if n < 0:
            n *= 1.00167
        debt.append(n)
        if sum(debt) <= -1e6:
            return (sum(debt), i)

    return (sum(debt), 3000)

def main():
    every_example = pd.DataFrame()
    lost_money = []
    bankcrupt_time = []
    for j in range(1000):
        m = record_daily_gambling()
        lost_money.append(m[0])
        bankcrupt_time.append(m[1])
        print(j)
    every_example['lost_money'] = lost_money
    every_example['bankcrupt_time'] = bankcrupt_time
    every_example.to_csv('experiment_data.csv', index=False, sep=',')

if __name__ == "__main__":
    main()
