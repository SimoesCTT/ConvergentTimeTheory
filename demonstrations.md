# Chronos Demonstrations

## 1. Basic Convergence
\`\`\`chronos
timeline x = [1, 2, 3, 4, 5];
x <~ 3.5;
result = converge(x);
\`\`\`

## 2. Factorial Constraint Solving  
\`\`\`chronos
timeline result = 1;
result <~ 120;  // 5! = 120
computed = converge(result);
\`\`\`

## 3. Multi-Variable Optimization
\`\`\`chronos
timeline temp = [1.0, 1.5, 2.0, 2.5, 3.0];
timeline emissions = [10, 20, 30, 40, 50];
temp <~ 1.8;
emissions <~ 25;
optimal = converge(temp) * converge(emissions);
\`\`\`
