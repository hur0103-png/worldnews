# QA Workflow Rule
When making code changes (especially HTML, CSS, JavaScript, or Python files), you MUST proactively check for syntax errors, missing brackets, broken string interpolations, and encoding issues (like corrupted Korean characters).
Before finalizing changes and telling the user "it is done", you MUST invoke the `bug_hunter` subagent or run strict syntax checks locally to verify that the code is free of bugs and parses correctly. Do NOT skip this step.
