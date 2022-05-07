# CS766-Analysis-of-Concurrent-Programe
**Introduction **
Our task was to develop a tiny software tool that takes a program as input and outputs all valid traces. Input program is allowed to have assert statement in it. If there exists a sequential execution(valid trace) that violates the assert statement, then our tool stops exploring traces and outputs the result as “Assertion violation” and displays this trace. 

**Input constraints: **
1. 1 ≤ n ≤ 10. 2. Maximum number of instruction per process = 4 3. Fixed global variables: x , y, and z. 4. Maximum number of local registers in the input program= 10 5. Each read instruction can obtain its value from max 4 write instruction. So, if there is read instruction, r = x, then it can obtain a value of x from max 4 write instructions on variable x. 6. Initially x=0 , y=0 , z=0. (Global variables are initialised with zero.)
