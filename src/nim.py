import random

class nim:
    def __init__(self):
        self.piles = []
        self.reset()

    def player_move(self, pile, stones) -> bool:
        if ((1 <= pile <= len(self.piles)) and (1 <= stones <= self.piles[pile - 1])):
            self.piles[pile - 1] -= stones;
            return True;
        else:
            return False;


    def pc_move(self):
        nim_sum = 0;
        for pile in self.piles:
            nim_sum ^= pile;

        if (nim_sum != 0):
            for i in range(len(self.piles)):
                target_size = self.piles[i] ^ nim_sum;
                if (target_size < self.piles[i]):
                    take = self.piles[i] - target_size;
                    self.piles[i] -= take;
                    return [i+1, take];

        non_empty_piles = [i for i, count in enumerate(self.piles) if count > 0];
        if (non_empty_piles): 
            pile_index = random.choice(non_empty_piles);
            take = random.randint(1, self.piles[pile_index]);
            self.piles[pile_index] -= take;
            return [pile_index+1, take];


    def get_bunches(self) -> list:
        return self.piles;

    def check_winner(self) -> bool:
        if (sum(self.piles) == 0):
            return True;
        else:
            return False;

    def reset(self) -> None:
        num_piles = random.randint(2, 4);
        self.piles = [random.randint(4, 14) for _ in range(num_piles)];




