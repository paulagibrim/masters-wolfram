class Class:
    def __init__(self, id):
        self.__id = id
        self.__label = self.__set_labels()
        self.__rules = []

        self.__set_rules()

    ### VALIDATION METHODS ###

    def validate_id(self):
        valid_ids = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}

        if isinstance(self.__id, str):
            if self.__id not in valid_ids:
                raise ValueError("Invalid ID. Must be 'I', 'II', 'III', or 'IV'.")
            self.__id = valid_ids[self.__id]  # Converte string para inteiro.

        if isinstance(self.__id, int):
            if self.__id not in valid_ids.values():
                raise ValueError("Invalid ID. Must be 1, 2, 3, or 4.")



    ### GETTERS AND SETTERS ###
    
    def get_id(self):
        return self.__id
    
    def get_label(self):
        return self.__label
    
    def get_rules(self):
        return self.__rules


    def __set_rules(self):
            self.validate_id()
            if self.__id == 1:
                self.__rules = [0, 8, 32, 40, 64, 96, 128, 136, 160, 168, 192, 224, 234, 
                              235, 238, 239, 248, 249, 250, 251, 252, 253, 254, 255]
            elif self.__id == 2:
                self.__rules = [1, 2, 3, 4, 5, 6, 7, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 
                              23, 24, 25, 26, 27, 28, 29, 31, 33, 34, 35, 36, 37, 38, 39, 42, 43, 
                              44, 46, 47, 48, 49, 50, 51, 52, 53, 55, 56, 57, 58, 59, 61, 62, 63, 
                              65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 76, 77, 78, 79, 80, 81, 82, 
                              83, 84, 85, 87, 88, 91, 92, 93, 94, 95, 98, 99,  100, 103, 104, 108, 
                              109, 111, 112, 113, 114, 115, 116, 117, 118, 119, 123, 125, 127, 130, 
                              131, 132, 133, 134, 138, 139, 140, 141, 142, 143, 144, 145, 148, 152, 
                              154, 155, 156, 157, 158, 159, 162, 163, 164, 166, 167, 170, 171, 172, 
                              173, 174, 175, 176, 177, 178, 179, 180, 181, 184, 185, 186, 187, 188, 
                              189, 190, 191, 194, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 
                              206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 
                              220, 221, 222, 223, 226, 227, 228, 229, 230, 231, 232, 233, 236, 237, 
                              240, 241, 242, 243, 244, 245, 246, 247]
            elif self.__id == 3:
                self.__rules = [18, 22, 30, 45, 60, 75, 86, 89, 90, 101, 102, 105, 122, 126, 129, 
                              135, 146, 149, 150, 151, 153, 161, 165, 182, 183, 195]
            
            elif self.__id == 4:
                self.__rules = [41, 54, 97, 106, 107, 110, 120, 121, 124, 137, 147, 169, 193, 225]

    def __set_labels(self):
        self.validate_id()
        if self.__id == 1:
            return 'I_Homogeneous'
        elif self.__id == 2:
            return 'II_Periodic'
        elif self.__id == 3:
            return 'III_Chaotic'
        elif self.__id == 4:
            return 'IV_Complex'

HOMOGENEOUS = Class(1)
PERIODIC = Class(2)
CHAOTIC = Class(3)
COMPLEX = Class(4)

