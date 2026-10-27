# Lab 5 – Reflection

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest issues to fix were the formatting and naming-related ones, such as blank-line warnings, missing docstrings, and inconsistent function names. These were relatively straightforward because the tools clearly indicated what needed to be changed.

The harder issues were related to the actual behaviour of the program. For example, the program accepted negative passenger counts and crashed when it tried to access route R3, which had already been removed. Fixing the bare `except` was also more complicated because it involved understanding why the exception was occurring instead of simply suppressing it. I learned that some fixes require understanding how different parts of the program interact, rather than just making individual changes.

## 2. Did the static analysis tools report any false positives? If so, describe one example.

One example is Bandit's B311 warning about `random.choice`. In this program, the function is used to select a shuttle driver, so using a predictable random generator does not necessarily create a security risk. Therefore, the warning is less relevant in this particular context than it would be in a security-sensitive application. I still replaced it with `secrets.choice` since it costs nothing, but in this context it could reasonably have been suppressed with `# nosec B311`.

I also noticed that some Pylint warnings, such as missing docstrings, are mainly related to code quality and maintainability rather than immediate functional problems. This helped me understand that a warning should be evaluated based on the context instead of assuming that every warning represents a serious bug.

## 3. How would you integrate static analysis tools into your actual software development workflow?

I would use tools such as Pylint and Flake8 regularly while developing, so that coding issues can be identified early. I could also configure pre-commit hooks to run checks before committing changes.

For a team project, I would integrate these tools into a CI pipeline using GitHub Actions so that the checks run automatically whenever code is pushed or a pull request is created. This would help maintain consistent code quality across the team. I would also use shared configuration files so that everyone follows the same rules. However, I would still run the program and test important scenarios because static analysis alone cannot detect every runtime bug.

## 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

The Pylint score improved from 6.25/10 to 10.00/10, Bandit went from 2 issues to none, and Flake8 went from 10 warnings to 0. The fixes improved the code's readability through consistent naming, better documentation, and cleaner formatting. The input-validation changes also made the program more robust by preventing invalid passenger counts from being accepted and by handling missing or unknown routes more safely.

Another important observation was that the original program crashed when it attempted to access route R3 after that route had been removed. This showed me that static analysis tools and actual program execution serve different purposes. Static analysis helps identify potential problems in the code, while running and testing the program helps reveal errors that may only occur during execution.

Overall, I learned that improving code quality involves more than just eliminating warnings. It also requires understanding the underlying problems, testing the fixes, and checking whether the program behaves correctly in different situations.
