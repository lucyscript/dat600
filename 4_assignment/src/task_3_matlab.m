f = -[3; 6; 5];
A = [
    0 1 2;
    3 2 1;
    1 1 1;
];
b = [6; 24; 12];
lb = [0; 0; 0];

[x, fval, exitflag, output] = linprog(f, A, b, [], [], lb, []);
max_value = -fval;

disp('Optimal x =');
disp(x);
disp('Maximum objective value =');
disp(max_value);
disp('Exit flag =');
disp(exitflag);
disp('Solver output =');
disp(output);
