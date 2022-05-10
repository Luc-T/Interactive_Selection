import random


class Dna:
    #static variable for maximum possible amount of genes needed
    LEN = 28
    
    def __init__ (self, newgenes):
        if (len(newgenes) == self.LEN):
            self.genes = newgenes
        else:
            self.genes = []
            for i in range(self.LEN):
                self.genes.append(random.random())


    def get_genes(self):
        return self.genes

    # combine genes list of two parents to make and return child
    def crossover(self, partner):
        partner_genes = partner.get_genes()
        newgenes = []
        crossover = random.randint(1, self.LEN)
        for i in range(self.LEN):
            if i > crossover: newgenes.append(self.genes[i])
            else: newgenes.append(partner_genes[i])
        
        child = Dna(newgenes)
        return child

    #go through list of genes and potentially change them
    def mutate(self, m):
        for i in range(self.LEN):
            if random.random() < m:
                self.genes[i] = random.random()