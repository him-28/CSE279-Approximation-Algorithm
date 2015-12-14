# CSE279-Approximation-Algorithm
Implementation of Berkowitz’s Algorithm as Approximation Algorithm Project .

Berkowitz’s algorithm is the fastest known parallel algorithm for computing the characteristic polynomial of a matrix. For the sake of simplicity I assume that the matrices are over {0, 1}, i.e., the two field elements, where plus is XOR and multiplication is AND. The algorithm is designed such that the process takes no more than log^2(n) sequentially many steps. The program is then rigorously tested to ensure its accuracy.

The Python threading library is used to accomplish the log^2(n) step complexity requirement. Even though the threaded implementation takes significantly longer to run than the single thread implementation, the purpose of this project is to show methods in which threaded peers can operate to complete this task in less steps. 
