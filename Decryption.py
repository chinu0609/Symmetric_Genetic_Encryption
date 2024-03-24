from collections import deque

from getting_data import Data_Prep


class Decrypt(Data_Prep):
    def __init__(self, file_name: str):
        super().__init__(file_name)
        self.break_to_16()

    def gen_algo(self, ind, cross_over_points, mutations):

        # print(self.cross_over_points)

        for i in range(cross_over_points[0] + 1, cross_over_points[1] + 1):
            # print(i)
            c = self.parts_16[ind][i]
            self.parts_16[ind][i] = self.parts_16[ind + 1][i]
            self.parts_16[ind + 1][i] = c
        for j in range(cross_over_points[2] + 1, cross_over_points[3] + 1):
            c1 = self.parts_16[ind][j]
            self.parts_16[ind][j] = self.parts_16[ind + 1][j]
            self.parts_16[ind + 1][j] = c1
        for mu in mutations:
            self.parts_16[ind][mu] = 128 - self.parts_16[ind][mu]
            self.parts_16[ind + 1][mu] = 128 - self.parts_16[ind + 1][mu]

    def decryption(self):
        ff = open("public_key.txt", "r")
        per = 0
        params = []
        rand = 0
        count = 0
        for i in ff.readlines():
            if count <= 1:

                params.append(i)
            elif count == 2:
                per = int(i)
            else:
                rand = int(i)
            count += 1
        for b in range(0, len(params)):
            params[b] = eval(params[b])
        # per = self.permutation_factor
        # params = self.cross_over_points + self.mutations
        for ind in range(0, len(self.parts_16), 2):
            if ind == 0:

                self.gen_algo(ind, params[0], params[1])
                params = params[0] + params[1]

                print(params)
            else:
                params = deque(params)
                params.rotate(-1 * per)
                params = params
                print(params)
                cross_temp = []
                mutation_temp = []
                c = 0

                for i in params:
                    if c < 4:
                        cross_temp.append(i)
                    elif c > 3 and c < 7:
                        mutation_temp.append(i)

                self.gen_algo(ind, cross_temp, mutation_temp)
            f = open("decrypt.txt", "wb")
            bytea = sum(self.parts_16, [])
            bytess = bytes(bytea)
            f.write(bytess)
            f.close()


if __name__ == "__main__":
    o = Decrypt("encrypt.txt")
    o.decryption()
