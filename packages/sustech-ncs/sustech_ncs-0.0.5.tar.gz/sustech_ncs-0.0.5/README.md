# A python impletation of NCS-C.



参考文献：

**K. Tang, P. Yang and X. Yao, "Negatively Correlated Search," in IEEE Journal on Selected Areas in Communications, vol. 34, no. 3, pp. 542-550, March 2016, doi: 10.1109/JSAC.2016.2525458.**



算法包sustech_ncs下，`NCS`是NCS-C的多进程并行加速的实现，`NCS_noMul`是未进行多进程加速的版本，`NCS_asym`是加入了非对称优化的实现版本。



使用示例:

```python
import numpy as np

# import optproblems.cec2005 as benchmark
import opfunu.cec_based.cec2005 as benchmark
from sustech_ncs import NCS


if __name__=='__main__':

    dimension0=30
    pop_size0=10 #
    sigma0=0.2  # 注意sigma不能是整数
    r0=0.80      #
    epoch0=10   #
    T0=30000
    scope = np.array([[-np.pi, np.pi]] * dimension0)

    # 选择测试使用的fitness function
    function=benchmark.F122005(ndim=dimension0).evaluate # opfunu
    # function=benchmark.F1(num_variables=dimension0) # optproblems
    optimizer = NCS(function, dimensions=dimension0, pop_size=pop_size0, sigma=np.full(pop_size0, sigma0), r=r0, epoch=epoch0, T_max=T0 ,scope=scope)

    best_solution, best_f_solution = optimizer.NCS_run()
    print("Best solution found by NCS:", best_solution)
    print("Objective function value:", best_f_solution)
    print(f"Function: {optimizer.objective_function_individual}, \n"
        f"Dimensions: {optimizer.dimensions}, Population Size: {optimizer.pop_size}, Sigma: {sigma0}, \n"
        f"R: {optimizer.r}, Epoch: {optimizer.epoch}, T_max: {optimizer.T_max}, "
        f"Scope: {optimizer.scope[0]}")

    # # opfunu用法
    # dimension = 10
    # problem = benchmark.F12005(dimension)
    # solution = [0.1] * dimension 
    # value = problem.evaluate(solution)
    # print(value)

    # # optproblems用法
    # dimension = 10
    # problem = benchmark.F1(dimension)
    # solution = [0.1] * dimension
    # value = problem(solution)
```



