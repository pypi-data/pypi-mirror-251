class KingdomRelations:
    def __init__(self):
        self.relations = {}
        self.vote_counts = {"ghaniyar": {"vaali": 3, "gurung": 3, "cheeka": 3, "ranga": 3, "narang": 3, "vishnu": 3},
                            "mannar": {"shiva_mannar": 0, "raja_mannar": 15, "varadha_raj_mannar": 1,
                                       "baachi": 0, "rudra": 1, "radha_rama": 0, "om": 1}}

        # Adding initial relationships
        self.add_relation("dhaara", "devaratha_raisaar", "father")
        self.add_relation("baarava", "raja_mannar", "son_in_law")
        self.add_relation("baarava", "radha_rama", "husband")
        self.add_relation("shiva_mannar", "raja_mannar", "father")
        self.add_relation("raja_mannar", "varadha_raj_mannar", "second_wife_son")
        self.add_relation("raja_mannar", "baachi", "second_wife_son")
        self.add_relation("raja_mannar", "rudra", "first_wife_son")
        self.add_relation("raja_mannar", "radha_rama", "first_wife_daughter")
        self.add_relation("raja_mannar", "om", "first_wife_brother")
        self.add_relation("narang", "vishnu", "son")

        # Adding all relationships
        self.add_relation("dhaara", "devaratha_raisaar", "father")
        

        self.add_relation("devaratha_raisaar", "dhaara", "son or child")
        

        
        
        self.add_relation("baarava", "radha_rama", "husband")
        self.add_relation("baarava", "raja_mannar", "son_in_law")
        self.add_relation("baarava", "rudra", "cousin brother")
        self.add_relation("baarava", "om", "son type relation")
        self.add_relation("baarava", "varadha_raj_mannar", "brother in law")
        self.add_relation("baarava", "baachi", "cousin brother")
        self.add_relation("baarava", "shiva_mannar", "grandson")


        

        self.add_relation("shiva_mannar", "raja_mannar", "father")
        self.add_relation("shiva_mannar", "baarava", "grand father")
        self.add_relation("shiva_mannar", "varadha_raj_mannar", "grand father")
        self.add_relation("shiva_mannar", "baachi", "grand father")
        self.add_relation("shiva_mannar", "rudra", "grand father")
        self.add_relation("shiva_mannar", "radha_rama", "grand father")
        self.add_relation("shiva_mannar", "om", "uncle")
        
        

        self.add_relation("raja_mannar", "shiva_mannar", "son or child")
        self.add_relation("raja_mannar", "varadha_raj_mannar", "father")
        self.add_relation("raja_mannar", "baachi", "father")
        self.add_relation("raja_mannar", "rudra", "father")
        self.add_relation("raja_mannar", "radha_rama", "father")
        self.add_relation("raja_mannar", "om", "first_wife_brother")
        self.add_relation("raja_mannar", "baarava", "father_in_law")
        
        
        
        
        self.add_relation("varadha_raj_mannar", "raja_mannar", "father")
        self.add_relation("varadha_raj_mannar", "shiva_mannar", "grand son")
        self.add_relation("varadha_raj_mannar", "rudra", "brother")
        self.add_relation("varadha_raj_mannar", "radha_rama", "brother")
        self.add_relation("varadha_raj_mannar", "baachi", "brother")
        self.add_relation("varadha_raj_mannar", "om", "son-in-law")
        self.add_relation("varadha_raj_mannar", "baarava", "brother in law")
        
        
        

        self.add_relation("baachi", "raja_mannar", "son")
        self.add_relation("baachi", "rudra", "brother")
        self.add_relation("baachi", "radha_rama", "brother")
        self.add_relation("baachi", "om", "son in law")
        self.add_relation("baachi", "shiva_mannar", "grand son")
        self.add_relation("baachi", "varadha_raj_mannar", "brother")
        self.add_relation("baachi", "baarava", "brother in law")
        
        
        
        

        self.add_relation("rudra", "raja_mannar", "first wife son")
        self.add_relation("rudra", "varadha_raj_mannar", "brother")
        self.add_relation("rudra", "radha_rama", "brother")
        self.add_relation("rudra", "baachi", "brother")
        self.add_relation("rudra", "baarava", "brother")
        self.add_relation("rudra", "om", "son in law")
        self.add_relation("rudra", "raja_mannar", "first wife son")
        self.add_relation("rudra", "shiva_mannar", "grandson")
        
        
        

        self.add_relation("radha_rama", "shiva_mannar", "grand dauther")
        self.add_relation("radha_rama", "raja_mannar", "dauther")
        self.add_relation("radha_rama", "varadha_raj_mannar", "sister")
        self.add_relation("radha_rama", "rudra", "sister")
        self.add_relation("radha_rama", "om", "dauther in law")
        self.add_relation("radha_rama", "baarava", "wife")
        self.add_relation("radha_rama", "baachi", "sister")
        
        
        

        self.add_relation("om", "raja_mannar", "son in law")
        self.add_relation("om", "baarava", "father type relation ")
        self.add_relation("om", "varadha_raj_mannar", "uncle")
        self.add_relation("om", "rudra", "uncle")
        self.add_relation("om", "radha_rama", "uncle")
        self.add_relation("om", "shiva_mannar", "son in law")
        self.add_relation("om", "baachi", "uncle")

        self.add_relation("vishnu", "narang", "child")
        self.add_relation("narang", "vishnu", "father")

    def add_relation(self, person1, person2, relationship):
        self.relations.setdefault(person1, {})[person2] = relationship
        self.relations.setdefault(person2, {})[person1] = relationship

    def get_relationship(self, person1, person2):
        if person1 in self.relations and person2 in self.relations[person1]:
            return self.relations[person1][person2]
        else:
            return "No relationship found."

    def get_vote_count(self, tribe, person):
        if tribe.lower() in self.vote_counts and person.lower() in self.vote_counts[tribe.lower()]:
            return self.vote_counts[tribe.lower()][person.lower()]
        else:
            return "Invalid tribe or person."

# Example usage:
if __name__ == "__main__":
    salaar_relations = KingdomRelations()

    # Example relationships
    # print(salaar_relations.get_relationship(c))
    print(salaar_relations.get_relationship("baarava", "raja_mannar"))
    print(salaar_relations.get_relationship("baarava", "radha_rama"))
    print(salaar_relations.get_relationship("shiva_mannar", "raja_mannar"))

    # Example vote counts
    print(salaar_relations.get_vote_count("ghaniyar", "vishnu"))
    print(salaar_relations.get_vote_count("mannar", "shiva_mannar"))
