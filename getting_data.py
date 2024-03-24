import random


class Data_Prep:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.parts_16 = None

    def break_to_16(self):
        f_po = open(self.file_name, "rb")
        l_16 = []
        __ = []
        flag = 0
        for i in f_po.read():
            if flag >= 16:
                flag = 0
                l_16.append(__)
                __ = []
            __.append(i)
            flag += 1
        if len(l_16) % 2 != 0:
            l_16.append([0] * 16)
        # l_16.append([random.randint(0,127)]*16)
        if len(l_16[-1]) != 16:
            l_16 = l_16 + [0] * (len(16 - l_16[0]))
        # [random.randint(0,127)]*(len(16 - l_16[0]))

        self.parts_16 = l_16
        return self.parts_16


if __name__ == "__main__":
    obj = Data_Prep(file_name="./getting_data.py")
    obj.break_to_16()
