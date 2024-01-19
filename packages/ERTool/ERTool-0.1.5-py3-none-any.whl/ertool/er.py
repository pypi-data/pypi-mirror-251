import numpy as np

def er_algorithm(W, DBF, numOfChildren, numOfGrades):
    """
    Input Variables:
        - W: A one-dimensional array of floats. It represents the weights of each child node. Tese weights are used in the algorithm to adjust the influence of each child node.
        - DBF: A two-dimensional array of floats. It stands for "Degrees of Belief" and is one of the main inputs to the algorithm, used to represent the initial belief degrees for each category or grade.
        - numOfChildren: An integer. It indicates the number of child nodes. In the DBF array, this typically corresponds to the number of rows.
        - numOfGrades: An integer. It indicates the number of categories or grades. In the DBF array, this typically corresponds to the number of columns.
    
    Output Values:
        - B Array: Upon completion of the algorithm, the B array is updated with the final calculation results. It reflects the degrees of belief that have been weighted and normalized.
        - False(Boolean). It returns True if the algorithm successfully executes and completes all computations. If any error is encountered during execution (e.g., division by zero), it returns False.
    """

    if len(DBF) != numOfChildren or len(DBF[0]) != numOfGrades or numOfChildren < 1 or numOfGrades < 1:
        print("An error occurred during the execution of the algorithm.")
        print(" | The input variables are incorrect. Please check them again. | ")
        return False
    
    B = np.zeros(numOfGrades+1)
    
    if not isinstance(W, np.ndarray):
        W = np.array(W)
    if not isinstance(DBF, np.ndarray):
        DBF = np.array(DBF)

    W = W / W.sum()

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
        strErrorMessage += " | Divided by 0 (sngSum) in er_algorithm. | "
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
            strErrorMessage += " | Divided by 0 (K) in er_algorithm. | "

        for n in range(numOfGrades):
            B[n] = K * (B[n] * M[r, n] + B[n] * (M[r, MTilde] + M[r, MBar]) + (B[MTilde] + BBar) * M[r, n])

        B[MTilde] = K * (B[MTilde] * M[r, MTilde] + BBar * M[r, MTilde] + B[MTilde] * M[r, MBar])
        BBar = K * BBar * M[r, MBar]

    # 使用完整性因子归一化组合的信度
    sngNormal = 1.0 - BBar
    if sngNormal != 0:
        B /= sngNormal
    else:
        strErrorMessage += " | Divided by 0 (sngNormal) in er_algorithm. | "

    # 检查是否有错误信息
    if strErrorMessage:
        print("An error occurred during the execution of the algorithm.")
        print(strErrorMessage)
        return False
    else:
        return B[:numOfGrades]