import numpy as np
from datetime import datetime


class ER:
    def er_algorithm(self, B, W, DBF, numOfChildren, numOfGrades):
        # 初始化变量
        strErrorMessage = ""
        MTilde = numOfGrades
        MBar = numOfGrades + 1
        ng2 = numOfGrades + 2

        # 创建一个二维数组 M
        M = np.zeros((numOfChildren, ng2), dtype=float)

        # 将 DBF 数组转换为 M 矩阵
        for i in range(numOfChildren):
            for j in range(numOfGrades):
                M[i, j] = DBF[i, j]

        # 归一化 W 数组
        sngSum = np.sum(W)
        if sngSum == 0:
            strErrorMessage += " | Divided by 0 (sngSum) in ER_Algorithm at " + str(datetime.now()) + ". | "
        else:
            W /= sngSum

        # 计算不完整因子和权重因子
        for i in range(numOfChildren):
            sngIncomplete = np.sum(M[i, :numOfGrades])
            M[i, MTilde] = W[i] * (1.0 - sngIncomplete)  # 不完整因子
            M[i, MBar] = 1.0 - W[i]  # 权重因子

        # 更新 M 矩阵中的概率分配
        for i in range(numOfChildren):
            for j in range(numOfGrades):
                M[i, j] *= W[i]

        # 结合所有因子并存储在 B 中
        B[:numOfGrades] = M[0, :numOfGrades]
        B[MTilde] = M[0, MTilde]
        BBar = M[0, MBar]

        # 递归地结合所有因子
        for r in range(1, numOfChildren):
            K = 1.0 - np.sum([B[i] * M[r, j] for i in range(numOfGrades) for j in range(numOfGrades) if j != i])
            if K != 0:
                K = 1.0 / K
            else:
                strErrorMessage += " | Divided by 0 (K) in ER_Algorithm at " + str(datetime.now()) + ". | "

            for n in range(numOfGrades):
                B[n] = K * (B[n] * M[r, n] + B[n] * (M[r, MTilde] + M[r, MBar]) + (B[MTilde] + BBar) * M[r, n])

            B[MTilde] = K * (B[MTilde] * M[r, MTilde] + BBar * M[r, MTilde] + B[MTilde] * M[r, MBar])
            BBar = K * BBar * M[r, MBar]

        # 使用完整性因子归一化组合的信度
        sngNormal = 1.0 - BBar
        if sngNormal != 0:
            B /= sngNormal
        else:
            strErrorMessage += " | Divided by 0 (sngNormal) in ER_Algorithm at " + str(datetime.now()) + ". | "

        # 检查是否有错误信息
        if strErrorMessage:
            print(strErrorMessage)
            return False
        else:
            return True